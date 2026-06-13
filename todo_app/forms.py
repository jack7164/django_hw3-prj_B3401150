# todo_app/forms.py
from django import forms
from django.utils import timezone
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        # 只需要讓使用者填寫標題、內容、截止時間
        fields = ['title', 'content', 'deadline']
        
        # 使用 widgets 替換原生輸入框，套用 Bootstrap 樣式與 HTML5 日期選擇器
        widgets = {
            #attrs：設定 HTML 屬性，這裡我們為標題和內容欄位添加了 Bootstrap 的 form-control 類別
            #並為截止日期欄位指定了 type="datetime-local" 以啟用 HTML5 的日期時間選擇器
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '要做什麼呢？'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '輸入細節？'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    # 【V2 核心評分點】自訂驗證邏輯：截止日期不能設定為過去的時間
    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline:
            now = timezone.now()+timezone.timedelta(minutes=1)  # 設定「現在時間的下一分鐘」作為比較基準，避免使用者選擇到剛好等於現在的時間而被誤判為過去
            # 若截止日期早於現在時間，拋出表單驗證錯誤 (ValidationError)
            if deadline < now:
                raise forms.ValidationError("截止日期不能設定為過去的時間！")
        return deadline