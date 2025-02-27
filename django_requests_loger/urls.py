from django.urls import path

from . import views

urlpatterns = [
    path('request-logs/', views.request_logs_view, name='request_logs'),
    path('request-logs/<int:log_id>/', views.request_log_detail_view, name='request_log_detail'),
    path('get_logs/', views.get_logs, name='get_logs'),
    path('fetch-latest-logs/', views.fetch_latest_logs, name='fetch_latest_logs'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
