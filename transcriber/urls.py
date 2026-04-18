from django.urls import path
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
]
