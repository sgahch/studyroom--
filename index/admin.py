from django.contrib import admin
from .models import TodoItem, BackgroundMusic

# Register your models here.
@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'completed', 'created_at')
    list_filter = ('completed', 'created_at')
    search_fields = ('content',)

@admin.register(BackgroundMusic)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploader', 'upload_time', 'is_active')
    list_filter = ('is_active', 'upload_time')
    search_fields = ('title',)
    
    def save_model(self, request, obj, form, change):
        if not change:  # 只在创建新记录时设置上传者
            obj.uploader = request.user.students
        super().save_model(request, obj, form, change)
