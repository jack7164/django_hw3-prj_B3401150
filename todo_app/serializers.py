# todo_app/serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title','content', 'is_completed', 'created_at', 'deadline']
    
    def validate_deadline(self, value):
        #負責驗證截止日期
        if value:
            # 加上 1 分鐘的緩衝，避免剛好等於現在時間被誤判
            now = timezone.now() + timezone.timedelta(minutes=1)
            if value < now:
                raise serializers.ValidationError("截止日期不能設定為過去的時間！")
        return value