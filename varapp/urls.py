from django.urls import path
from varapp import views

urlpatterns = [

    path('', views.index, name='homepage'),

    path('process/<file_processing_code>',
         views.process_pdf, name='processed_pdf'),

    path('download/<file_processing_code>',
         views.download, name='download_csv')

]
