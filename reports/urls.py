from django.urls import path
from .views import upload_excel, export_report, gm_dashboard_api

urlpatterns = [
    path('upload', upload_excel, name='upload_excel'),
    path('export', export_report, name='export_report'),
    path('gm-dashboard', gm_dashboard_api, name='gm_dashboard_api'),
]
