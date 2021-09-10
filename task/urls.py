from django.urls import path
from . import views

urlpatterns = [
    path('handle_order_id_email', views.handle_order_id_email, name='order-email-handler'),
    
    
]
