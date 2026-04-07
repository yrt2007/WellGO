/* ============================================
   体操舞蹈教学视频库网站 - 交互功能脚本
   ============================================ */

// ============================================
// 视频数据
// ============================================

const videoData = [
    {
        id: 1,
        title: "基础体操入门 - 热身运动",
        instructor: "张美丽",
        duration: "12:30",
        difficulty: "easy",
        difficultyText: "初级",
        category: "基础动作",
        views: 15234,
        thumbnail: "https://placehold.co/400x225/6366f1/ffffff?text=热身运动",
        description: "本课程教授体操舞蹈的基础热身动作，包括头部、肩部、腰部、腿部等各个部位的拉伸和活动，帮助学员在开始正式训练前做好充分准备，预防运动损伤。",
        points: [
            "头部运动：左右旋转、前后点头，每个动作重复8次",
            "肩部运动：绕肩、扩胸运动，每个动作重复10次",
            "腰部运动：左右侧弯、前后弯曲，注意动作幅度适中",
            "腿部运动：弓步压腿、侧压腿，每侧保持20秒",
            "全身协调：开合跳30次，提升心率"
        ]
    },
    {
        id: 2,
        title: "芭蕾基础 - 站姿与手位",
        instructor: "李雪婷",
        duration: "18:45",
        difficulty: "easy",
        difficultyText: "初级",
        category: "基础动作",
        views: 12345,
        thumbnail: "https://placehold.co/400x225/8b5cf6/ffffff?text=站姿手位",
        description: "学习芭蕾舞的基本站姿和手位，这是所有芭蕾动作的基础。通过本课程，你将掌握正确的身体姿态和手臂位置，为后续学习打下坚实基础。",
        points: [
            "基础站姿：双脚并拢，脚尖外开，膝盖伸直",
            "一位手：手臂呈椭圆形，手指相对，位置在腰部前方",
            "二位手：手臂向两侧打开，略低于肩膀",
            "三位手：手臂向上延伸，形成优美的弧线",
            "保持呼吸平稳，核心收紧"
        ]
    },
    {
        id: 3,
        title: "现代舞 - 流动性训练",
        instructor: "王芳",
        duration: "25:10",
        difficulty: "medium",
        difficultyText: "中级",
        category: "舞蹈组合",
        views: 9876,
        thumbnail: "https://placehold.co/400x225/a855f7/ffffff?text=流动性训练",
        description: "现代舞强调身体的自由表达和流动性。本课程通过一系列连贯的动作组合，训练学员的身体控制能力和动作流畅性。",
        points: [
            "地面动作：从躺姿到站姿的流畅转换",
            "空间感知：利用整个舞蹈空间进行移动",
            "呼吸配合：动作与呼吸的协调统一",
            "重心转移：学习在不同支撑点之间转移重心",
            "情感表达：通过动作传达内在情感"
        ]
    },
    {
        id: 4,
        title: "技巧训练 - 后空翻入门",
        instructor: "陈强",
        duration: "15:20",
        difficulty: "hard",
        difficultyText: "高级",
        category: "技巧训练",
        views: 7654,
        thumbnail: "https://placehold.co/400x225/ec4899/ffffff?text=后空翻",
        description: "后空翻是体操中的一项高难度技巧动作。本课程适合有一定基础的学员，通过分解教学，逐步掌握后空翻的技术要领。",
        points: [
            "热身准备：充分活动手腕、脚踝和腰部",
            "基础练习：后滚翻和倒立练习",
            "起跳技巧：膝盖弯曲，手臂上摆，快速起跳",
            "空中姿态：身体紧缩，下巴收向胸部",
            "落地缓冲：膝盖微屈，双脚同时着地"
        ]
    },
    {
        id: 5,
        title: "民族舞 - 藏族舞基础",
        instructor: "卓玛",
        duration: "20:30",
        difficulty: "medium",
        difficultyText: "中级",
        category: "舞蹈组合",
        views: 8765,
        thumbnail: "https://placehold.co/400x225/f43f5e/ffffff?text=藏族舞",
        description: "藏族舞以其独特的风格和丰富的文化内涵而闻名。本课程教授藏族舞的基本步伐和手部动作，让你感受高原舞蹈的魅力。",
        points: [
            "基本步伐：踢踏步、颤膝步",
            "手部动作：转腕、甩袖",
            "身体姿态：上身挺直，膝盖微屈",
            "节奏把握：配合藏族音乐的节拍",
            "表情管理：展现藏族人民的热情与豪迈"
        ]
    },
    {
        id: 6,
        title: "表演展示 - 舞台表现力",
        instructor: "刘晓梅",
        duration: "22:15",
        difficulty: "medium",
        difficultyText: "中级",
        category: "表演展示",
        views: 6543,
        thumbnail: "https://placehold.co/400x225/3b82f6/ffffff?text=舞台表现力",
        description: "优秀的舞者不仅要有扎实的技术功底，还需要出色的舞台表现力。本课程教授如何在舞台上更好地展现自己，与观众产生情感共鸣。",
        points: [
            "眼神交流：与观众建立眼神联系",
            "面部表情：根据舞蹈内容调整表情",
            "舞台空间：充分利用舞台的各个区域",
            "节奏掌控：在高潮部分加强表现",
            "自信展现：相信自己的能力，享受舞台"
        ]
    },
    {
        id: 7,
        title: "柔韧性训练 - 分腿劈叉",
        instructor: "赵敏",
        duration: "16:40",
        difficulty: "medium",
        difficultyText: "中级",
        category: "技巧训练",
        views: 11234,
        thumbnail: "https://placehold.co/400x225/10b981/ffffff?text=劈叉训练",
        description: "劈叉是体操舞蹈中展示柔韧性的经典动作。本课程通过科学的训练方法，帮助学员安全、有效地提高柔韧性，完成劈叉动作。",
        points: [
            "热身运动：充分活动髋关节和腿部肌肉",
            "压腿练习：前后压腿，每侧保持30秒",
            "辅助练习：利用墙壁或椅子辅助下压",
            "呼吸配合：下压时呼气，保持时深呼吸",
            "循序渐进：不要急于求成，避免拉伤"
        ]
    },
    {
        id: 8,
        title: "拉丁舞 - 伦巴基础",
        instructor: "Carlos Rodriguez",
        duration: "28:00",
        difficulty: "easy",
        difficultyText: "初级",
        category: "舞蹈组合",
        views: 14567,
        thumbnail: "https://placehold.co/400x225/f59e0b/ffffff?text=伦巴基础",
        description: "伦巴被称为"拉丁舞之魂"，以其浪漫和感性的风格著称。本课程教授伦巴的基本步伐和身体律动，让你感受拉丁舞的热情与魅力。",
        points: [
            "基本步伐：伦巴步、古巴步",
            "身体律动：胯部的8字形运动",
            "手臂动作：流畅的手臂线条",
            "情感表达：展现浪漫和感性的情感",
            "音乐配合：准确把握伦巴的节奏"
        ]
    },
    {
        id: 9,
        title: "技巧训练 - 侧手翻",
        instructor: "陈强",
        duration: "14:25",
        difficulty: "medium",
        difficultyText: "中级",
        category: "技巧训练",
        views: 9876,
        thumbnail: "https://placehold.co/400x225/6366f1/ffffff?text=侧手翻",
        description: "侧手翻是体操中的一项基础技巧动作，也是学习更复杂动作的前提。本课程通过分解教学，帮助学员掌握侧手翻的正确技术。",
        points: [
            "准备姿势：侧身站立，手臂上举",
            "起跳技巧：膝盖弯曲，快速蹬地",
            "手部支撑：双手依次着地，保持直线",
            "空中姿态：身体呈直线，双腿分开",
            "落地缓冲：双脚依次着地，膝盖微屈"
        ]
    },
    {
        id: 10,
        title: "表演展示 - 编舞技巧",
        instructor: "刘晓梅",
        duration: "30:15",
        difficulty: "hard",
        difficultyText: "高级",
        category: "表演展示",
        views: 5432,
        thumbnail: "https://placehold.co/400x225/8b5cf6/ffffff?text=编舞技巧",
        description: "编舞是将舞蹈动作组合成完整作品的艺术。本课程教授编舞的基本原则和技巧，帮助学员创作出属于自己的舞蹈作品。",
        points: [
            "主题确定：明确舞蹈的主题和情感",
            "音乐选择：选择与主题契合的音乐",
            "动作编排：根据音乐节奏编排动作",
            "空间利用：合理利用舞台空间",
            "细节打磨：注意动作的衔接和过渡"
        ]
    },
    {
        id: 11,
        title: "基础动作 - 踢腿训练",
        instructor: "张美丽",
        duration: "17:30",
        difficulty: "easy",
        difficultyText: "初级",
        category: "基础动作",
        views: 13456,
        thumbnail: "https://placehold.co/400x225/a855f7/ffffff?text=踢腿训练",
        description: "踢腿是体操舞蹈中的基础动作，对提高腿部力量和柔韧性非常重要。本课程教授正确的踢腿方法和注意事项。",
        points: [
            "准备姿势：站立，双手扶墙或椅子",
            "前踢腿：保持上身挺直，踢腿高度逐步提高",
            "侧踢腿：注意髋关节的灵活性",
            "后踢腿：保持身体平衡，不要过度后仰",
            "控制速度：踢腿和收腿都要有控制"
        ]
    },
    {
        id: 12,
        title: "技巧训练 - 前手翻",
        instructor: "陈强",
        duration: "19:45",
        difficulty: "hard",
        difficultyText: "高级",
        category: "技巧训练",
        views: 4321,
        thumbnail: "https://placehold.co/400x225/ec4899/ffffff?text=前手翻",
        description: "前手翻是一项高难度的体操技巧动作，需要良好的身体控制能力和勇气。本课程适合有扎实基础的学员学习。",
        points: [
            "热身准备：充分活动手腕和肩部",
            "基础练习：倒立和前滚翻练习",
            "起跳技巧：膝盖弯曲，快速向前上方起跳",
            "手部支撑：双手同时着地，保持平衡",
            "落地缓冲：双脚同时着地，向前滚动缓冲"
        ]
    }
];

// ============================================
// 全局变量
// ============================================

let currentPage = 1;
const itemsPerPage = 6;
let filteredVideos = [...videoData];
let selectedCategories = [];
let selectedDifficulties = [];
let searchQuery = '';
let currentSort = 'newest';

// ============================================
// DOM加载完成后执行
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    initNavbar();
    initMobileMenu();
    
    // 根据当前页面初始化相应功能
    const currentPath = window.location.pathname;
    
    if (currentPath.includes('video-library.html')) {
        initVideoLibrary();
    } else if (currentPath.includes('video-detail.html')) {
        initVideoDetail();
    } else {
        initHomePage();
    }
});

// ============================================
// 导航栏功能
// ============================================

function initNavbar() {
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        // 滚动时改变导航栏样式
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
}

// ============================================
// 移动端菜单功能
// ============================================

function initMobileMenu() {
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarMenu = document.querySelector('.navbar-menu');
    
    if (navbarToggle && navbarMenu) {
        navbarToggle.addEventListener('click', function() {
            navbarMenu.classList.toggle('active');
        });
        
        // 点击菜单项后关闭菜单
        const navbarLinks = navbarMenu.querySelectorAll('.navbar-link');
        navbarLinks.forEach(link => {
            link.addEventListener('click', function() {
                navbarMenu.classList.remove('active');
            });
        });
        
        // 点击页面其他区域关闭菜单
        document.addEventListener('click', function(event) {
            if (!navbarToggle.contains(event.target) && !navbarMenu.contains(event.target)) {
                navbarMenu.classList.remove('active');
            }
        });
    }
}

// ============================================
// 首页功能
// ============================================

function initHomePage() {
    renderRecommendedVideos();
}

function renderRecommendedVideos() {
    const container = document.querySelector('.recommended-videos-grid');
    if (!container) return;
    
    // 获取前6个视频作为推荐
    const recommendedVideos = videoData.slice(0, 6);
    
    container.innerHTML = recommendedVideos.map(video => createVideoCard(video)).join('');
    
    // 添加点击事件
    const videoCards = container.querySelectorAll('.video-card');
    videoCards.forEach((card, index) => {
        card.addEventListener('click', function() {
            navigateToVideoDetail(recommendedVideos[index].id);
        });
    });
}

// ============================================
// 视频库页面功能
// ============================================

function initVideoLibrary() {
    // 从URL读取参数
    loadFiltersFromURL();
    
    initSearch();
    initFilters();
    initSort();
    renderVideos();
    initPagination();
    initClearFilters();
}

function initSearch() {
    const searchInput = document.getElementById('searchInput');
    const clearButton = document.getElementById('clearSearch');
    
    if (searchInput) {
        // 设置初始值
        if (searchQuery) {
            searchInput.value = searchQuery;
            clearButton.style.display = 'block';
        }
        
        // 实时搜索
        searchInput.addEventListener('input', function(e) {
            searchQuery = e.target.value.toLowerCase().trim();
            
            // 显示/隐藏清除按钮
            clearButton.style.display = searchQuery ? 'block' : 'none';
            
            currentPage = 1;
            filterVideos();
            updateURL();
        });
    }
    
    // 清除搜索
    if (clearButton) {
        clearButton.addEventListener('click', function() {
            searchQuery = '';
            searchInput.value = '';
            clearButton.style.display = 'none';
            currentPage = 1;
            filterVideos();
            updateURL();
        });
    }
}

function initFilters() {
    // 分类筛选（多选）
    const categoryCheckboxes = document.querySelectorAll('#categoryFilters input[type="checkbox"]');
    categoryCheckboxes.forEach(checkbox => {
        // 设置初始选中状态
        if (selectedCategories.includes(checkbox.value)) {
            checkbox.checked = true;
        }
        
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                selectedCategories.push(this.value);
            } else {
                selectedCategories = selectedCategories.filter(c => c !== this.value);
            }
            currentPage = 1;
            filterVideos();
            updateURL();
        });
    });
    
    // 难度筛选（多选）
    const difficultyCheckboxes = document.querySelectorAll('#difficultyFilters input[type="checkbox"]');
    difficultyCheckboxes.forEach(checkbox => {
        // 设置初始选中状态
        if (selectedDifficulties.includes(checkbox.value)) {
            checkbox.checked = true;
        }
        
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                selectedDifficulties.push(this.value);
            } else {
                selectedDifficulties = selectedDifficulties.filter(d => d !== this.value);
            }
            currentPage = 1;
            filterVideos();
            updateURL();
        });
    });
}

function initSort() {
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        // 设置初始值
        sortSelect.value = currentSort;
        
        sortSelect.addEventListener('change', function(e) {
            currentSort = e.target.value;
            currentPage = 1;
            filterVideos();
            updateURL();
        });
    }
}

function initClearFilters() {
    const clearButton = document.getElementById('clearFilters');
    if (clearButton) {
        clearButton.addEventListener('click', function() {
            // 清除所有筛选条件
            selectedCategories = [];
            selectedDifficulties = [];
            searchQuery = '';
            currentSort = 'newest';
            currentPage = 1;
            
            // 重置UI
            document.querySelectorAll('#categoryFilters input[type="checkbox"]').forEach(cb => cb.checked = false);
            document.querySelectorAll('#difficultyFilters input[type="checkbox"]').forEach(cb => cb.checked = false);
            document.getElementById('searchInput').value = '';
            document.getElementById('clearSearch').style.display = 'none';
            document.getElementById('sortSelect').value = 'newest';
            
            filterVideos();
            updateURL();
        });
    }
}

function filterVideos() {
    filteredVideos = videoData.filter(video => {
        // 搜索筛选（标题、描述、讲师）
        const matchesSearch = !searchQuery || 
                            video.title.toLowerCase().includes(searchQuery) ||
                            video.description.toLowerCase().includes(searchQuery) ||
                            video.instructor.toLowerCase().includes(searchQuery);
        
        // 分类筛选（多选）
        const matchesCategory = selectedCategories.length === 0 || 
                               selectedCategories.includes(video.category);
        
        // 难度筛选（多选）
        const matchesDifficulty = selectedDifficulties.length === 0 || 
                                  selectedDifficulties.includes(video.difficulty);
        
        return matchesSearch && matchesCategory && matchesDifficulty;
    });
    
    // 排序
    sortVideos();
    
    renderVideos();
    renderPagination();
    updateResultsCount();
    updateClearFiltersButton();
}

function sortVideos() {
    switch (currentSort) {
        case 'newest':
            // 按ID降序（ID越大越新）
            filteredVideos.sort((a, b) => b.id - a.id);
            break;
        case 'popularity':
            // 按观看次数降序
            filteredVideos.sort((a, b) => b.views - a.views);
            break;
        case 'duration':
            // 按时长升序
            filteredVideos.sort((a, b) => {
                const durationA = parseDuration(a.duration);
                const durationB = parseDuration(b.duration);
                return durationA - durationB;
            });
            break;
    }
}

function parseDuration(duration) {
    // 将时长字符串（如 "12:30"）转换为秒数
    const parts = duration.split(':');
    return parseInt(parts[0]) * 60 + parseInt(parts[1]);
}

function updateResultsCount() {
    const resultsCount = document.getElementById('resultsCount');
    if (resultsCount) {
        resultsCount.textContent = `共 ${filteredVideos.length} 个视频`;
    }
}

function updateClearFiltersButton() {
    const clearButton = document.getElementById('clearFilters');
    if (clearButton) {
        const hasFilters = selectedCategories.length > 0 || 
                          selectedDifficulties.length > 0 || 
                          searchQuery !== '' ||
                          currentSort !== 'newest';
        clearButton.style.display = hasFilters ? 'block' : 'none';
    }
}

function renderVideos() {
    const container = document.querySelector('.videos-grid');
    if (!container) return;
    
    // 计算当前页的视频
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const currentVideos = filteredVideos.slice(startIndex, endIndex);
    
    if (currentVideos.length === 0) {
        container.innerHTML = `
            <div class="no-results" style="grid-column: 1 / -1; text-align: center; padding: 3rem;">
                <svg style="width: 64px; height: 64px; color: var(--text-light); margin-bottom: 1rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <p style="color: var(--text-secondary); font-size: 1.125rem;">没有找到匹配的视频</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = currentVideos.map(video => createVideoCard(video)).join('');
    
    // 添加点击事件
    const videoCards = container.querySelectorAll('.video-card');
    videoCards.forEach((card, index) => {
        card.addEventListener('click', function() {
            navigateToVideoDetail(currentVideos[index].id);
        });
    });
}

function initPagination() {
    const prevButton = document.querySelector('.pagination-prev');
    const nextButton = document.querySelector('.pagination-next');
    
    if (prevButton) {
        prevButton.addEventListener('click', function() {
            if (currentPage > 1) {
                currentPage--;
                renderVideos();
                renderPagination();
                updateURL();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    }
    
    if (nextButton) {
        nextButton.addEventListener('click', function() {
            const totalPages = Math.ceil(filteredVideos.length / itemsPerPage);
            if (currentPage < totalPages) {
                currentPage++;
                renderVideos();
                renderPagination();
                updateURL();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    }
}

function renderPagination() {
    const totalPages = Math.ceil(filteredVideos.length / itemsPerPage);
    const prevButton = document.querySelector('.pagination-prev');
    const nextButton = document.querySelector('.pagination-next');
    const pageNumbers = document.querySelector('.pagination-numbers');
    
    if (prevButton) {
        prevButton.disabled = currentPage === 1;
    }
    
    if (nextButton) {
        nextButton.disabled = currentPage === totalPages || totalPages === 0;
    }
    
    if (pageNumbers) {
        let html = '';
        for (let i = 1; i <= totalPages; i++) {
            html += `<button class="pagination-button ${i === currentPage ? 'active' : ''}" data-page="${i}">${i}</button>`;
        }
        pageNumbers.innerHTML = html;
        
        // 添加页码点击事件
        const pageButtons = pageNumbers.querySelectorAll('.pagination-button');
        pageButtons.forEach(button => {
            button.addEventListener('click', function() {
                currentPage = parseInt(this.dataset.page);
                renderVideos();
                renderPagination();
                updateURL();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });
    }
}

// ============================================
// 视频详情页功能
// ============================================

function initVideoDetail() {
    // 从URL获取视频ID
    const urlParams = new URLSearchParams(window.location.search);
    const videoId = parseInt(urlParams.get('id'));
    
    if (videoId) {
        const video = videoData.find(v => v.id === videoId);
        if (video) {
            renderVideoDetail(video);
        } else {
            // 如果找不到视频，显示错误信息
            showVideoNotFound();
        }
    } else {
        // 如果没有ID，显示第一个视频
        renderVideoDetail(videoData[0]);
    }
    
    initPlayButton();
}

function renderVideoDetail(video) {
    // 更新标题
    const titleElement = document.querySelector('.video-detail-title');
    if (titleElement) {
        titleElement.textContent = video.title;
    }
    
    // 更新元数据
    const instructorElement = document.querySelector('.meta-instructor');
    if (instructorElement) {
        instructorElement.innerHTML = `
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
            ${video.instructor}
        `;
    }
    
    const durationElement = document.querySelector('.meta-duration');
    if (durationElement) {
        durationElement.innerHTML = `
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            ${video.duration}
        `;
    }
    
    const difficultyElement = document.querySelector('.meta-difficulty');
    if (difficultyElement) {
        const difficultyClass = `difficulty-${video.difficulty}`;
        difficultyElement.innerHTML = `
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
            <span class="video-difficulty ${difficultyClass}">${video.difficultyText}</span>
        `;
    }
    
    const viewsElement = document.querySelector('.meta-views');
    if (viewsElement) {
        viewsElement.innerHTML = `
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
            </svg>
            ${formatViews(video.views)} 次观看
        `;
    }
    
    // 更新描述
    const descriptionElement = document.querySelector('.video-description');
    if (descriptionElement) {
        descriptionElement.textContent = video.description;
    }
    
    // 更新动作要点
    const pointsList = document.querySelector('.points-list');
    if (pointsList) {
        pointsList.innerHTML = video.points.map((point, index) => `
            <div class="point-item">
                <span class="point-number">${index + 1}</span>
                <span class="point-text">${point}</span>
            </div>
        `).join('');
    }
    
    // 渲染相关推荐视频
    renderRelatedVideos(video);
}

function renderRelatedVideos(currentVideo) {
    const container = document.querySelector('.related-videos-grid');
    if (!container) return;
    
    // 获取相关视频（排除当前视频）
    const relatedVideos = videoData
        .filter(v => v.id !== currentVideo.id)
        .filter(v => v.category === currentVideo.category || v.difficulty === currentVideo.difficulty)
        .slice(0, 4);
    
    // 如果相关视频不足4个，补充其他视频
    if (relatedVideos.length < 4) {
        const additionalVideos = videoData
            .filter(v => v.id !== currentVideo.id && !relatedVideos.includes(v))
            .slice(0, 4 - relatedVideos.length);
        relatedVideos.push(...additionalVideos);
    }
    
    container.innerHTML = relatedVideos.map(video => createVideoCard(video)).join('');
    
    // 添加点击事件
    const videoCards = container.querySelectorAll('.video-card');
    videoCards.forEach((card, index) => {
        card.addEventListener('click', function() {
            navigateToVideoDetail(relatedVideos[index].id);
        });
    });
}

function initPlayButton() {
    const playButton = document.querySelector('.play-button');
    if (playButton) {
        playButton.addEventListener('click', function() {
            alert('视频播放功能演示：在实际项目中，这里会加载真实的视频播放器。');
        });
    }
}

function showVideoNotFound() {
    const container = document.querySelector('.video-detail-container');
    if (container) {
        container.innerHTML = `
            <div style="text-align: center; padding: 4rem 2rem;">
                <svg style="width: 80px; height: 80px; color: var(--text-light); margin-bottom: 2rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                </svg>
                <h2 style="font-size: 2rem; color: var(--text-primary); margin-bottom: 1rem;">视频未找到</h2>
                <p style="color: var(--text-secondary); margin-bottom: 2rem;">抱歉，您要查看的视频不存在或已被删除。</p>
                <a href="video-library.html" style="display: inline-block; background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; padding: 1rem 2rem; border-radius: 0.5rem; font-weight: 600; transition: all 0.3s ease;">
                    返回视频库
                </a>
            </div>
        `;
    }
}

// ============================================
// URL参数同步功能
// ============================================

function loadFiltersFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    
    // 读取搜索关键词
    if (urlParams.has('q')) {
        searchQuery = urlParams.get('q').toLowerCase();
    }
    
    // 读取分类筛选
    if (urlParams.has('category')) {
        selectedCategories = urlParams.get('category').split(',').filter(c => c);
    }
    
    // 读取难度筛选
    if (urlParams.has('difficulty')) {
        selectedDifficulties = urlParams.get('difficulty').split(',').filter(d => d);
    }
    
    // 读取排序方式
    if (urlParams.has('sort')) {
        currentSort = urlParams.get('sort') || 'newest';
    }
    
    // 读取页码
    if (urlParams.has('page')) {
        currentPage = parseInt(urlParams.get('page')) || 1;
    }
}

function updateURL() {
    const url = new URL(window.location);
    const params = new URLSearchParams();
    
    // 添加搜索关键词
    if (searchQuery) {
        params.set('q', searchQuery);
    }
    
    // 添加分类筛选
    if (selectedCategories.length > 0) {
        params.set('category', selectedCategories.join(','));
    }
    
    // 添加难度筛选
    if (selectedDifficulties.length > 0) {
        params.set('difficulty', selectedDifficulties.join(','));
    }
    
    // 添加排序方式
    if (currentSort !== 'newest') {
        params.set('sort', currentSort);
    }
    
    // 添加页码
    if (currentPage > 1) {
        params.set('page', currentPage);
    }
    
    // 更新URL（不刷新页面）
    url.search = params.toString();
    window.history.replaceState({}, '', url);
}

// ============================================
// 辅助函数
// ============================================

function createVideoCard(video) {
    const difficultyClass = `difficulty-${video.difficulty}`;
    return `
        <div class="video-card fade-in" data-id="${video.id}">
            <div class="video-thumbnail">
                <img src="${video.thumbnail}" alt="${video.title}" loading="lazy">
                <span class="video-duration">${video.duration}</span>
            </div>
            <div class="video-content">
                <h3 class="video-title">${video.title}</h3>
                <div class="video-instructor">
                    <svg style="width: 16px; height: 16px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                    ${video.instructor}
                </div>
                <div class="video-meta">
                    <span class="video-difficulty ${difficultyClass}">${video.difficultyText}</span>
                    <span class="video-views">${formatViews(video.views)} 观看</span>
                </div>
            </div>
        </div>
    `;
}

function formatViews(views) {
    if (views >= 10000) {
        return (views / 10000).toFixed(1) + '万';
    } else if (views >= 1000) {
        return (views / 1000).toFixed(1) + 'k';
    }
    return views.toString();
}

function navigateToVideoDetail(videoId) {
    window.location.href = `video-detail.html?id=${videoId}`;
}

// ============================================
// 平滑滚动到锚点
// ============================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80; // 减去导航栏高度
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// ============================================
// 图片懒加载（可选功能）
// ============================================

if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ============================================
// 控制台欢迎信息
// ============================================

console.log('%c体操舞蹈教学视频库', 'font-size: 24px; font-weight: bold; color: #6366f1;');
console.log('%c欢迎访问我们的视频教学平台！', 'font-size: 14px; color: #64748b;');

// ============================================
// 用户功能 - localStorage管理
// ============================================

const STORAGE_KEYS = {
    FAVORITES: 'dance_video_favorites',
    HISTORY: 'dance_video_history',
    LEARNED: 'dance_video_learned'
};

// 获取收藏列表
function getFavorites() {
    const favorites = localStorage.getItem(STORAGE_KEYS.FAVORITES);
    return favorites ? JSON.parse(favorites) : [];
}

// 保存收藏列表
function saveFavorites(favorites) {
    localStorage.setItem(STORAGE_KEYS.FAVORITES, JSON.stringify(favorites));
    updateFavoritesCount();
}

// 切换收藏状态
function toggleFavorite(videoId) {
    let favorites = getFavorites();
    const index = favorites.indexOf(videoId);
    
    if (index > -1) {
        favorites.splice(index, 1);
    } else {
        favorites.push(videoId);
    }
    
    saveFavorites(favorites);
    return index === -1; // 返回true表示添加收藏，false表示取消收藏
}

// 检查是否已收藏
function isFavorite(videoId) {
    const favorites = getFavorites();
    return favorites.includes(videoId);
}

// 获取播放历史
function getHistory() {
    const history = localStorage.getItem(STORAGE_KEYS.HISTORY);
    return history ? JSON.parse(history) : [];
}

// 保存播放历史
function saveHistory(history) {
    localStorage.setItem(STORAGE_KEYS.HISTORY, JSON.stringify(history));
}

// 添加到播放历史
function addToHistory(videoId) {
    let history = getHistory();
    
    // 移除已存在的记录（如果有的话）
    history = history.filter(id => id !== videoId);
    
    // 添加到开头
    history.unshift(videoId);
    
    // 只保留最近10个
    if (history.length > 10) {
        history = history.slice(0, 10);
    }
    
    saveHistory(history);
}

// 清除播放历史
function clearHistory() {
    localStorage.removeItem(STORAGE_KEYS.HISTORY);
}

// 获取已学习列表
function getLearnedVideos() {
    const learned = localStorage.getItem(STORAGE_KEYS.LEARNED);
    return learned ? JSON.parse(learned) : [];
}

// 保存已学习列表
function saveLearnedVideos(learned) {
    localStorage.setItem(STORAGE_KEYS.LEARNED, JSON.stringify(learned));
}

// 切换已学习状态
function toggleLearned(videoId) {
    let learned = getLearnedVideos();
    const index = learned.indexOf(videoId);
    
    if (index > -1) {
        learned.splice(index, 1);
    } else {
        learned.push(videoId);
    }
    
    saveLearnedVideos(learned);
    return index === -1;
}

// 检查是否已学习
function isLearned(videoId) {
    const learned = getLearnedVideos();
    return learned.includes(videoId);
}

// 更新导航栏收藏数量
function updateFavoritesCount() {
    const favoritesCount = document.getElementById('favoritesCount');
    if (favoritesCount) {
        const count = getFavorites().length;
        favoritesCount.textContent = count;
        favoritesCount.style.display = count > 0 ? 'flex' : 'none';
    }
}

// ============================================
// 用户功能 - 视频卡片更新
// ============================================

// 更新后的createVideoCard函数，添加收藏按钮
function createVideoCard(video) {
    const difficultyClass = `difficulty-${video.difficulty}`;
    const isFav = isFavorite(video.id);
    const isLearnedVideo = isLearned(video.id);
    
    return `
        <div class="video-card fade-in" data-id="${video.id}">
            <div class="video-thumbnail">
                <img src="${video.thumbnail}" alt="${video.title}" loading="lazy">
                <span class="video-duration">${video.duration}</span>
                <div class="video-card-actions">
                    <button class="video-action-btn favorite-btn ${isFav ? 'active' : ''}" 
                            data-video-id="${video.id}" 
                            aria-label="${isFav ? '取消收藏' : '添加收藏'}"
                            onclick="event.stopPropagation(); handleFavoriteClick(${video.id}, this);">
                        <svg viewBox="0 0 24 24" fill="${isFav ? '#ef4444' : 'none'}" stroke="currentColor" stroke-width="2">
                            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path>
                        </svg>
                    </button>
                </div>
            </div>
            <div class="video-content">
                <h3 class="video-title">${video.title}</h3>
                <div class="video-instructor">
                    <svg style="width: 16px; height: 16px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                    ${video.instructor}
                </div>
                <div class="video-meta">
                    <span class="video-difficulty ${difficultyClass}">${video.difficultyText}</span>
                    <span class="video-views">${formatViews(video.views)} 观看</span>
                    ${isLearnedVideo ? `
                        <span class="learned-badge">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M9 12l2 2 4-4"></path>
                                <circle cx="12" cy="12" r="10"></circle>
                            </svg>
                            已学习
                        </span>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
}

// 处理收藏按钮点击
function handleFavoriteClick(videoId, button) {
    const isAdded = toggleFavorite(videoId);
    
    if (isAdded) {
        button.classList.add('active');
        button.setAttribute('aria-label', '取消收藏');
        button.querySelector('svg').setAttribute('fill', '#ef4444');
    } else {
        button.classList.remove('active');
        button.setAttribute('aria-label', '添加收藏');
        button.querySelector('svg').setAttribute('fill', 'none');
    }
}

// ============================================
// 用户功能 - 视频详情页更新
// ============================================

function renderVideoDetail(video) {
    // 更新标题
    const titleElement = document.querySelector('.video-detail-title');
    if (titleElement) {
        titleElement.textContent = video.title;
    }
    
    // 更新元数据
    const instructorElement = document.querySelector('.meta-instructor');
    if (instructorElement) {
        instructorElement.innerHTML = `
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
            ${video.instructor}
        `;
    }
    
    const durationElement = document.querySelector('.meta-duration');
    if (durationElement) {
        durationElement.innerHTML = `
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            ${video.duration}
        `;
    }
    
    const difficultyElement = document.querySelector('.meta-difficulty');
    if (difficultyElement) {
        const difficultyClass = `difficulty-${video.difficulty}`;
        difficultyElement.innerHTML = `
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
            <span class="video-difficulty ${difficultyClass}">${video.difficultyText}</span>
        `;
    }
    
    const viewsElement = document.querySelector('.meta-views');
    if (viewsElement) {
        viewsElement.innerHTML = `
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
            </svg>
            ${formatViews(video.views)} 次观看
        `;
    }
    
    // 更新描述
    const descriptionElement = document.querySelector('.video-description');
    if (descriptionElement) {
        descriptionElement.textContent = video.description;
    }
    
    // 更新动作要点
    const pointsList = document.querySelector('.points-list');
    if (pointsList) {
        pointsList.innerHTML = video.points.map((point, index) => `
            <div class="point-item">
                <span class="point-number">${index + 1}</span>
                <span class="point-text">${point}</span>
            </div>
        `).join('');
    }
    
    // 添加用户功能按钮
    addUserActionButtons(video);
    
    // 渲染相关推荐视频
    renderRelatedVideos(video);
    
    // 添加到播放历史
    addToHistory(video.id);
}

// 添加用户操作按钮（收藏、已学习）
function addUserActionButtons(video) {
    const videoInfoSection = document.querySelector('.video-info-section');
    if (!videoInfoSection) return;
    
    const isFav = isFavorite(video.id);
    const isLearnedVideo = isLearned(video.id);
    
    // 检查是否已存在操作按钮区域
    let actionsContainer = document.querySelector('.video-detail-actions');
    if (!actionsContainer) {
        actionsContainer = document.createElement('div');
        actionsContainer.className = 'video-detail-actions';
        videoInfoSection.appendChild(actionsContainer);
    }
    
    actionsContainer.innerHTML = `
        <button class="detail-action-btn favorite-btn ${isFav ? 'active' : ''}" 
                data-video-id="${video.id}"
                onclick="handleDetailFavoriteClick(${video.id}, this);">
            <svg viewBox="0 0 24 24" fill="${isFav ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path>
            </svg>
            ${isFav ? '已收藏' : '收藏'}
        </button>
        <button class="detail-action-btn learned-btn ${isLearnedVideo ? 'active' : ''}" 
                data-video-id="${video.id}"
                onclick="handleLearnedClick(${video.id}, this);">
            <svg viewBox="0 0 24 24" fill="${isLearnedVideo ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
                <path d="M9 12l2 2 4-4"></path>
                <circle cx="12" cy="12" r="10"></circle>
            </svg>
            ${isLearnedVideo ? '已学习' : '标记为已学习'}
        </button>
    `;
}

// 处理详情页收藏按钮点击
function handleDetailFavoriteClick(videoId, button) {
    const isAdded = toggleFavorite(videoId);
    
    if (isAdded) {
        button.classList.add('active');
        button.innerHTML = `
            <svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2">
                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path>
            </svg>
            已收藏
        `;
    } else {
        button.classList.remove('active');
        button.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path>
            </svg>
            收藏
        `;
    }
}

// 处理已学习按钮点击
function handleLearnedClick(videoId, button) {
    const isAdded = toggleLearned(videoId);
    
    if (isAdded) {
        button.classList.add('active');
        button.innerHTML = `
            <svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2">
                <path d="M9 12l2 2 4-4"></path>
                <circle cx="12" cy="12" r="10"></circle>
            </svg>
            已学习
        `;
    } else {
        button.classList.remove('active');
        button.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 12l2 2 4-4"></path>
                <circle cx="12" cy="12" r="10"></circle>
            </svg>
            标记为已学习
        `;
    }
}

// ============================================
// 用户功能 - 个人中心页面
// ============================================

function initUserCenter() {
    updateFavoritesCount();
    renderProgressReport();
    renderHistory();
    renderFavorites();
    initClearHistoryButton();
}

// 渲染学习进度报告
function renderProgressReport() {
    const learned = getLearnedVideos();
    const favorites = getFavorites();
    
    // 更新摘要卡片
    const totalLearned = document.getElementById('totalLearned');
    if (totalLearned) {
        totalLearned.textContent = learned.length;
    }
    
    const totalFavorites = document.getElementById('totalFavorites');
    if (totalFavorites) {
        totalFavorites.textContent = favorites.length;
    }
    
    const totalProgress = document.getElementById('totalProgress');
    if (totalProgress) {
        const progress = Math.round((learned.length / videoData.length) * 100);
        totalProgress.textContent = progress + '%';
    }
    
    // 渲染分类进度
    const categoryProgressList = document.getElementById('categoryProgressList');
    if (!categoryProgressList) return;
    
    const categories = ['基础动作', '舞蹈组合', '技巧训练', '表演展示'];
    
    categoryProgressList.innerHTML = categories.map(category => {
        const categoryVideos = videoData.filter(v => v.category === category);
        const categoryLearned = categoryVideos.filter(v => learned.includes(v.id)).length;
        const progress = categoryVideos.length > 0 
            ? Math.round((categoryLearned / categoryVideos.length) * 100) 
            : 0;
        
        return `
            <div class="category-progress-item">
                <div class="category-progress-header">
                    <span class="category-progress-name">${category}</span>
                    <span class="category-progress-text">${categoryLearned}/${categoryVideos.length} (${progress}%)</span>
                </div>
                <div class="category-progress-bar">
                    <div class="category-progress-fill" style="width: ${progress}%"></div>
                </div>
            </div>
        `;
    }).join('');
}

// 渲染播放历史
function renderHistory() {
    const container = document.getElementById('historyVideosGrid');
    if (!container) return;
    
    const history = getHistory();
    
    if (history.length === 0) {
        container.innerHTML = `
            <div class="empty-state" id="historyEmptyState">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <p>暂无播放历史</p>
            </div>
        `;
        return;
    }
    
    const historyVideos = history
        .map(id => videoData.find(v => v.id === id))
        .filter(v => v !== undefined);
    
    container.innerHTML = historyVideos.map(video => createVideoCard(video)).join('');
    
    // 添加点击事件
    const videoCards = container.querySelectorAll('.video-card');
    videoCards.forEach((card, index) => {
        card.addEventListener('click', function() {
            navigateToVideoDetail(historyVideos[index].id);
        });
    });
}

// 渲染收藏视频
function renderFavorites() {
    const container = document.getElementById('favoritesVideosGrid');
    if (!container) return;
    
    const favorites = getFavorites();
    
    if (favorites.length === 0) {
        container.innerHTML = `
            <div class="empty-state" id="favoritesEmptyState">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path>
                </svg>
                <p>暂无收藏视频</p>
            </div>
        `;
        return;
    }
    
    const favoriteVideos = favorites
        .map(id => videoData.find(v => v.id === id))
        .filter(v => v !== undefined);
    
    container.innerHTML = favoriteVideos.map(video => createVideoCard(video)).join('');
    
    // 添加点击事件
    const videoCards = container.querySelectorAll('.video-card');
    videoCards.forEach((card, index) => {
        card.addEventListener('click', function() {
            navigateToVideoDetail(favoriteVideos[index].id);
        });
    });
}

// 初始化清除历史按钮
function initClearHistoryButton() {
    const clearButton = document.getElementById('clearHistoryBtn');
    if (clearButton) {
        clearButton.addEventListener('click', function() {
            if (confirm('确定要清除所有播放历史吗？')) {
                clearHistory();
                renderHistory();
            }
        });
    }
}

// ============================================
// 更新DOM加载事件处理
// ============================================

// 修改原有的DOMContentLoaded事件监听器
document.addEventListener('DOMContentLoaded', function() {
    initNavbar();
    initMobileMenu();
    updateFavoritesCount();
    
    // 根据当前页面初始化相应功能
    const currentPath = window.location.pathname;
    
    if (currentPath.includes('user-center.html')) {
        initUserCenter();
    } else if (currentPath.includes('video-library.html')) {
        initVideoLibrary();
    } else if (currentPath.includes('video-detail.html')) {
        initVideoDetail();
    } else {
        initHomePage();
    }
});
