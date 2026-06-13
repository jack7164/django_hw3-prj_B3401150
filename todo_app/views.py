# todo_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required  # 【V2 新增】登入保護裝飾器
from .models import Todo
from .forms import TodoForm  # 【V2 新增】匯入剛才自訂的 ModelForm
#用於註冊時建立帳號與自動登入
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .serializers import TodoSerializer
import json

# 1. 渲染網頁的 View
@login_required(login_url='/login/')  # 未登入者會被自動導向 /login/
@ensure_csrf_cookie  # 確保前端可以拿到 CSRF Token 用於 API 請求
def todo_page(request):
    todos = Todo.objects.filter(user=request.user)# 只顯示當前登入使用者的任務
    return render(request, 'todo.html', {'todos': todos})

# 2. 新增任務頁面 
@login_required(login_url='/login/')
def add_todo_page(request):
    if request.method == 'POST':
        # 將前端送來的資料丟給 TodoForm 進行驗證
        form = TodoForm(request.POST)
        if form.is_valid():  # 這裡會自動觸發 clean_deadline() 檢查時間
            # 先不要寫入資料庫 (commit=False)，因為要先綁定使用者
            todo = form.save(commit=False)
            todo.user = request.user  # 綁定給當前的登入者
            todo.save()  # 正式寫入
            return redirect('todo_page')
    else:
        form = TodoForm()  # 產生空白表單
        
    # 將 form 物件傳給樣板（若驗證失敗，form 內部會帶有錯誤訊息）
    return render(request, 'add_todo.html', {'form': form})


# 3. 切換狀態 API
def toggle_todo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        todo.is_completed = not todo.is_completed
        todo.save()
        return JsonResponse({'status': 'success', 'is_completed': todo.is_completed})

# 4. 刪除任務 API (新加入)
def delete_todo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        todo.delete()
        return JsonResponse({'status': 'success'})

# 5. 編輯任務頁面 (新加入)
def edit_todo_page(request, pk):
    # 取得要編輯的那筆資料
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # 傳入既有物件 instance=todo 進行更新覆蓋
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_page')
    else: # GET 請求時，將舊資料傳給模板顯示
        form = TodoForm(instance=todo)
        
    
    return render(request, 'edit_todo.html', {'form': form, 'todo': todo})    

# 6. 會員註冊頁面 (V2 新增)
def register_page(request):
    if request.method == 'POST':
        # 使用 Django 內建的註冊表單驗證帳號密碼規則
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # 建立新使用者寫入資料庫
            login(request, user)  # 註冊成功後自動幫使用者登入
            return redirect('todo_page')  # 導向待辦事項首頁
    else:
        form = UserCreationForm()
        
    return render(request, 'register.html', {'form': form})
@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required
def api_todo_list_create(request):
    """API 1：取得待辦清單 (GET) 或 新增待辦事項 (POST)"""
    if request.method == 'GET':
        # 取得登入者的所有任務
        todos = Todo.objects.filter(user=request.user).order_by('-created_at')
        serializer = TodoSerializer(todos, many=True)
        return JsonResponse({'status': 'success', 'data': serializer.data})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')

        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            # 綁定當前登入的使用者並寫入資料庫
            todo = serializer.save(user=request.user)
            return JsonResponse({
                'status': 'success', 
                'message': '任務新增成功！',
                'data': TodoSerializer(todo).data
            }, status=201)
        else:
            return JsonResponse({'status': 'error', 'errors': serializer.errors}, status=400)


@csrf_exempt
@require_http_methods(["DELETE", "PATCH"])
@login_required
def api_todo_detail(request, pk):
    """API 2：刪除 (DELETE) 或 切換狀態 (PATCH) 單一任務"""
    todo = get_object_or_404(Todo, pk=pk, user=request.user)

    if request.method == 'DELETE':
        todo.delete()
        return JsonResponse({'status': 'success', 'message': '任務已刪除'})

    elif request.method == 'PATCH':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')

        # partial=True 允許只更新部分欄位 (例如只傳入 is_completed)
        serializer = TodoSerializer(todo, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': 'success', 'data': serializer.data})
        return JsonResponse({'status': 'error', 'errors': serializer.errors}, status=400)