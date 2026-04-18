from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'transcriber'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_image, name='upload'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('reformat/<int:pk>/', views.reformat_text, name='reformat'),
    path('custom-prompt/<int:pk>/', views.process_custom_prompt, name='custom_prompt'),
    path('history/', views.history, name='history'),
    path('delete/<int:pk>/', views.delete_transcription, name='delete'),
    path('api/transcription/<int:pk>/', views.api_transcription, name='api_transcription'),
    path('login/', auth_views.LoginView.as_view(template_name='transcriber/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
