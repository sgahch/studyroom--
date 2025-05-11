from django.db import models
from login.models import Students

# Create your models here.

class TodoItem(models.Model):
    """用户待办事项"""
    user = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name='用户', related_name='todos')
    content = models.CharField(max_length=200, verbose_name='内容')
    completed = models.BooleanField(default=False, verbose_name='是否完成')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '待办事项'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.name} - {self.content}"

class BackgroundMusic(models.Model):
    """背景音乐"""
    title = models.CharField(max_length=100, verbose_name='标题')
    audio_file = models.FileField(upload_to='music/', verbose_name='音频文件')
    uploader = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name='上传者')
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')

    class Meta:
        verbose_name = '背景音乐'
        verbose_name_plural = verbose_name
        ordering = ['-upload_time']

    def __str__(self):
        return self.title
