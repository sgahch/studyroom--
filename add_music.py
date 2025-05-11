#!/usr/bin/env python
"""
将静态音乐文件添加到数据库中的脚本。
运行方式：python add_music.py
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyroom.settings')
django.setup()

from django.contrib.auth.models import User
from index.models import BackgroundMusic
from login.models import Students
import glob

def add_music_files():
    """将static/music目录中的音乐文件添加到数据库"""
    
    # 获取第一个用户作为上传者
    try:
        admin_user = User.objects.filter(is_staff=True).first()
        uploader = Students.objects.get(user=admin_user)
    except:
        print("警告: 找不到管理员用户，尝试获取第一个学生用户")
        try:
            uploader = Students.objects.first()
        except:
            print("错误: 无法找到任何用户作为上传者")
            return

    # 获取音乐文件列表
    music_files = glob.glob("static/music/*.mp3") + glob.glob("static/music/*.ogg")
    
    # 获取数据库中已有的音乐文件路径
    existing_paths = set()
    for music in BackgroundMusic.objects.all():
        if hasattr(music.audio_file, 'name'):
            existing_paths.add(music.audio_file.name)
        else:
            existing_paths.add(str(music.audio_file))
    
    print(f"数据库中已有 {len(existing_paths)} 条音乐记录")
    
    added_count = 0
    for music_file in music_files:
        # 从文件路径提取标题
        title = os.path.basename(music_file)
        title = os.path.splitext(title)[0]  # 移除扩展名
        
        # 转换路径为相对于media目录的路径
        # static/music/song.mp3 -> music/song.mp3
        relative_path = music_file.replace("static/", "")
        
        # 检查文件是否已存在数据库中
        if relative_path not in existing_paths:
            try:
                # 创建记录
                BackgroundMusic.objects.create(
                    title=title,
                    audio_file=relative_path,
                    uploader=uploader,
                    is_active=True
                )
                print(f"已添加: {title} (路径: {relative_path})")
                added_count += 1
            except Exception as e:
                print(f"添加 {title} 失败: {str(e)}")
        else:
            print(f"已跳过 (已存在): {title}")
    
    print(f"总共添加了 {added_count} 首新音乐")

if __name__ == "__main__":
    print("开始添加音乐文件到数据库...")
    add_music_files()
    print("完成!") 