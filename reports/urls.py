from django.urls import path
from .views import upload_excel, export_report

urlpatterns = [
    path('upload', upload_excel, name='upload_excel'),
    path('export', export_report, name='export_report'),
]
