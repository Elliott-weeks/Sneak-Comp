from celery import Celery
from celery import shared_task
from competitions.models import Competition
from orders.models import Order
from datetime import date, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def expire_competitions():
    today = date.today()
    yesterday = today - timedelta(1)
    comps = Competition.objects.all()
    if comps.exists():
        for x in range(len(comps)):
                if yesterday  >= comps[x].competition_end_date and comps[x].state == "published":
                    comps[x].state = "awaiting"
                    comps[x].save()
               
    
    return "complete"
    
def send_email_now(cartId, email):
    order = Order.objects.filter(pk=cartId)
    if order.exists():
        select_order = order[0]
        context = {'order_number': select_order.pk ,"items" : select_order.items.all() , "total": select_order.get_total()}
        msg_html = render_to_string('email/order-conf.html', context )
        send_mail('The sneaker competion order confirmation',"hello",'no-reply@tsc.com',[email],html_message=msg_html)


def send_plain_text_email(subject, message, emails):
    send_mail(subject,message,'no-reply@tsc.com',emails)



