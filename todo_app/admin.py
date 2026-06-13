# todo_app/admin.py
from django.contrib import admin
from .models import Todo

# 使用裝飾器註冊 Model 至 Admin 後台
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    #自訂列表的「顯示欄位」
    # 在後台任務列表中，同時清楚呈現：標題、所屬使用者、是否完成、截止時間
    list_display = ('title', 'user', 'is_completed', 'deadline',)
    
    #自訂「搜尋功能」
    # 允許管理者在上方搜尋吧直接輸入關鍵字，比對任務標題、詳細內容，甚至所屬使用者的帳號名稱
    search_fields = ('title', 'content', 'user__username')
    
    #自訂「側邊欄過濾功能」
    # 在右側提供快速篩選器，可一鍵篩選出「已完成/未完成」、「特定使用者」或「特定截止日期」的任務
    list_filter = ('is_completed', 'user', 'deadline')
    
    #預設排序方式：依照建立時間由新到舊排序
    ordering = ('-created_at',)
    
    #實用進階設定：允許在後台列表頁面直接勾選/取消「是否完成」，不需點進去詳細頁面
    list_editable = ('is_completed',)