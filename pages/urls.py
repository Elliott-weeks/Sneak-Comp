from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faq', views.faq , name='faq'),
    path('how-to-play', views.how_to_play, name="how-to-play"),
    path('contact-us', views.contact_us, name="contact-us"),
    path('free-postal-entry', views.postal_entry, name="free-postal-entry")
    
]
