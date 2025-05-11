// static/js/music-player.js
class MusicPlayer {
    static instance = null;

    constructor() {
        if (MusicPlayer.instance) {
            return MusicPlayer.instance;
        }
        MusicPlayer.instance = this;

        // 初始化音频对象
        this.audio = new Audio();
        this.audio.preload = 'auto';
        
        // 设置默认音量为100%
        this.audio.volume = 1.0;
        
        // 基础状态
        this.playlist = [];
        this.currentTrack = 0;
        this.isPlaying = false;
        this.isMinimized = false;
        this.isDragging = false;
        this.isVolumeSliding = false;

        // 绑定方法到实例
        this.handleVisibilityChange = this.handleVisibilityChange.bind(this);
        this.handleBeforeUnload = this.handleBeforeUnload.bind(this);
        this.handlePageShow = this.handlePageShow.bind(this);
        
        // 初始化节流函数
        this.throttledSaveState = this.throttle(this.saveState.bind(this), 1000);
        
        this.initialize();
    }

    async initialize() {
        try {
            await this.cacheElements();
            this.bindEvents();
            await this.loadPlaylist();
            
            // 确保音量为100%并更新UI
            this.audio.volume = 1.0;
            
            // 在执行restoreState之前确保UI已经更新为100%
            this.updateVolumeUI(100);
            
            await this.restoreState();
            
            // 如果restoreState没有设置音量，确保仍然是100%
            if (this.audio.volume < 0.98) {
                this.audio.volume = 1.0;
                this.updateVolumeUI(100);
            }
            
            // 注册页面生命周期事件
            document.addEventListener('visibilitychange', this.handleVisibilityChange);
            window.addEventListener('beforeunload', this.handleBeforeUnload);
            window.addEventListener('pageshow', this.handlePageShow);
            
            // 设置音频事件
            this.audio.addEventListener('play', () => this.updatePlayState(true));
            this.audio.addEventListener('pause', () => this.updatePlayState(false));
            this.audio.addEventListener('ended', () => this.handleTrackEnd());
            this.audio.addEventListener('volumechange', () => {
                this.updateVolumeUI(this.audio.volume * 100);
                this.updateVolumeIcon();
            });
            
            // 性能优化：使用节流进行状态保存
            this.throttledSaveState = this.throttle(this.saveState.bind(this), 1000);
        } catch (error) {
            console.error('初始化播放器失败:', error);
        }
    }

    // 节流函数
    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }

    handleVisibilityChange() {
        if (document.hidden) {
            this.saveState();
        }
    }

    handleBeforeUnload() {
        this.saveState();
    }

    handlePageShow(e) {
        if (e.persisted) {
            this.restoreState();
        }
    }

    handleTrackEnd() {
        this.nextTrack();
    }

    updatePlayState(isPlaying) {
        this.isPlaying = isPlaying;
        if (this.elements.playPause) {
            this.elements.playPause.innerHTML = isPlaying ? 
                '<i class="fas fa-pause"></i>' : 
                '<i class="fas fa-play"></i>';
        }
        this.throttledSaveState();
    }

    async restoreState() {
        try {
            // 优先从 sessionStorage 恢复完整状态
            const sessionState = JSON.parse(sessionStorage.getItem('musicPlayerState'));
            // 如果没有 sessionStorage 状态，尝试从 localStorage 恢复
            const localState = JSON.parse(localStorage.getItem('musicPlayerState'));
            
            const state = sessionState || localState;
            const hasValidState = state && typeof state === 'object';

            // 恢复基本状态
            this.currentTrack = hasValidState ? (state.currentTrack || 0) : 0;
            this.isPlaying = hasValidState ? (state.isPlaying || false) : false;
            this.isMinimized = hasValidState ? (state.isMinimized || false) : false;

            // 恢复音频状态
            if (hasValidState && state.currentTime) {
                this.audio.currentTime = state.currentTime;
            }

            // 恢复音量，如果没有恢复值则保持100%
            if (hasValidState && state.volume !== undefined) {
                this.audio.volume = state.volume;
                this.updateVolumeUI(state.volume * 100);
            } else {
                // 确保默认为100%音量
                this.audio.volume = 1.0;
                this.updateVolumeUI(100);
                console.log('设置默认音量为100%');
            }

            // 恢复最小化状态
            if (this.isMinimized && this.elements.musicPlayer) {
                this.elements.musicPlayer.classList.add('minimized');
                const icon = this.elements.minimizeBtn?.querySelector('i');
                if (icon) {
                    icon.className = 'fas fa-chevron-up';
                }
            }

            // 恢复位置（仅从sessionStorage）
            if (sessionState?.position && this.elements.musicPlayer) {
                const { x, y } = sessionState.position;
                const maxX = window.innerWidth - this.elements.musicPlayer.offsetWidth;
                const maxY = window.innerHeight - this.elements.musicPlayer.offsetHeight;
                const boundedX = Math.max(0, Math.min(x, maxX));
                const boundedY = Math.max(0, Math.min(y, maxY));
                
                this.elements.musicPlayer.style.left = `${boundedX}px`;
                this.elements.musicPlayer.style.top = `${boundedY}px`;
                this.elements.musicPlayer.style.right = 'auto';
                this.elements.musicPlayer.style.bottom = 'auto';
            } else if (this.elements.musicPlayer) {
                this.elements.musicPlayer.style.left = `${window.innerWidth - 330}px`;
                this.elements.musicPlayer.style.top = '30px';
                this.elements.musicPlayer.style.right = 'auto';
                this.elements.musicPlayer.style.bottom = 'auto';
            }

            // 加载并播放音乐
            await this.loadTrack(this.currentTrack);
            if (this.isPlaying) {
                try {
                    await this.audio.play();
                } catch (error) {
                    console.warn('自动播放失败:', error);
                    this.isPlaying = false;
                }
            }
        } catch (error) {
            console.error('恢复状态失败:', error);
            // 出错时确保音量为100%
            this.audio.volume = 1.0;
            this.updateVolumeUI(100);
        }
    }

    saveState() {
        try {
            const state = {
                currentTrack: this.currentTrack,
                isPlaying: this.isPlaying,
                isMinimized: this.isMinimized,
                currentTime: this.audio.currentTime,
                volume: this.audio.volume,
                position: this.elements.musicPlayer ? {
                    x: parseInt(this.elements.musicPlayer.style.left) || window.innerWidth - 330,
                    y: parseInt(this.elements.musicPlayer.style.top) || 30
                } : null
            };
            // 同时保存到 sessionStorage 和 localStorage
            sessionStorage.setItem('musicPlayerState', JSON.stringify(state));
            this.saveToLocalStorage();
        } catch (error) {
            console.error('保存状态失败:', error);
        }
    }

    saveToLocalStorage() {
        try {
            const state = {
                currentTrack: this.currentTrack,
                isPlaying: this.isPlaying,
                currentTime: this.audio.currentTime,
                volume: this.audio.volume
            };
            localStorage.setItem('musicPlayerState', JSON.stringify(state));
        } catch (error) {
            console.error('保存到localStorage失败:', error);
        }
    }

    async cacheElements() {
        // 等待DOM加载完成
        if (document.readyState !== 'complete') {
            await new Promise(resolve => {
                window.addEventListener('load', resolve);
            });
        }

        this.elements = {
            playPause: document.getElementById('playPause'),
            prevTrack: document.getElementById('prevTrack'),
            nextTrack: document.getElementById('nextTrack'),
            songTitle: document.getElementById('songTitle'),
            progressBar: document.querySelector('.music-progress-bar'),
            progressContainer: document.querySelector('.music-progress'),
            progressHandle: document.querySelector('.progress-handle'),
            currentTime: document.getElementById('currentTime'),
            duration: document.getElementById('duration'),
            volumeSliderFill: document.querySelector('.volume-slider-fill'),
            volumeSliderContainer: document.querySelector('.volume-slider-container'),
            volumeHandle: document.querySelector('.volume-handle'),
            volumeBtn: document.querySelector('.volume-btn'),
            volumeIcon: document.querySelector('.volume-btn i'),
            minimizeBtn: document.querySelector('.minimize-btn'),
            musicPlayer: document.querySelector('.music-player'),
            playerHeader: document.querySelector('.music-player-header')
        };

        // 检查元素是否都存在
        Object.entries(this.elements).forEach(([key, element]) => {
            if (!element) {
                console.error(`找不到元素: ${key}`);
            }
        });
    }

    async loadPlaylist() {
        try {
            console.log('开始加载音乐列表...');
            
            // 从API获取音乐列表
            try {
                const response = await fetch('/api/music/');
                if (!response.ok) {
                    throw new Error(`API请求失败: ${response.status}`);
                }
                
                const result = await response.json();
                if (result.status === 'success' && Array.isArray(result.data)) {
                    this.playlist = result.data.map(item => ({
                        id: item.id,
                        title: item.title,
                        url: item.audio_file,
                        cover: '/static/img/default-cover.jpg'
                    }));
                    console.log('从API加载的播放列表:', this.playlist);
                } else {
                    throw new Error('API返回格式错误');
                }
            } catch (apiError) {
                console.error('API加载失败，回退到静态列表:', apiError);
                // 回退到静态播放列表
                this.playlist = [
                    {
                        id: 1,
                        title: 'DJ睿 - 别叫我达芬奇',
                        url: '/static/music/DJ睿 - 别叫我达芬奇 (DJ睿 remix).ogg',
                        cover: '/static/img/default-cover.jpg'
                    },
                    {
                        id: 2,
                        title: 'Seven but you\'re in a bathroom at a party',
                        url: '/static/music/TommyMuzzic _ ZeddMusique - Seven but you\'re in a bathroom at a party.ogg',
                        cover: '/static/img/default-cover.jpg'
                    },
                    {
                        id: 3,
                        title: '高桥千春 - 为什么不回消息',
                        url: '/static/music/高桥千春 - 为什么不回消息.ogg',
                        cover: '/static/img/default-cover.jpg'
                    },
                    {
                        id: 4,
                        title: '精彩轩迪 - 慢慢',
                        url: '/static/music/精彩轩迪 - 慢慢.ogg',
                        cover: '/static/img/default-cover.jpg'
                    },
                    {
                        id: 5,
                        title: '洛天依 - 又见·明月光',
                        url: '/static/music/洛天依 - 又见·明月光 (2024花好月圆会·中秋漫游夜现场).ogg',
                        cover: '/static/img/default-cover.jpg'
                    },
                    {
                        id: 6,
                        title: 'Music 1',
                        url: '/static/music/music1.mp3',
                        cover: '/static/img/default-cover.jpg'
                    },
                    {
                        id: 7,
                        title: '天府事变 - 雾都啊雾都',
                        url: '/static/music/天府事变 - 雾都啊雾都.ogg',
                        cover: '/static/img/default-cover.jpg'
                    },
                    {
                        id: 8,
                        title: '恰见明月栖山 - 三葉のテーマ (钢琴版)',
                        url: '/static/music/恰见明月栖山 - 三葉のテーマ (钢琴版).ogg',
                        cover: '/static/img/default-cover.jpg'
                    },
                    {
                        id: 9,
                        title: '音乐吧 - 无人之岛 (钢琴版)',
                        url: '/static/music/音乐吧 - 无人之岛 (钢琴版).ogg',
                        cover: '/static/img/default-cover.jpg'
                    }
                ];
            }

            if (this.playlist.length === 0) {
                console.warn('播放列表为空');
                throw new Error('没有找到音乐文件');
            }

            // 更新歌曲标题显示
            if (this.elements.songTitle) {
                this.elements.songTitle.textContent = this.playlist[this.currentTrack].title;
                console.log('更新歌曲标题:', this.playlist[this.currentTrack].title);
            }
        } catch (error) {
            console.error('音乐列表加载失败:', error);
            console.error('错误详情:', {
                message: error.message,
                stack: error.stack
            });
            this.playlist = [];
            if (this.elements.songTitle) {
                this.elements.songTitle.textContent = '无法加载音乐列表';
            }
            throw error;
        }
    }

    async loadTrack(index) {
        if (!this.playlist.length) {
            console.warn('播放列表为空');
            return;
        }
        
        try {
            const track = this.playlist[index];
            if (!track) {
                console.warn('无效的音轨索引:', index);
                return;
            }

            console.log('正在加载音轨:', track);
            if (this.elements.songTitle) {
                this.elements.songTitle.textContent = track.title;
            }
            
            // 保存当前的播放状态
            const wasPlaying = this.isPlaying;
            
            // 重置进度条为0，提前给用户视觉反馈
            if (this.elements.progressBar) {
                this.elements.progressBar.style.width = '0%';
            }
            if (this.elements.progressHandle) {
                this.elements.progressHandle.style.left = '0%';
            }
            if (this.elements.currentTime) {
                this.elements.currentTime.textContent = '0:00';
            }
            
            // 检查音频文件是否可访问
            try {
                console.log('尝试访问音频文件:', track.url);
                const response = await fetch(track.url, { method: 'HEAD' });
                console.log('音频文件响应状态:', response.status);
                if (!response.ok) {
                    console.error(`无法访问音频文件: ${track.url}, 状态码: ${response.status}`);
                    return;
                }
            } catch (error) {
                console.error('音频文件检查失败:', error);
                return;
            }
            
            // 使用 preload 预加载
            this.audio.preload = 'auto';
            this.audio.src = track.url;
            
            // 添加音频事件监听
            this.audio.onerror = (e) => {
                console.error('音频加载错误:', {
                    error: e,
                    code: this.audio.error ? this.audio.error.code : null,
                    message: this.audio.error ? this.audio.error.message : null
                });
            };
            
            this.audio.onloadeddata = () => {
                console.log('音频数据加载成功');
                
                // 更新总时长显示
                if (this.elements.duration && this.audio.duration) {
                    this.elements.duration.textContent = this.formatTime(this.audio.duration);
                }
                
                // 强制调用一次更新进度条
                this.updateProgress();
                
                // 如果之前在播放，则自动开始播放新的音轨
                if (wasPlaying) {
                    this.audio.play().catch(error => {
                        console.error('自动播放失败:', error);
                    });
                }
            };
            
            await this.audio.load();
            console.log('音频加载完成');
            
            // 保存状态到 localStorage（跨页面持久化）
            this.saveToLocalStorage();
        } catch (error) {
            console.error('加载音轨失败:', error);
        }
    }

    bindEvents() {
        if (!this.elements.playPause) return;

        // 播放控制
        this.elements.playPause.addEventListener('click', () => this.togglePlay());
        this.elements.prevTrack.addEventListener('click', () => this.prevTrack());
        this.elements.nextTrack.addEventListener('click', () => this.nextTrack());
        
        // 进度控制
        this.audio.addEventListener('timeupdate', () => this.updateProgress());
        this.elements.progressContainer.addEventListener('click', (e) => this.setProgress(e));
        this.elements.progressContainer.addEventListener('mousemove', (e) => this.showProgressHandle(e));
        this.elements.progressContainer.addEventListener('mouseleave', () => this.hideProgressHandle());
        
        // 音量控制 - 完全重写
        this.elements.volumeSliderContainer.addEventListener('mousedown', (e) => {
            e.preventDefault(); // 防止选中文本
            
            // 添加激活状态
            this.elements.volumeSliderContainer.classList.add('active');
            this.isVolumeSliding = true;
            
            // 计算并设置新的音量位置
            this.updateVolumeFromMousePosition(e);
            
            // 绑定文档级别的鼠标移动和释放事件
            document.addEventListener('mousemove', this.handleDocumentMouseMove);
            document.addEventListener('mouseup', this.handleDocumentMouseUp);
        });
        
        // 鼠标悬停事件 - 仅显示手柄
        this.elements.volumeSliderContainer.addEventListener('mousemove', (e) => {
            if (!this.isVolumeSliding) {
                const sliderRect = this.elements.volumeSliderContainer.getBoundingClientRect();
                const relativeX = Math.max(0, Math.min(e.clientX - sliderRect.left, sliderRect.width));
                const percent = (relativeX / sliderRect.width) * 100;
                
                if (this.elements.volumeHandle) {
                    this.elements.volumeHandle.style.left = `${percent}%`;
                    this.elements.volumeHandle.style.opacity = '1';
                }
            }
        });
        
        this.elements.volumeSliderContainer.addEventListener('mouseleave', () => {
            if (!this.isVolumeSliding) {
                const currentVolume = this.audio.volume * 100;
                
                if (this.elements.volumeHandle) {
                    this.elements.volumeHandle.style.left = `${currentVolume}%`;
                    this.elements.volumeHandle.style.opacity = '0';
                }
            }
        });
        
        // 文档级别的鼠标事件处理
        this.handleDocumentMouseMove = (e) => {
            if (this.isVolumeSliding) {
                this.updateVolumeFromMousePosition(e);
            }
        };
        
        this.handleDocumentMouseUp = () => {
            if (this.isVolumeSliding) {
                this.isVolumeSliding = false;
                this.elements.volumeSliderContainer.classList.remove('active');
                
                // 清理文档级别的事件监听
                document.removeEventListener('mousemove', this.handleDocumentMouseMove);
                document.removeEventListener('mouseup', this.handleDocumentMouseUp);
                
                // 保存状态
                this.saveState();
            }
        };
        
        // 音量按钮点击事件
        this.elements.volumeBtn.addEventListener('click', () => this.toggleMute());
        
        // 最小化控制
        this.elements.minimizeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleMinimize();
        });
        
        this.elements.playerHeader.addEventListener('click', () => this.toggleMinimize());

        // 拖拽功能
        this.initDragAndDrop();

        // 键盘控制
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && e.target === document.body) {
                e.preventDefault();
                this.togglePlay();
            }
        });
    }

    initDragAndDrop() {
        let startX, startY, initialX, initialY;
        const header = this.elements.playerHeader;
        const player = this.elements.musicPlayer;

        if (!header || !player) {
            console.error('找不到拖拽所需的元素');
            return;
        }

        // 确保播放器有初始位置
        if (!player.style.left && !player.style.top) {
            player.style.left = `${window.innerWidth - 330}px`;
            player.style.top = '30px';
            player.style.right = 'auto';
            player.style.bottom = 'auto';
        }

        const onMouseDown = (e) => {
            // 如果点击的是最小化按钮或音量滑块，不启动拖拽
            if (e.target.closest('.minimize-btn') || e.target.closest('.volume-slider')) return;
            
            e.preventDefault(); // 防止文本选择
            this.isDragging = true;
            player.classList.add('dragging');
            
            // 获取初始位置
            startX = e.clientX;
            startY = e.clientY;
            
            // 获取当前播放器位置
            const rect = player.getBoundingClientRect();
            initialX = rect.left;
            initialY = rect.top;
            
            // 添加移动和释放事件监听
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
        };

        const onMouseMove = (e) => {
            if (!this.isDragging) return;
            
            e.preventDefault();
            
            // 计算移动距离
            const dx = e.clientX - startX;
            const dy = e.clientY - startY;
            
            // 更新位置
            const newX = initialX + dx;
            const newY = initialY + dy;
            
            // 确保不超出视窗范围
            const maxX = window.innerWidth - player.offsetWidth;
            const maxY = window.innerHeight - player.offsetHeight;
            
            const boundedX = Math.max(0, Math.min(newX, maxX));
            const boundedY = Math.max(0, Math.min(newY, maxY));
            
            // 应用新位置
            player.style.left = `${boundedX}px`;
            player.style.top = `${boundedY}px`;
            player.style.right = 'auto';
            player.style.bottom = 'auto';
            
            // 实时保存位置
            this.throttledSaveState();
        };

        const onMouseUp = () => {
            if (!this.isDragging) return;
            
            this.isDragging = false;
            player.classList.remove('dragging');
            
            // 保存新位置
            this.saveState();
            
            // 移除事件监听
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
        };

        // 绑定拖拽开始事件
        header.addEventListener('mousedown', onMouseDown);
    }

    togglePlay() {
        if (this.isPlaying) {
            this.audio.pause();
        } else {
            this.audio.play().catch(error => {
                console.error('播放失败:', error);
                this.isPlaying = false;
                this.updatePlayState(false);
            });
        }
    }

    updateProgress() {
        const { duration, currentTime } = this.audio;
        if (duration) {
            // 计算进度百分比，确保在有效范围内
            const progressPercent = Math.max(0, Math.min((currentTime / duration) * 100, 100));
            
            // 确保初始化时完全设置为0
            if (currentTime === 0) {
                if (this.elements.progressBar) {
                    this.elements.progressBar.style.width = '0%';
                }
                if (this.elements.progressHandle) {
                    this.elements.progressHandle.style.left = '0%';
                }
            } else {
                // 正常更新进度条位置
                if (this.elements.progressBar) {
                    this.elements.progressBar.style.width = `${progressPercent}%`;
                }
                if (this.elements.progressHandle) {
                    this.elements.progressHandle.style.left = `${progressPercent}%`;
                }
            }
            
            // 更新时间显示
            if (this.elements.currentTime) {
                this.elements.currentTime.textContent = this.formatTime(currentTime);
            }
            if (this.elements.duration) {
                this.elements.duration.textContent = this.formatTime(duration);
            }
            
            // 定期保存当前播放时间
            this.saveState();
        } else {
            // 如果没有 duration，则将进度条重置为0
            if (this.elements.progressBar) {
                this.elements.progressBar.style.width = '0%';
            }
            if (this.elements.progressHandle) {
                this.elements.progressHandle.style.left = '0%';
            }
        }
    }

    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    }

    setProgress(e) {
        if (!this.elements.progressContainer) return;
        
        const width = this.elements.progressContainer.clientWidth;
        const rect = this.elements.progressContainer.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const duration = this.audio.duration;
        
        if (duration && width) {
            // 确保点击位置在有效范围内
            const percent = Math.max(0, Math.min(clickX / width, 1));
            this.audio.currentTime = percent * duration;
            
            // 立即更新视觉反馈
            if (this.elements.progressBar) {
                const progressPercent = percent * 100;
                this.elements.progressBar.style.width = `${progressPercent}%`;
            }
            if (this.elements.progressHandle) {
                const progressPercent = percent * 100;
                this.elements.progressHandle.style.left = `${progressPercent}%`;
                this.elements.progressHandle.style.opacity = '1';
            }
        }
    }

    showProgressHandle(e) {
        if (!this.elements.progressContainer || !this.elements.progressHandle) return;
        
        const width = this.elements.progressContainer.clientWidth;
        const rect = this.elements.progressContainer.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const percent = Math.max(0, Math.min(mouseX / width * 100, 100));
        
        this.elements.progressHandle.style.left = `${percent}%`;
        this.elements.progressHandle.style.opacity = '1';
    }

    hideProgressHandle() {
        if (this.elements.progressHandle) {
            this.elements.progressHandle.style.opacity = '0';
        }
    }

    toggleMinimize() {
        this.isMinimized = !this.isMinimized;
        if (this.elements.musicPlayer) {
            this.elements.musicPlayer.classList.toggle('minimized');
            if (this.elements.minimizeBtn) {
                const icon = this.elements.minimizeBtn.querySelector('i');
                if (icon) {
                    icon.className = this.isMinimized ? 'fas fa-chevron-up' : 'fas fa-chevron-down';
                }
            }
            this.saveState();
        }
    }

    updateVolumeIcon() {
        const volume = this.audio.volume;
        const isMuted = this.audio.muted;
        
        if (isMuted || volume === 0) {
            this.elements.volumeIcon.className = 'fas fa-volume-mute';
        } else if (volume < 0.3) {
            this.elements.volumeIcon.className = 'fas fa-volume-off';
        } else if (volume < 0.7) {
            this.elements.volumeIcon.className = 'fas fa-volume-down';
        } else {
            this.elements.volumeIcon.className = 'fas fa-volume-up';
        }
    }

    prevTrack() {
        this.currentTrack--;
        if (this.currentTrack < 0) {
            this.currentTrack = this.playlist.length - 1;
        }
        this.loadTrack(this.currentTrack);
    }

    nextTrack() {
        this.currentTrack++;
        if (this.currentTrack > this.playlist.length - 1) {
            this.currentTrack = 0;
        }
        this.loadTrack(this.currentTrack);
    }

    // 更新音量UI元素 - 修改后的方法
    updateVolumeUI(percent) {
        const limitedPercent = Math.max(0, Math.min(percent, 100));
        
        // 设置填充宽度
        if (this.elements.volumeSliderFill) {
            this.elements.volumeSliderFill.style.width = `${limitedPercent}%`;
            console.log('更新音量填充宽度:', `${limitedPercent}%`);
        }
        
        // 设置手柄位置
        if (this.elements.volumeHandle) {
            this.elements.volumeHandle.style.left = `${limitedPercent}%`;
            console.log('更新音量手柄位置:', `${limitedPercent}%`);
        }
        
        // 更新音量相关类
        this.updateVolumeClasses(limitedPercent);
    }
    
    // 从鼠标位置更新音量 - 修改后的方法
    updateVolumeFromMousePosition(e) {
        const sliderRect = this.elements.volumeSliderContainer.getBoundingClientRect();
        const relativeX = Math.max(0, Math.min(e.clientX - sliderRect.left, sliderRect.width));
        const percent = (relativeX / sliderRect.width) * 100;
        
        console.log('音量更新:', percent);
        
        // 设置音频音量
        this.audio.volume = percent / 100;
        
        // 更新UI元素
        this.updateVolumeUI(percent);
    }
    
    // 更新音量相关类 - 新方法
    updateVolumeClasses(percent) {
        const limitedPercent = Math.max(0, Math.min(percent, 100));
        
        // 当音量为0时，隐藏末端指示器
        if (limitedPercent === 0) {
            this.elements.volumeSliderFill.classList.add('empty');
        } else {
            this.elements.volumeSliderFill.classList.remove('empty');
        }
        
        // 添加特殊类以增强视觉对比
        if (limitedPercent < 20) {
            this.elements.volumeSliderContainer.classList.add('volume-low');
            this.elements.volumeSliderContainer.classList.remove('volume-medium', 'volume-high');
        } else if (limitedPercent < 60) {
            this.elements.volumeSliderContainer.classList.add('volume-medium');
            this.elements.volumeSliderContainer.classList.remove('volume-low', 'volume-high');
        } else {
            this.elements.volumeSliderContainer.classList.add('volume-high');
            this.elements.volumeSliderContainer.classList.remove('volume-low', 'volume-medium');
        }
    }

    toggleMute() {
        this.audio.muted = !this.audio.muted;
        
        // 记住当前音量
        const currentVolume = this.audio.volume * 100;
        
        if (this.audio.muted) {
            this.elements.volumeIcon.className = 'fas fa-volume-mute';
            // 保存原来的音量值但视觉上显示为0
            this.elements.volumeSliderContainer.dataset.previousVolume = currentVolume;
            this.updateVolumeUI(0);
        } else {
            // 恢复原来的音量值
            const originalValue = this.elements.volumeSliderContainer.dataset.previousVolume || 100;
            this.updateVolumeUI(originalValue);
            this.audio.volume = originalValue / 100;
        }
        this.updateVolumeIcon();
    }
}

// 确保只在DOM加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new MusicPlayer());
} else {
    new MusicPlayer();
}