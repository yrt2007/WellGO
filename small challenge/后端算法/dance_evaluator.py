import cv2
import numpy as np
import mediapipe as mp
import json
import os
import sys
from tqdm import tqdm
from scipy.spatial.distance import euclidean
from scipy.signal import butter, filtfilt
from scipy.interpolate import interp1d
from fastdtw import fastdtw
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyArrowPatch
import warnings
import platform


# 设置中文字体（在导入plt之后立即设置）
def setup_chinese_font():
    """设置中文字体支持"""
    system = platform.system()

    # 尝试设置中文字体
    if system == 'Windows':
        # Windows系统常见中文字体
        chinese_fonts = ['Microsoft YaHei', 'SimHei', 'KaiTi', 'FangSong', 'STSong']
    elif system == 'Darwin':  # macOS
        chinese_fonts = ['PingFang SC', 'Hiragino Sans GB', 'STHeiti', 'Apple LiGothic']
    else:  # Linux
        chinese_fonts = ['WenQuanYi Zen Hei', 'Noto Sans CJK SC', 'DejaVu Sans']

    # 查找可用的中文字体
    available_fonts = []
    for font in chinese_fonts:
        try:
            # 检查字体是否可用
            font_prop = fm.FontProperties(family=font)
            font_path = fm.findfont(font_prop, fallback_to_default=False)
            if font_path:
                available_fonts.append(font)
        except:
            continue

    # 设置可用的中文字体
    if available_fonts:
        # 优先使用第一个可用的中文字体
        plt.rcParams['font.sans-serif'] = available_fonts
        plt.rcParams['axes.unicode_minus'] = False
        print(f"已设置中文字体: {available_fonts[0]}")
    else:
        # 如果没有中文字体，使用英文字体
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
        print("未找到中文字体，使用英文字体")

    return available_fonts


# 调用字体设置
available_fonts = setup_chinese_font()

warnings.filterwarnings('ignore')

# 初始化MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


class VideoPoseProcessor:
    def __init__(self, model_complexity=1):
        """初始化姿态处理器

        Args:
            model_complexity: 模型复杂度 (0:轻量, 1:中等, 2:重量级)
        """
        self.pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=model_complexity,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # 姿态关键点名称映射
        self.landmark_names = [
            "鼻子", "左眼内角", "左眼", "左眼外角",
            "右眼内角", "右眼", "右眼外角", "左耳",
            "右耳", "左嘴角", "右嘴角", "左肩",
            "右肩", "左肘", "右肘", "左腕",
            "右腕", "左小指", "右小指", "左食指",
            "右食指", "左拇指", "右拇指", "左髋",
            "右髋", "左膝", "右膝", "左踝",
            "右踝", "左脚跟", "右脚跟", "左脚尖",
            "右脚尖"
        ]

        # 关节连接定义 (用于角度计算)
        self.joint_connections = {
            '左肘': [11, 13, 15],  # 左肩, 左肘, 左腕
            '右肘': [12, 14, 16],  # 右肩, 右肘, 右腕
            '左肩': [13, 11, 23],  # 左肘, 左肩, 左髋
            '右肩': [14, 12, 24],  # 右肘, 右肩, 右髋
            '左髋': [11, 23, 25],  # 左肩, 左髋, 左膝
            '右髋': [12, 24, 26],  # 右肩, 右髋, 右膝
            '左膝': [23, 25, 27],  # 左髋, 左膝, 左踝
            '右膝': [24, 26, 28],  # 右髋, 右膝, 右踝
            '左踝': [25, 27, 31],  # 左膝, 左踝, 左脚尖
            '右踝': [26, 28, 32]  # 右膝, 右踝, 右脚尖
        }

    def process_video(self, input_video_path, output_video_path=None, output_json_path=None):
        """处理视频并输出标注视频和姿态数据

        Args:
            input_video_path: 输入视频文件路径
            output_video_path: 输出标注视频路径（可选）
            output_json_path: 输出姿态JSON文件路径（可选）

        Returns:
            tuple: (姿态数据, 视频信息)
        """
        # 检查输入文件
        if not os.path.exists(input_video_path):
            raise FileNotFoundError(f"输入视频文件不存在: {input_video_path}")

        # 打开视频文件
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {input_video_path}")

        # 获取视频信息
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        if fps == 0:  # 如果无法获取fps，设置默认值
            fps = 30
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(f"视频信息:")
        print(f"  分辨率: {width}x{height}")
        print(f"  帧率: {fps} FPS")
        print(f"  总帧数: {total_frames}")

        # 初始化输出视频写入器
        video_writer = None
        if output_video_path:
            # 创建输出目录（如果不存在）
            output_dir = os.path.dirname(output_video_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # 尝试不同的编码器以确保视频可播放
            codec_options = [
                ('mp4v', '.mp4'),  # MPEG-4编码，通常兼容性好
                ('avc1', '.mp4'),  # H.264编码
                ('XVID', '.avi'),  # 如果mp4不行，尝试avi格式
                ('MJPG', '.avi')  # Motion-JPEG编码
            ]

            video_writer = None
            for codec, ext in codec_options:
                # 确保文件扩展名匹配编码器
                if not output_video_path.endswith(ext):
                    base_path = os.path.splitext(output_video_path)[0]
                    current_output_path = base_path + ext
                else:
                    current_output_path = output_video_path

                fourcc = cv2.VideoWriter_fourcc(*codec)
                temp_writer = cv2.VideoWriter(
                    current_output_path,
                    fourcc,
                    fps,
                    (width, height)
                )

                if temp_writer.isOpened():
                    video_writer = temp_writer
                    output_video_path = current_output_path  # 更新为实际使用的路径
                    print(f"  使用编码器: {codec}")
                    print(f"  输出文件: {output_video_path}")
                    break
                else:
                    print(f"  编码器 {codec} 不可用，尝试下一个...")

            if video_writer is None:
                print("警告: 无法创建视频写入器，将不输出视频文件")

        # 存储姿态数据
        pose_data = {
            "video_info": {
                "fps": fps,
                "width": width,
                "height": height,
                "total_frames": total_frames,
                "input_path": input_video_path,
                "output_path": output_video_path if video_writer else None
            },
            "frames": [],
            "landmark_names": self.landmark_names,
            "joint_angles": {}  # 存储关节角度数据
        }

        frame_count = 0
        frames_with_pose = 0

        # 使用进度条
        print(f"开始处理视频...")
        if total_frames > 0:
            pbar = tqdm(total=total_frames, desc="处理进度")
        else:
            pbar = None
            print("警告: 无法确定视频总帧数，进度条不可用")

        # 存储每一帧的关节角度
        joint_angle_sequences = {joint: [] for joint in self.joint_connections.keys()}

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            # 处理当前帧
            frame_data, annotated_frame = self.process_frame(frame)

            # 计算关节角度
            if frame_data:
                frame_joint_angles = self.calculate_joint_angles(frame_data)
                for joint, angle in frame_joint_angles.items():
                    joint_angle_sequences[joint].append(angle)
            else:
                for joint in self.joint_connections.keys():
                    joint_angle_sequences[joint].append(None)

            # 添加帧信息到数据
            frame_info = {
                "frame_number": frame_count,
                "landmarks": frame_data,
                "joint_angles": frame_joint_angles if frame_data else {}
            }
            pose_data["frames"].append(frame_info)

            if frame_data:  # 如果检测到姿态
                frames_with_pose += 1

            # 写入输出视频
            if video_writer and annotated_frame is not None:
                # 确保帧的尺寸正确
                if annotated_frame.shape[1] != width or annotated_frame.shape[0] != height:
                    annotated_frame = cv2.resize(annotated_frame, (width, height))
                video_writer.write(annotated_frame)

            if pbar:
                pbar.update(1)
                # 每100帧更新一次状态
                if frame_count % 100 == 0:
                    pbar.set_postfix({
                        "检测到姿态的帧": f"{frames_with_pose}/{frame_count}"
                    })

        if pbar:
            pbar.close()

        # 存储关节角度序列
        pose_data["joint_angles"] = joint_angle_sequences

        # 释放资源
        cap.release()
        if video_writer:
            video_writer.release()
            print(f"视频文件已保存: {output_video_path}")

        # 保存姿态数据到JSON文件
        if output_json_path:
            self.save_pose_data(pose_data, output_json_path)

        print(f"\n处理完成!")
        print(f"  处理总帧数: {frame_count}")
        print(f"  检测到姿态的帧数: {frames_with_pose} ({frames_with_pose / max(frame_count, 1) * 100:.1f}%)")

        return pose_data

    def process_frame(self, frame):
        """处理单帧图像

        Args:
            frame: 输入图像帧

        Returns:
            tuple: (姿态数据, 标注后的图像帧)
        """
        # 创建原始帧的副本用于标注
        annotated_frame = frame.copy()

        # 转换颜色空间
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False

        # 姿态检测
        results = self.pose.process(image_rgb)

        # 转换回BGR用于显示
        image_rgb.flags.writeable = True

        landmark_data = []

        if results.pose_landmarks:
            # 在图像上绘制骨架
            mp_drawing.draw_landmarks(
                annotated_frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )

            # 提取关键点数据
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                h, w, _ = frame.shape

                landmark_info = {
                    "name": self.landmark_names[idx] if idx < len(self.landmark_names) else f"landmark_{idx}",
                    "x": float(landmark.x),
                    "y": float(landmark.y),
                    "z": float(landmark.z) if hasattr(landmark, 'z') else 0.0,
                    "visibility": float(landmark.visibility) if hasattr(landmark, 'visibility') else 0.0,
                    "pixel_x": int(landmark.x * w),
                    "pixel_y": int(landmark.y * h)
                }
                landmark_data.append(landmark_info)

            # 在图像上显示关键关节角度
            joint_angles = self.calculate_joint_angles(landmark_data)
            self.draw_joint_angles(annotated_frame, joint_angles)

        return landmark_data, annotated_frame

    def calculate_joint_angles(self, landmarks):
        """计算关节角度

        Args:
            landmarks: 关键点数据列表

        Returns:
            dict: 关节角度字典
        """
        joint_angles = {}

        for joint_name, joint_indices in self.joint_connections.items():
            if len(landmarks) > max(joint_indices):
                # 获取三个关键点的坐标
                p1 = landmarks[joint_indices[0]]
                p2 = landmarks[joint_indices[1]]  # 顶点
                p3 = landmarks[joint_indices[2]]

                # 转换为向量
                v1 = np.array([p1['pixel_x'] - p2['pixel_x'], p1['pixel_y'] - p2['pixel_y']])
                v2 = np.array([p3['pixel_x'] - p2['pixel_x'], p3['pixel_y'] - p2['pixel_y']])

                # 计算向量夹角（角度）
                angle = self.vector_angle(v1, v2)
                joint_angles[joint_name] = angle

        return joint_angles

    def vector_angle(self, v1, v2):
        """计算两个向量之间的夹角（0-180度）

        Args:
            v1, v2: 输入向量

        Returns:
            float: 夹角角度
        """
        # 计算点积和模长
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)

        # 防止除以零
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0

        # 计算余弦值并限制在[-1, 1]范围内
        cos_theta = dot_product / (norm_v1 * norm_v2)
        cos_theta = np.clip(cos_theta, -1.0, 1.0)

        # 计算角度
        angle = np.degrees(np.arccos(cos_theta))
        return angle

    def draw_joint_angles(self, image, joint_angles, position=(10, 30)):
        """在图像上绘制关节角度

        Args:
            image: 输入图像
            joint_angles: 关节角度字典
            position: 文字起始位置
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_color = (0, 255, 0)
        line_type = 2

        y_offset = 0
        for i, (joint, angle) in enumerate(list(joint_angles.items())[:5]):  # 只显示前5个关节
            text = f"{joint}: {angle:.1f}°"
            y = position[1] + y_offset
            cv2.putText(image, text, (position[0], y), font, font_scale, font_color, line_type)
            y_offset += 25

    def save_pose_data(self, pose_data, output_path):
        """保存姿态数据到JSON文件

        Args:
            pose_data: 姿态数据字典
            output_path: 输出JSON文件路径
        """
        # 创建输出目录（如果不存在）
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 保存到JSON文件
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(pose_data, f, indent=2, ensure_ascii=False)

        print(f"姿态数据已保存到: {output_path}")
        return output_path

    def cleanup(self):
        """清理资源"""
        self.pose.close()


class DanceEvaluator:
    """舞蹈运动评估器，专门用于评估跳舞视频"""

    def __init__(self, standard_data, user_data, dance_style="general"):
        """初始化舞蹈评估器

        Args:
            standard_data: 标准舞蹈视频的姿态数据
            user_data: 用户舞蹈视频的姿态数据
            dance_style: 舞蹈风格 ("科目三", "hiphop", "ballet", "general")
        """
        self.standard_data = standard_data
        self.user_data = user_data
        self.dance_style = dance_style

        # 舞蹈风格特定的关节权重
        self.joint_weights = self.get_dance_joint_weights(dance_style)

        # 预处理角度序列
        self.std_angles = self.preprocess_angles(standard_data["joint_angles"])
        self.usr_angles = self.preprocess_angles(user_data["joint_angles"])

        # 时间对齐
        self.std_aligned, self.usr_aligned = self.time_align_sequences()

        # 评估结果
        self.evaluation_results = {}

    def get_dance_joint_weights(self, dance_style):
        """获取舞蹈运动的关节权重

        Args:
            dance_style: 舞蹈风格

        Returns:
            dict: 关节权重字典
        """
        # 基础权重（所有关节）
        weights = {
            '左肘': 1.0, '右肘': 1.0,
            '左肩': 1.0, '右肩': 1.0,
            '左髋': 1.0, '右髋': 1.0,
            '左膝': 1.0, '右膝': 1.0,
            '左踝': 1.0, '右踝': 1.0
        }

        dance_style_lower = dance_style.lower()

        if "科目三" in dance_style_lower or dance_style_lower == "kemusan":
            # 科目三舞蹈权重：注重髋部摆动、脚步节奏和身体协调性
            print("使用科目三舞蹈权重配置")
            weights.update({
                '左髋': 2.5,  # 髋部摆动是关键
                '右髋': 2.5,
                '左膝': 2.0,  # 膝盖节奏重要
                '右膝': 2.0,
                '左踝': 1.8,  # 脚踝动作
                '右踝': 1.8,
                '左肩': 1.5,  # 肩部协调
                '右肩': 1.5,
                '左肘': 1.3,  # 手臂动作
                '右肘': 1.3
            })

        elif dance_style_lower == "hiphop" or dance_style_lower == "街舞":
            # 街舞权重：注重全身协调和节奏感
            print("使用街舞权重配置")
            weights.update({
                '左髋': 2.0,
                '右髋': 2.0,
                '左膝': 1.8,
                '右膝': 1.8,
                '左肩': 1.8,
                '右肩': 1.8,
                '左肘': 1.5,
                '右肘': 1.5,
                '左踝': 1.3,
                '右踝': 1.3
            })

        elif dance_style_lower == "ballet" or dance_style_lower == "芭蕾":
            # 芭蕾权重：注重腿部姿态和身体平衡
            print("使用芭蕾舞权重配置")
            weights.update({
                '左膝': 2.5,
                '右膝': 2.5,
                '左踝': 2.2,
                '右踝': 2.2,
                '左髋': 1.8,
                '右髋': 1.8,
                '左肩': 1.5,
                '右肩': 1.5,
                '左肘': 1.2,
                '右肘': 1.2
            })

        else:
            # 通用舞蹈权重：注重全身协调
            print("使用通用舞蹈权重配置")
            weights.update({
                '左髋': 1.8,
                '右髋': 1.8,
                '左膝': 1.6,
                '右膝': 1.6,
                '左肩': 1.4,
                '右肩': 1.4,
                '左踝': 1.2,
                '右踝': 1.2
            })

        # 归一化权重
        total_weight = sum(weights.values())
        for joint in weights:
            weights[joint] /= total_weight / len(weights)

        return weights

    def preprocess_angles(self, angle_sequences):
        """预处理角度序列：填充缺失值并滤波

        Args:
            angle_sequences: 原始角度序列

        Returns:
            dict: 预处理后的角度序列
        """
        processed = {}

        for joint, angles in angle_sequences.items():
            if angles:
                # 转换为numpy数组
                angles_array = np.array(angles, dtype=np.float32)

                # 处理缺失值 (None)
                mask = np.isnan(angles_array)
                if np.any(mask):
                    # 使用线性插值填充缺失值
                    indices = np.arange(len(angles_array))
                    angles_array[mask] = np.interp(indices[mask], indices[~mask], angles_array[~mask])

                # 应用低通滤波器去除噪声
                if len(angles_array) > 10:
                    angles_array = self.butter_lowpass_filter(angles_array, cutoff=5.0, fs=30.0)

                processed[joint] = angles_array

        return processed

    def butter_lowpass_filter(self, data, cutoff=5.0, fs=30.0, order=4):
        """应用巴特沃斯低通滤波器

        Args:
            data: 输入数据
            cutoff: 截止频率
            fs: 采样频率
            order: 滤波器阶数

        Returns:
            ndarray: 滤波后的数据
        """
        nyquist = 0.5 * fs
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        y = filtfilt(b, a, data)
        return y

    def time_align_sequences(self):
        """时间对齐两个序列（使用DTW或插值）

        Returns:
            tuple: (对齐后的标准序列, 对齐后的用户序列)
        """
        std_aligned = {}
        usr_aligned = {}

        for joint in self.std_angles.keys():
            if joint in self.usr_angles:
                std_seq = self.std_angles[joint]
                usr_seq = self.usr_angles[joint]

                # 如果序列长度不同，使用动态时间规整对齐
                if len(std_seq) != len(usr_seq):
                    std_seq_2d = std_seq.reshape(-1, 1)
                    usr_seq_2d = usr_seq.reshape(-1, 1)

                    # 使用fastdtw进行对齐
                    distance, path = fastdtw(std_seq_2d, usr_seq_2d, dist=euclidean)

                    # 根据路径对齐序列
                    std_aligned_seq = np.zeros(len(path))
                    usr_aligned_seq = np.zeros(len(path))

                    for i, (std_idx, usr_idx) in enumerate(path):
                        std_aligned_seq[i] = std_seq[std_idx] if std_idx < len(std_seq) else std_seq[-1]
                        usr_aligned_seq[i] = usr_seq[usr_idx] if usr_idx < len(usr_seq) else usr_seq[-1]

                    std_aligned[joint] = std_aligned_seq
                    usr_aligned[joint] = usr_aligned_seq
                else:
                    std_aligned[joint] = std_seq
                    usr_aligned[joint] = usr_seq

        return std_aligned, usr_aligned

    def evaluate_dance_movement(self):
        """执行完整的舞蹈运动评估

        Returns:
            dict: 评估结果
        """
        print("=" * 60)
        print(f"开始评估 {self.dance_style} 舞蹈")
        print("=" * 60)

        # 评估四个维度
        standardization_score, standardization_details = self.evaluate_dance_standardization()
        rhythm_score, rhythm_details = self.evaluate_dance_rhythm()
        fluency_score, fluency_details = self.evaluate_dance_fluency()
        expression_score, expression_details = self.evaluate_dance_expression()

        # 舞蹈风格专项评估
        if "科目三" in self.dance_style.lower():
            special_score, special_details = self.evaluate_kemusan_special()
            print(f"  科目三专项得分: {special_score:.1f}/100")

        # 计算综合得分（舞蹈运动的权重）
        weights = {
            'standardization': 0.25,  # 规范性
            'rhythm': 0.35,  # 节奏感（舞蹈非常重要）
            'fluency': 0.25,  # 流畅性
            'expression': 0.15  # 表现力
        }

        overall_score = (
                standardization_score * weights['standardization'] +
                rhythm_score * weights['rhythm'] +
                fluency_score * weights['fluency'] +
                expression_score * weights['expression']
        )

        # 构建评估结果
        self.evaluation_results = {
            'overall_score': overall_score,
            'dimension_scores': {
                'standardization': standardization_score,
                'rhythm': rhythm_score,
                'fluency': fluency_score,
                'expression': expression_score
            },
            'details': {
                'standardization': standardization_details,
                'rhythm': rhythm_details,
                'fluency': fluency_details,
                'expression': expression_details
            },
            'dance_style': self.dance_style,
            'joint_weights': self.joint_weights
        }

        # 如果有专项评估，添加到结果中
        if "科目三" in self.dance_style.lower():
            self.evaluation_results['special_score'] = special_score
            self.evaluation_results['special_details'] = special_details

        return self.evaluation_results

    def evaluate_dance_standardization(self):
        """评估舞蹈动作规范性：与标准动作的相似度

        Returns:
            tuple: (总得分, 详细得分)
        """
        print("\n评估舞蹈动作规范性...")

        joint_scores = {}
        total_weighted_score = 0
        total_weight = 0

        for joint in self.std_aligned.keys():
            if joint in self.usr_aligned:
                std_seq = self.std_aligned[joint]
                usr_seq = self.usr_aligned[joint]

                # 计算均方根误差 (RMSE)
                rmse = np.sqrt(np.mean((std_seq - usr_seq) ** 2))

                # 对于舞蹈，允许更大的动作变化范围
                # 将RMSE转换为分数 (0-100分)
                max_rmse = 40.0  # 舞蹈允许更大的误差
                score = max(0, 100 - (rmse / max_rmse * 100))

                # 应用关节权重
                weight = self.joint_weights.get(joint, 1.0)
                weighted_score = score * weight

                joint_scores[joint] = {
                    'score': score,
                    'weighted_score': weighted_score,
                    'rmse': rmse,
                    'weight': weight
                }

                total_weighted_score += weighted_score
                total_weight += weight

        # 计算加权平均分
        standardization_score = total_weighted_score / total_weight if total_weight > 0 else 0

        # 显示结果
        print(f"  动作规范性得分: {standardization_score:.1f}/100")

        # 显示问题最大的3个关节
        worst_joints = sorted(joint_scores.items(), key=lambda x: x[1]['score'])[:3]
        for joint, scores in worst_joints:
            if scores['score'] < 70:
                print(f"    {joint}: {scores['score']:.1f}分 (偏差: {scores['rmse']:.1f}°)")

        return standardization_score, joint_scores

    def evaluate_dance_rhythm(self):
        """评估舞蹈节奏匹配度：动作时间序列的同步性和节奏感

        Returns:
            tuple: (总得分, 详细得分)
        """
        print("\n评估舞蹈节奏匹配度...")

        # 计算主要关节的角度变化率（角速度）
        if "科目三" in self.dance_style.lower():
            primary_joints = ['左髋', '右髋', '左膝', '右膝']  # 科目三注重髋部和膝盖
        else:
            primary_joints = ['左髋', '右髋', '左肩', '右肩']  # 通用舞蹈注重髋部和肩部

        rhythm_scores = {}

        for joint in primary_joints:
            if joint in self.std_aligned and joint in self.usr_aligned:
                std_seq = self.std_aligned[joint]
                usr_seq = self.usr_aligned[joint]

                # 计算角速度（一阶差分）
                std_velocity = np.diff(std_seq)
                usr_velocity = np.diff(usr_seq)

                # 计算角速度的相关系数
                if len(std_velocity) > 1 and len(usr_velocity) > 1:
                    # 确保长度相同
                    min_len = min(len(std_velocity), len(usr_velocity))
                    std_vel = std_velocity[:min_len]
                    usr_vel = usr_velocity[:min_len]

                    # 计算相关系数
                    correlation = np.corrcoef(std_vel, usr_vel)[0, 1]

                    # 处理NaN值
                    if np.isnan(correlation):
                        correlation = 0

                    # 对于舞蹈，节奏感更重要
                    # 将相关系数转换为分数 (-1到1映射到0-100分)
                    score = max(0, (correlation + 1) / 2 * 100)

                    # 计算节奏稳定性（速度变化的标准差）
                    if len(usr_velocity) > 5:
                        velocity_std = np.std(usr_velocity)
                        stability_score = max(0, 100 - velocity_std * 2)
                    else:
                        stability_score = 50

                    # 综合节奏得分
                    rhythm_score = 0.7 * score + 0.3 * stability_score

                    rhythm_scores[joint] = {
                        'score': rhythm_score,
                        'correlation': correlation,
                        'stability_score': stability_score,
                        'velocity_std': velocity_std if 'velocity_std' in locals() else 0
                    }

        # 计算平均节奏得分
        if rhythm_scores:
            rhythm_score = np.mean([s['score'] for s in rhythm_scores.values()])
        else:
            rhythm_score = 0

        print(f"  节奏匹配度得分: {rhythm_score:.1f}/100")

        return rhythm_score, rhythm_scores

    def evaluate_dance_fluency(self):
        """评估舞蹈动作流畅性：角度变化的平滑度和连贯性

        Returns:
            tuple: (总得分, 详细得分)
        """
        print("\n评估舞蹈动作流畅性...")

        joint_scores = {}

        for joint in self.usr_angles.keys():
            angles = self.usr_angles[joint]

            if len(angles) > 10:
                # 计算角速度（一阶差分）
                velocity = np.diff(angles)

                # 计算角加速度（二阶差分）
                acceleration = np.diff(velocity)

                if len(acceleration) > 0:
                    # 计算加速度的标准差（越小越平滑）
                    accel_std = np.std(acceleration)

                    # 计算加速度变化的平均绝对值（jerk，越小越流畅）
                    jerk = np.mean(np.abs(np.diff(acceleration))) if len(acceleration) > 1 else 0

                    # 对于舞蹈，流畅性要求更高
                    max_accel_std = 30.0  # 比普通运动更严格
                    max_jerk = 50.0

                    accel_score = max(0, 100 - (accel_std / max_accel_std * 100))
                    jerk_score = max(0, 100 - (jerk / max_jerk * 100))

                    # 计算动作连贯性（速度过零次数，反映动作变化频率）
                    zero_crossings = np.where(np.diff(np.sign(velocity)))[0]
                    if len(velocity) > 0:
                        change_frequency = len(zero_crossings) / len(velocity) * 100
                        # 适度的变化频率更好（既不是太单调，也不是太杂乱）
                        frequency_score = max(0, 100 - abs(change_frequency - 15) * 3)
                    else:
                        frequency_score = 50

                    # 综合流畅度得分
                    fluency_score = 0.5 * accel_score + 0.3 * jerk_score + 0.2 * frequency_score

                    joint_scores[joint] = {
                        'score': fluency_score,
                        'acceleration_std': accel_std,
                        'jerk': jerk,
                        'change_frequency': change_frequency if 'change_frequency' in locals() else 0,
                        'accel_score': accel_score,
                        'jerk_score': jerk_score,
                        'frequency_score': frequency_score
                    }

        # 计算加权平均流畅度得分
        if joint_scores:
            total_weighted_score = 0
            total_weight = 0

            for joint, scores in joint_scores.items():
                weight = self.joint_weights.get(joint, 1.0)
                total_weighted_score += scores['score'] * weight
                total_weight += weight

            fluency_score = total_weighted_score / total_weight if total_weight > 0 else 0
        else:
            fluency_score = 0

        print(f"  动作流畅性得分: {fluency_score:.1f}/100")

        return fluency_score, joint_scores

    def evaluate_dance_expression(self):
        """评估舞蹈表现力：动作幅度、身体协调性和表现力

        Returns:
            tuple: (总得分, 详细得分)
        """
        print("\n评估舞蹈表现力...")

        expression_scores = {}

        # 1. 评估动作幅度
        amplitude_scores = {}
        for joint in self.usr_angles.keys():
            angles = self.usr_angles[joint]
            if len(angles) > 5:
                angle_range = np.max(angles) - np.min(angles)

                # 根据不同关节设定理想幅度
                if '髋' in joint:
                    ideal_range = 60.0  # 髋部应该有较大摆动
                elif '膝' in joint:
                    ideal_range = 80.0  # 膝盖弯曲幅度
                elif '肘' in joint:
                    ideal_range = 100.0  # 肘部活动范围
                elif '肩' in joint:
                    ideal_range = 70.0  # 肩部活动
                elif '踝' in joint:
                    ideal_range = 50.0  # 脚踝活动
                else:
                    ideal_range = 60.0

                # 幅度得分（接近理想幅度为高分）
                range_ratio = angle_range / ideal_range if ideal_range > 0 else 1
                if range_ratio < 0.5:
                    amplitude_score = range_ratio * 100  # 幅度太小
                elif range_ratio > 1.5:
                    amplitude_score = max(0, 100 - (range_ratio - 1) * 50)  # 幅度太大
                else:
                    amplitude_score = 100 - abs(range_ratio - 1) * 50  # 接近理想

                amplitude_scores[joint] = {
                    'score': amplitude_score,
                    'range': angle_range,
                    'ideal_range': ideal_range,
                    'range_ratio': range_ratio
                }

        # 2. 评估身体协调性（对称性和相位关系）
        coordination_scores = {}

        # 检查左右对称性
        for left_joint in ['左髋', '左膝', '左踝', '左肩', '左肘']:
            right_joint = left_joint.replace('左', '右')
            if left_joint in self.usr_angles and right_joint in self.usr_angles:
                left_angles = self.usr_angles[left_joint]
                right_angles = self.usr_angles[right_joint]

                if len(left_angles) == len(right_angles) and len(left_angles) > 10:
                    # 计算对称性（角度差的平均值）
                    symmetry_error = np.mean(np.abs(left_angles - right_angles))
                    symmetry_score = max(0, 100 - symmetry_error * 2)

                    coordination_scores[f'{left_joint}_对称性'] = {
                        'score': symmetry_score,
                        'symmetry_error': symmetry_error
                    }

        # 检查上下肢协调性（髋部和肩部的相位关系）
        if '左髋' in self.usr_angles and '左肩' in self.usr_angles:
            hip_angles = self.usr_angles['左髋']
            shoulder_angles = self.usr_angles['左肩']

            if len(hip_angles) == len(shoulder_angles) and len(hip_angles) > 20:
                # 计算相位差（使用互相关）
                correlation = np.corrcoef(hip_angles, shoulder_angles)[0, 1]
                phase_score = max(0, (correlation + 1) / 2 * 100)

                coordination_scores['上下肢协调性'] = {
                    'score': phase_score,
                    'correlation': correlation
                }

        # 3. 综合表现力得分
        if amplitude_scores and coordination_scores:
            # 计算平均幅度得分（加权）
            amplitude_total = 0
            amplitude_weight = 0
            for joint, scores in amplitude_scores.items():
                weight = self.joint_weights.get(joint, 1.0)
                amplitude_total += scores['score'] * weight
                amplitude_weight += weight

            avg_amplitude_score = amplitude_total / amplitude_weight if amplitude_weight > 0 else 0

            # 计算平均协调性得分
            avg_coordination_score = np.mean([s['score'] for s in coordination_scores.values()])

            # 综合表现力得分
            expression_score = 0.6 * avg_amplitude_score + 0.4 * avg_coordination_score

            expression_scores = {
                'amplitude_scores': amplitude_scores,
                'coordination_scores': coordination_scores,
                'avg_amplitude': avg_amplitude_score,
                'avg_coordination': avg_coordination_score
            }
        else:
            expression_score = 0

        print(f"  舞蹈表现力得分: {expression_score:.1f}/100")

        return expression_score, expression_scores

    def evaluate_kemusan_special(self):
        """科目三舞蹈的专项评估
        科目三舞蹈特点：髋部摆动、脚步节奏、手臂协调
        """
        print("\n评估科目三舞蹈专项...")

        special_scores = {}

        # 1. 评估髋部摆动幅度和频率
        hip_joints = ['左髋', '右髋']
        hip_scores = []

        for joint in hip_joints:
            if joint in self.usr_angles:
                angles = self.usr_angles[joint]
                if len(angles) > 20:
                    # 计算摆动幅度（角度变化范围）
                    angle_range = np.max(angles) - np.min(angles)

                    # 计算摆动频率（过零次数）
                    zero_crossings = np.where(np.diff(np.sign(np.diff(angles))))[0]
                    frequency = len(zero_crossings) / len(angles) * 100

                    # 科目三理想：中等幅度+高频率
                    range_score = min(100, angle_range * 2)  # 理想50度=100分
                    freq_score = min(100, frequency * 10)  # 理想10%频率=100分

                    hip_score = 0.6 * range_score + 0.4 * freq_score
                    hip_scores.append(hip_score)

                    special_scores[f'{joint}_摆动'] = {
                        'score': hip_score,
                        'range': angle_range,
                        'frequency': frequency,
                        'range_score': range_score,
                        'freq_score': freq_score
                    }

        # 2. 评估脚步节奏（脚踝动作）
        ankle_joints = ['左踝', '右踝']
        ankle_scores = []

        for joint in ankle_joints:
            if joint in self.usr_angles:
                angles = self.usr_angles[joint]
                if len(angles) > 20:
                    # 计算动作的规律性（自相关）
                    autocorr = self.calculate_autocorrelation(angles, max_lag=15)
                    regularity = np.mean(np.abs(autocorr[:5]))  # 短期自相关

                    # 计算节奏稳定性
                    velocity = np.diff(angles)
                    if len(velocity) > 5:
                        velocity_std = np.std(velocity)
                        stability = max(0, 1 - velocity_std / 10)
                    else:
                        stability = 0.5

                    ankle_score = (regularity * 0.7 + stability * 0.3) * 100
                    ankle_scores.append(ankle_score)

                    special_scores[f'{joint}_节奏'] = {
                        'score': ankle_score,
                        'regularity': regularity,
                        'stability': stability
                    }

        # 3. 评估整体协调性（髋部和脚踝的相位关系）
        coordination_score = 0
        if '左髋' in self.usr_angles and '左踝' in self.usr_angles:
            hip_angles = self.usr_angles['左髋'][:100]  # 取前100帧
            ankle_angles = self.usr_angles['左踝'][:100]

            if len(hip_angles) == len(ankle_angles) and len(hip_angles) > 10:
                # 计算相位差相关性
                correlation = np.corrcoef(hip_angles, ankle_angles)[0, 1]
                coordination_score = max(0, (correlation + 1) / 2 * 100)

                special_scores['身体协调性'] = {
                    'score': coordination_score,
                    'correlation': correlation
                }

        # 4. 计算科目三专项总分
        all_scores = []
        if hip_scores:
            all_scores.extend(hip_scores)
        if ankle_scores:
            all_scores.extend(ankle_scores)
        if coordination_score > 0:
            all_scores.append(coordination_score)

        if all_scores:
            kemusan_score = np.mean(all_scores)
        else:
            kemusan_score = 0

        return kemusan_score, special_scores

    def calculate_autocorrelation(self, data, max_lag=10):
        """计算数据的自相关性（用于评估节奏）

        Args:
            data: 输入数据序列
            max_lag: 最大滞后

        Returns:
            ndarray: 自相关系数
        """
        n = len(data)
        if n < max_lag * 2:
            max_lag = n // 2

        autocorr = np.zeros(max_lag)

        for lag in range(max_lag):
            if lag < n:
                autocorr[lag] = np.corrcoef(data[:n - lag], data[lag:n])[0, 1]
            else:
                autocorr[lag] = 0

        return autocorr

    def generate_dance_report(self, output_path=None):
        """生成舞蹈评估报告

        Args:
            output_path: 输出报告路径（可选）

        Returns:
            str: 报告内容
        """
        if not self.evaluation_results:
            self.evaluate_dance_movement()

        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append(f"{self.dance_style}舞蹈评估报告")
        report_lines.append("=" * 70)
        report_lines.append(f"舞蹈风格: {self.dance_style}")
        report_lines.append(f"综合得分: {self.evaluation_results['overall_score']:.1f}/100")
        report_lines.append("")

        # 各维度得分
        report_lines.append("各维度得分:")
        report_lines.append("-" * 30)
        for dimension, score in self.evaluation_results['dimension_scores'].items():
            dimension_name = {
                'standardization': '动作规范性',
                'rhythm': '节奏匹配度',
                'fluency': '动作流畅性',
                'expression': '舞蹈表现力'
            }.get(dimension, dimension)

            # 添加评分条
            bar_length = 20
            filled_length = int(bar_length * score / 100)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)

            report_lines.append(f"{dimension_name:10} {score:5.1f}/100 [{bar}]")

        report_lines.append("")

        # 详细分析
        report_lines.append("详细分析:")
        report_lines.append("-" * 30)

        # 动作规范性详情
        standardization_details = self.evaluation_results['details']['standardization']
        if standardization_details:
            report_lines.append("1. 动作规范性分析:")
            worst_joints = sorted(standardization_details.items(),
                                  key=lambda x: x[1]['score'])[:3]
            for joint, details in worst_joints:
                if details['score'] < 70:
                    report_lines.append(f"   • {joint}: 与标准动作偏差较大 (偏差: {details['rmse']:.1f}°)")

        # 节奏匹配度详情
        rhythm_details = self.evaluation_results['details']['rhythm']
        if rhythm_details:
            report_lines.append("\n2. 节奏匹配度分析:")
            for joint, details in list(rhythm_details.items())[:2]:
                correlation = details['correlation']
                if correlation < 0.6:
                    report_lines.append(f"   • {joint}: 节奏同步性需要提高 (同步率: {correlation:.2f})")

        # 动作流畅性详情
        fluency_details = self.evaluation_results['details']['fluency']
        if fluency_details:
            report_lines.append("\n3. 动作流畅性分析:")
            worst_joints = sorted(fluency_details.items(),
                                  key=lambda x: x[1]['score'])[:2]
            for joint, details in worst_joints:
                if details['score'] < 70:
                    report_lines.append(f"   • {joint}: 动作不够流畅 (抖动指数: {details['jerk']:.1f})")

        # 舞蹈表现力详情
        expression_details = self.evaluation_results['details']['expression']
        if expression_details and 'amplitude_scores' in expression_details:
            report_lines.append("\n4. 舞蹈表现力分析:")
            amplitude_scores = expression_details['amplitude_scores']
            low_amplitude = [(j, s) for j, s in amplitude_scores.items() if s['score'] < 70]
            if low_amplitude:
                for joint, details in low_amplitude[:2]:
                    report_lines.append(
                        f"   • {joint}: 动作幅度不足 (当前: {details['range']:.1f}°, 理想: {details['ideal_range']:.1f}°)")

        # 科目三专项分析
        if "科目三" in self.dance_style.lower() and 'special_details' in self.evaluation_results:
            report_lines.append("\n5. 科目三专项分析:")
            special_details = self.evaluation_results['special_details']
            for item, details in special_details.items():
                if 'score' in details and details['score'] < 70:
                    if '摆动' in item:
                        report_lines.append(f"   • {item}: 摆动幅度或频率不足")
                    elif '节奏' in item:
                        report_lines.append(f"   • {item}: 节奏稳定性需要提高")

        report_lines.append("")
        report_lines.append("舞蹈改进建议:")
        report_lines.append("-" * 30)

        # 根据舞蹈风格和得分提供建议
        overall_score = self.evaluation_results['overall_score']

        if "科目三" in self.dance_style.lower():
            report_lines.append("💃 科目三舞蹈专项建议:")

            if self.evaluation_results['dimension_scores']['rhythm'] < 80:
                report_lines.append("  - 加强节奏感训练，特别是髋部摆动与音乐的配合")
                report_lines.append("  - 使用节拍器练习，确保动作踩准节拍")

            if self.evaluation_results['dimension_scores']['fluency'] < 80:
                report_lines.append("  - 练习动作的连贯性，减少动作之间的停顿")
                report_lines.append("  - 特别注意髋部和膝盖的协调运动")

            # 检查科目三专项问题
            if 'special_score' in self.evaluation_results and self.evaluation_results['special_score'] < 70:
                report_lines.append("  - 重点练习髋部摆动，增加摆动幅度和频率")
                report_lines.append("  - 加强脚步练习，确保脚步节奏稳定")

            if overall_score >= 85:
                report_lines.append("  - 继续保持，可以尝试增加舞蹈表现力和个人风格")
            elif overall_score >= 70:
                report_lines.append("  - 基础不错，需要加强节奏感和动作协调性")
            else:
                report_lines.append("  - 从基础动作开始练习，重点掌握髋部摆动和基本步伐")

        else:
            # 通用舞蹈建议
            if overall_score >= 90:
                report_lines.append("💃 舞蹈表现非常出色！")
                report_lines.append("  - 继续保持高水平的舞蹈技巧")
                report_lines.append("  - 可以尝试更具挑战性的舞蹈动作")
                report_lines.append("  - 注重情感表达和舞台表现力")
            elif overall_score >= 80:
                report_lines.append("💃 舞蹈表现良好")
                report_lines.append("  - 继续保持良好的舞蹈基础")
                report_lines.append("  - 加强动作的精确性和节奏感")
                report_lines.append("  - 尝试增加舞蹈的层次感和变化")
            elif overall_score >= 70:
                report_lines.append("💃 舞蹈表现合格")
                report_lines.append("  - 加强基础动作练习")
                report_lines.append("  - 注意动作的连贯性和流畅性")
                report_lines.append("  - 多听音乐，提高节奏感")
            else:
                report_lines.append("💃 需要更多练习")
                report_lines.append("  - 从最基本的舞蹈动作开始练习")
                report_lines.append("  - 加强身体协调性训练")
                report_lines.append("  - 观看教学视频，学习正确动作")
                report_lines.append("  - 保持练习，每天进步一点点")

        report_lines.append("")
        report_lines.append("=" * 70)

        report_text = "\n".join(report_lines)

        # 保存报告到文件
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"舞蹈评估报告已保存到: {output_path}")

        # 显示报告
        print(report_text)

        return report_text

    def visualize_dance_comparison(self, output_path="dance_comparison.png"):
        """可视化用户和标准舞蹈动作的对比

        Args:
            output_path: 输出图像路径
        """
        # 确保字体设置
        if available_fonts:
            plt.rcParams['font.sans-serif'] = available_fonts
        plt.rcParams['axes.unicode_minus'] = False

        # 选择关键关节进行可视化
        if "科目三" in self.dance_style.lower():
            key_joints = ['左髋', '右髋', '左膝', '左踝']
            joint_keys = ['左髋', '右髋', '左膝', '左踝']
            chart_title = f'{self.dance_style}舞蹈动作对比分析'
        else:
            key_joints = ['左髋', '右髋', '左肩', '右肩']
            joint_keys = ['左髋', '右髋', '左肩', '右肩']
            chart_title = f'{self.dance_style}舞蹈动作对比分析'

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()

        for i, (joint_name, joint_key) in enumerate(zip(key_joints, joint_keys)):
            if i < len(axes) and joint_key in self.std_aligned and joint_key in self.usr_aligned:
                ax = axes[i]

                # 获取对齐后的序列
                std_seq = self.std_aligned[joint_key]
                usr_seq = self.usr_aligned[joint_key]

                # 创建时间轴（归一化到0-100%）
                time_std = np.linspace(0, 100, len(std_seq))
                time_usr = np.linspace(0, 100, len(usr_seq))

                # 绘制曲线
                ax.plot(time_std, std_seq, 'b-', linewidth=2, label='标准舞蹈', alpha=0.7)
                ax.plot(time_usr, usr_seq, 'r-', linewidth=2, label='用户舞蹈', alpha=0.7)

                # 填充差异区域
                min_len = min(len(std_seq), len(usr_seq))
                if min_len > 0:
                    time_common = np.linspace(0, 100, min_len)
                    std_common = std_seq[:min_len]
                    usr_common = usr_seq[:min_len]

                    # 填充差异区域
                    ax.fill_between(time_common, std_common, usr_common,
                                    where=std_common >= usr_common,
                                    interpolate=True, color='red', alpha=0.2, label='差异区域')
                    ax.fill_between(time_common, std_common, usr_common,
                                    where=std_common <= usr_common,
                                    interpolate=True, color='blue', alpha=0.2)

                # 设置图表属性
                ax.set_xlabel('时间 (%)', fontsize=10)
                ax.set_ylabel('角度 (°)', fontsize=10)
                ax.set_title(f'{joint_name} 角度对比', fontsize=12, fontweight='bold')
                ax.legend(loc='best')
                ax.grid(True, alpha=0.3)

                # 计算并显示RMSE
                if min_len > 0:
                    rmse = np.sqrt(np.mean((std_common - usr_common) ** 2))
                    ax.text(0.05, 0.95, f'偏差: {rmse:.1f}°',
                            transform=ax.transAxes, fontsize=10,
                            verticalalignment='top',
                            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        # 如果所有子图都为空，关闭它们
        for i in range(len(key_joints), len(axes)):
            axes[i].set_visible(False)

        # 调整布局
        plt.suptitle(chart_title, fontsize=16, fontweight='bold')
        plt.tight_layout()

        # 保存图像
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.show()

        print(f"舞蹈对比图表已保存到: {output_path}")


def main():
    """主函数：完整的舞蹈评估流程"""
    import argparse

    parser = argparse.ArgumentParser(description='舞蹈运动评估系统')
    parser.add_argument('standard_video', help='标准舞蹈视频路径')
    parser.add_argument('user_video', help='用户舞蹈视频路径')
    parser.add_argument('--dance_style', '-ds', default='科目三',
                        help='舞蹈风格 (科目三, hiphop, ballet, general, 默认: 科目三)')
    parser.add_argument('--output_dir', '-od', default='dance_evaluation_results',
                        help='输出目录 (默认: dance_evaluation_results)')
    parser.add_argument('--model_complexity', '-mc', type=int, default=1,
                        help='模型复杂度: 0=轻量, 1=中等, 2=重量级 (默认: 1)')

    args = parser.parse_args()

    # 创建输出目录
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    try:
        print("=" * 60)
        print("舞蹈运动评估系统")
        print("=" * 60)

        # 1. 处理标准视频
        print(f"\n1. 处理标准舞蹈视频: {args.standard_video}")
        std_processor = VideoPoseProcessor(model_complexity=args.model_complexity)
        std_output_json = os.path.join(args.output_dir, 'standard_dance_data.json')
        std_data = std_processor.process_video(
            input_video_path=args.standard_video,
            output_json_path=std_output_json
        )
        std_processor.cleanup()

        # 2. 处理用户视频
        print(f"\n2. 处理用户舞蹈视频: {args.user_video}")
        usr_processor = VideoPoseProcessor(model_complexity=args.model_complexity)
        usr_output_json = os.path.join(args.output_dir, 'user_dance_data.json')
        usr_data = usr_processor.process_video(
            input_video_path=args.user_video,
            output_json_path=usr_output_json
        )
        usr_processor.cleanup()

        # 3. 舞蹈评估
        print(f"\n3. 执行舞蹈评估")
        evaluator = DanceEvaluator(
            standard_data=std_data,
            user_data=usr_data,
            dance_style=args.dance_style
        )

        evaluation_results = evaluator.evaluate_dance_movement()

        # 4. 生成报告
        print(f"\n4. 生成舞蹈评估报告")
        report_path = os.path.join(args.output_dir, 'dance_evaluation_report.txt')
        evaluator.generate_dance_report(output_path=report_path)

        # 5. 可视化对比
        print(f"\n5. 生成可视化对比")
        viz_path = os.path.join(args.output_dir, 'dance_comparison.png')
        evaluator.visualize_dance_comparison(output_path=viz_path)

        # 6. 保存完整评估结果
        results_path = os.path.join(args.output_dir, 'dance_evaluation_results.json')
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(evaluation_results, f, indent=2, ensure_ascii=False)

        print(f"\n✓ 舞蹈评估完成！结果保存在: {args.output_dir}")
        print(f"  - 姿态数据: standard_dance_data.json, user_dance_data.json")
        print(f"  - 评估报告: dance_evaluation_report.txt")
        print(f"  - 可视化图表: dance_comparison.png")
        print(f"  - 完整结果: dance_evaluation_results.json")

    except Exception as e:
        print(f"\n✗ 处理过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


def quick_dance_example():
    """快速舞蹈评估示例"""
    # 注意：这里需要替换为实际视频文件路径
    standard_video = "科目三-标准版.mp4"
    user_video = "科目三-用户版.mp4"

    if not os.path.exists(standard_video):
        print(f"警告: 标准舞蹈视频文件不存在: {standard_video}")
        print("请准备标准舞蹈视频和用户舞蹈视频")
        return

    if not os.path.exists(user_video):
        print(f"警告: 用户舞蹈视频文件不存在: {user_video}")
        print("请准备标准舞蹈视频和用户舞蹈视频")
        return

    # 创建输出目录
    output_dir = "dance_evaluation_results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. 处理标准视频
    print("处理标准舞蹈视频...")
    std_processor = VideoPoseProcessor(model_complexity=1)
    std_data = std_processor.process_video(
        input_video_path=standard_video,
        output_json_path=os.path.join(output_dir, 'standard_dance_data.json')
    )
    std_processor.cleanup()

    # 2. 处理用户视频
    print("\n处理用户舞蹈视频...")
    usr_processor = VideoPoseProcessor(model_complexity=1)
    usr_data = usr_processor.process_video(
        input_video_path=user_video,
        output_json_path=os.path.join(output_dir, 'user_dance_data.json')
    )
    usr_processor.cleanup()

    # 3. 舞蹈评估
    print("\n执行舞蹈评估...")
    evaluator = DanceEvaluator(
        standard_data=std_data,
        user_data=usr_data,
        dance_style="科目三"
    )

    evaluation_results = evaluator.evaluate_dance_movement()

    # 4. 生成报告
    print("\n生成舞蹈评估报告...")
    evaluator.generate_dance_report(output_path=os.path.join(output_dir, 'dance_evaluation_report.txt'))

    print(f"\n舞蹈评估完成！结果保存在: {output_dir}")


if __name__ == "__main__":
    # 使用命令行参数运行
    main()

    # 或者运行快速示例
    # quick_dance_example()