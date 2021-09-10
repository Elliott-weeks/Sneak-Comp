from django.urls import path
from .views import capture,create


urlpatterns = [
    path('create', create, name="paypal-create"),
    path('<order_id>/capture/<cart_id>', capture, name="paypal-capture"),
    
]
