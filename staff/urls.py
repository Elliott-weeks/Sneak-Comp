from django.urls import path
from . import views

urlpatterns = [
    path('management', views.staff_portal , name='staff-portal'),
    path('download/comp/<competition_id>', views.get_comp_excel , name='comp-download')
    
]
