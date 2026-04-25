from django.urls import path
from . import views
from .views import login_view, input_client, save_history, history, history_detail, delete_history,choose_type

urlpatterns = [
    path('', views.login_view, name='login'),
    path('choose-type/', views.choose_type, name='choose_type'),  # ✅ THIS
    path('input/', views.input_client, name='input_client'),
    path('set-type/<str:tipe>/', views.set_type, name='set_type'),
    path('save-history/', views.save_history, name='save_history'),
    path('history/', views.history, name='history'),
    path('history/<int:id>/', views.history_detail, name='history_detail'),
    path('history/delete/<int:id>/', views.delete_history, name='delete_history'),
    path('history/<int:id>/pdf/', views.download_history_pdf, name='download_history_pdf'),
]