# todo_app/urls.py
from django.urls import path
from . import views
# 【V2 新增】匯入內建的 auth views 來處理登入與登出
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.todo_page, name='todo_page'),
    path('add/', views.add_todo_page, name='add_todo_page'),
    path('toggle/<int:pk>/', views.toggle_todo, name='toggle_todo'),
    path('delete/<int:pk>/', views.delete_todo, name='delete_todo'),
    path('edit/<int:pk>/', views.edit_todo_page, name='edit_todo_page'),
    # 【V2 新增】會員系統路由
    path('register/', views.register_page, name='register'),
    # 使用內建 LoginView，並指定樣板名稱
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # 使用內建 LogoutView，登出後自動導回登入頁面
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # RESTful API 路由
    path('api/todos/', views.api_todo_list_create, name='api_todos'),
    path('api/todos/<int:pk>/', views.api_todo_detail, name='api_todo_detail'),
]