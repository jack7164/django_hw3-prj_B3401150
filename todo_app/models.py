from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=200, verbose_name="任務名稱")
    content = models.TextField(blank=True, null=True, verbose_name="詳細內容")
    is_completed = models.BooleanField(default=False, verbose_name="是否完成")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    
    # 【V2 新增】截止日期欄位 (設定 null=True, blank=True 讓舊資料不會報錯)
    deadline = models.DateTimeField(verbose_name="截止時間", null=True, blank=True)
    # 【V2 新增】建立外鍵 (ForeignKey) 關聯，將任務綁定至特定使用者
    # on_delete=models.CASCADE：當該名使用者被刪除時，他所建立的所有任務也會連帶一併刪除
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="所屬使用者")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title