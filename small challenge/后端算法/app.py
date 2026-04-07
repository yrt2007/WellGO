from flask import Flask, request, jsonify, render_template_string, send_file
from flask_cors import CORS
import os
import json
import tempfile
import uuid
import sys
from movement_evaluator import VideoPoseProcessor, MovementEvaluator

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB


@app.route('/')
def home():
    """提供 HTML 页面"""
    with open('video-upload(3).html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)


@app.route('/api/upload', methods=['POST'])
def upload_videos():
    """上传标准视频和练习视频"""
    try:
        if 'standard_video' not in request.files or 'practice_video' not in request.files:
            return jsonify({'error': '请上传两个视频文件'}), 400

        standard_file = request.files['standard_video']
        practice_file = request.files['practice_video']
        exercise_type = request.form.get('exercise_type', 'dance')

        # 生成唯一会话 ID
        session_id = str(uuid.uuid4())
        session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        os.makedirs(session_folder, exist_ok=True)

        # 保存视频文件
        standard_path = os.path.join(session_folder, 'standard.mp4')
        practice_path = os.path.join(session_folder, 'practice.mp4')

        standard_file.save(standard_path)
        practice_file.save(practice_path)

        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': '视频上传成功'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/evaluate', methods=['POST'])
def evaluate_movement():
    """执行运动评估"""
    try:
        data = request.json
        session_id = data.get('session_id')
        exercise_type = data.get('exercise_type', 'dance')

        if not session_id:
            return jsonify({'error': '缺少会话ID'}), 400

        session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        standard_path = os.path.join(session_folder, 'standard.mp4')
        practice_path = os.path.join(session_folder, 'practice.mp4')

        if not os.path.exists(standard_path) or not os.path.exists(practice_path):
            return jsonify({'error': '视频文件不存在'}), 400

        # 处理标准视频
        print(f"处理标准视频: {standard_path}")
        std_processor = VideoPoseProcessor(model_complexity=1)
        std_data = std_processor.process_video(
            input_video_path=standard_path,
            output_json_path=os.path.join(session_folder, 'standard_pose_data.json')
        )
        std_processor.cleanup()

        # 处理用户视频
        print(f"处理用户视频: {practice_path}")
        usr_processor = VideoPoseProcessor(model_complexity=1)
        usr_data = usr_processor.process_video(
            input_video_path=practice_path,
            output_json_path=os.path.join(session_folder, 'user_pose_data.json')
        )
        usr_processor.cleanup()

        # 运动评估
        print("执行运动评估...")
        evaluator = MovementEvaluator(
            standard_data=std_data,
            user_data=usr_data,
            exercise_type=exercise_type
        )

        evaluation_results = evaluator.evaluate_movement()

        # 生成可视化图表
        viz_path = os.path.join(session_folder, 'comparison.png')
        evaluator.visualize_comparison(output_path=viz_path)

        # 生成改进建议
        improvement_suggestions = generate_improvement_suggestions(evaluation_results)

        # 构建前端所需的响应格式
        response_data = {
            'success': True,
            'overall_score': float(evaluation_results['overall_score']),
            'dimension_scores': {
                'standardization': {
                    'score': float(evaluation_results['dimension_scores']['standardization']),
                    'name': '动作规范性',
                    'description': '评估动作与标准动作的相似度'
                },
                'rhythm': {
                    'score': float(evaluation_results['dimension_scores']['rhythm']),
                    'name': '节奏匹配度',
                    'description': '评估动作节奏的同步性'
                },
                'fluency': {
                    'score': float(evaluation_results['dimension_scores']['fluency']),
                    'name': '动作流畅性',
                    'description': '评估动作的平滑度和连贯性'
                },
                'power': {
                    'score': float(evaluation_results['dimension_scores']['power']),
                    'name': '力量控制',
                    'description': '评估力量和速度的控制'
                }
            },
            'detailed_feedback': improvement_suggestions,
            'visualization_url': f'/api/results/{session_id}/comparison.png'
        }

        # 保存评估结果
        results_path = os.path.join(session_folder, 'evaluation_results.json')
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(response_data, f, indent=2, ensure_ascii=False)

        return jsonify(response_data)

    except Exception as e:
        print(f"评估过程中发生错误: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/results/<session_id>/<filename>')
def get_result_file(session_id, filename):
    """获取结果文件"""
    try:
        session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        file_path = os.path.join(session_folder, filename)

        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            return jsonify({'error': '文件不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def generate_improvement_suggestions(evaluation_results):
    """生成改进建议"""
    suggestions = []
    overall_score = evaluation_results['overall_score']

    # 根据综合得分给出总体评价
    if overall_score >= 90:
        suggestions.append({
            'type': 'good',
            'title': '优秀表现',
            'content': '您的动作非常标准，继续保持！'
        })
    elif overall_score >= 80:
        suggestions.append({
            'type': 'good',
            'title': '表现良好',
            'content': '动作基本标准，有一些细节可以改进'
        })
    elif overall_score >= 70:
        suggestions.append({
            'type': 'warning',
            'title': '需要改进',
            'content': '动作基本正确，但需要较多改进'
        })
    else:
        suggestions.append({
            'type': 'error',
            'title': '需要大量练习',
            'content': '建议从基础动作开始练习'
        })

    # 根据各维度得分给出具体建议
    dimension_scores = evaluation_results['dimension_scores']

    if dimension_scores['standardization'] < 80:
        suggestions.append({
            'type': 'warning',
            'title': '动作规范性',
            'content': '注意关节角度和身体姿态，参考标准动作调整'
        })

    if dimension_scores['rhythm'] < 80:
        suggestions.append({
            'type': 'warning',
            'title': '节奏匹配度',
            'content': '注意跟随音乐节奏，保持动作同步性'
        })

    if dimension_scores['fluency'] < 80:
        suggestions.append({
            'type': 'warning',
            'title': '动作流畅性',
            'content': '减少动作停顿，保持动作连贯平滑'
        })

    if dimension_scores['power'] < 80:
        suggestions.append({
            'type': 'warning',
            'title': '力量控制',
            'content': '注意控制动作力度，避免过大或过小'
        })

    # 从详细结果中提取具体的关节反馈
    standardization_details = evaluation_results['details']['standardization']
    if standardization_details:
        # 找出得分最低的关节
        worst_joints = sorted(standardization_details.items(),
                              key=lambda x: x[1]['score'])[:2]
        for joint, details in worst_joints:
            if details['score'] < 70:
                suggestions.append({
                    'type': 'error',
                    'title': f'{joint} 需要改进',
                    'content': f'该关节角度偏差较大 (RMSE: {details["rmse"]:.1f}°)，请特别注意'
                })

    return suggestions


@app.route('/api/history')
def get_history():
    """获取历史评估记录"""
    # 这里可以从数据库读取历史记录
    # 简化示例：返回模拟数据
    return jsonify({
        'success': True,
        'history': [
            {
                'id': 1,
                'practice_name': '舞蹈练习1',
                'standard_name': '标准舞蹈示范',
                'score': 85.5,
                'date': '2024-01-15 14:30',
                'feedback': [
                    {'type': 'good', 'title': '节奏感', 'content': '节奏把握良好'},
                    {'type': 'warning', 'title': '动作幅度', 'content': '可以加大动作幅度'}
                ]
            }
        ]
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')