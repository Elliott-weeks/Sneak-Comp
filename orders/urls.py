from django.urls import path
from .views import (payment_success,add_to_cart, remove_from_cart, OrderSummaryView, remove_single_item_from_cart, Checkout, payment_processed)

urlpatterns = [
    path('add-to-cart/<int:competition_id>/<int:amount>/<int:answer_selection>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:competition_id>', remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<int:competition_id>', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', Checkout.as_view(), name = "checkout"),
    path('payment-processed/', payment_processed, name = "payment-processed"),
    path('payment-complete',payment_success, name="payment-success" )
    
]
