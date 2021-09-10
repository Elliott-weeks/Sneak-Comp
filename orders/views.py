from django.shortcuts import render, get_object_or_404, redirect
from competitions.models import Competition
from .models import OrderItem, Order, Payment, Address
from competitions.models import Entrie
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.detail import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
import json
from competitions.tasks import send_email_now
from django.db import connection
from django.conf import settings

from task.http_task_creator import create_task



   


    




@login_required
def add_to_cart(request, competition_id, amount, answer_selection):
    item = get_object_or_404(Competition, pk=competition_id)
    comp = Competition.objects.filter(pk=competition_id)[0]
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists() :
        order = order_qs[0]  
        entries = comp.entries.filter(user=request.user)
        tickets_in_basket = 0

        if order.items.filter(item__pk= item.pk).exists():
            tickets_in_basket = order.items.filter(item__pk= item.pk)[0].quantity
        ticket_count = 0
        for entry in entries:
            ticket_count += entry.number_of_tickets_purchased
            
        number_of_entries_left = comp.ticket_limit - comp.get_total_number_of_entries()
        if(amount + tickets_in_basket > number_of_entries_left or number_of_entries_left < 0): # checks to ensure we have space for more entries
            messages.error(request, "Not enough tickets left in the raffle to complete purchase")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if (ticket_count + tickets_in_basket + amount > 20): # check if current ticket count + current cart amount + amount adding takes you over 20 entries
            user_number_of_entries_left = 20 - ticket_count
            messages.error(request, "You have already purchased " + str(ticket_count) + " tickets so you only "+ str(user_number_of_entries_left) + " remaining." )
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                        
            
        
    else:
        entries = comp.entries.filter(user=request.user)
        ticket_count = 0 
        for entry in entries:
            ticket_count += entry.number_of_tickets_purchased
        number_of_entries_left = comp.ticket_limit - comp.get_total_number_of_entries()
        if(amount > number_of_entries_left or number_of_entries_left < 0): # checks to ensure we have space for more entries
            messages.error(request, "Not enough tickets left in the raffle to complete purchase")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if (ticket_count + amount > 20): # check if current ticket count + current cart amount + amount adding takes you over 20 entries
            user_number_of_entries_left = 20 - ticket_count
            messages.error(request, "You have already purchased " + str(ticket_count) + " tickets so you only "+ str(user_number_of_entries_left) + " remaining." )
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

       







    if order_qs.exists() :
        order = order_qs[0]   
        if  order_qs[0].items != None and order.items.filter(item__pk=item.pk).exists():
            number_of_tickets_in_cart = order.items.filter(item__pk=item.pk)
            if number_of_tickets_in_cart[0].quantity >= 20:
                messages.error(
                    request, "Maximum number of entries per user is 20")
            else:
                # find the order item
                order_item = order.items.filter(
                    item__pk=item.pk, ordered=False)[0]
                # increase the order item count
                order_item.quantity += 1
                # saving the order
                order_item.save()
                messages.info(request, "Added item to the existing tickets")

        else:
            order_date = timezone.now()
            order_item = OrderItem.objects.create(
                item=item, user=request.user, answer=answer_selection, quantity=amount)
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
    else:
        ordered_date = timezone.now()
        
        order = Order.objects.create(
            user=request.user, order_date=ordered_date, is_ordered=False)
        order_item = OrderItem.objects.create(
            item=item, user=request.user, answer=answer_selection, quantity=amount, ordered=False)

        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return redirect("order-summary")


@login_required
def remove_from_cart(request, competition_id):
    item = get_object_or_404(Competition, pk=competition_id)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=competition_id).exists():
            ordered_item = OrderItem.objects.filter(
                item=item, user=request.user,  ordered=False)[0]
            order.items.remove(ordered_item)
            ordered_item.delete()

    return redirect("order-summary")


@login_required
def remove_single_item_from_cart(request, competition_id):
    item = get_object_or_404(Competition, pk=competition_id)
    order_qs = Order.objects.filter(
        user=request.user,
        is_ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("order-summary")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("order-summary")


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            context = {'object': order}
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")
        return render(self.request, 'orders/order_summary.html', context)


def is_db_in_write_mode():
    # check if db is sqlite to support development
    db_backend = settings.DATABASES['default']['ENGINE'].split('.')[-1]
    if(db_backend == "sqlite3"):
        return True

    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_is_in_recovery()")
        row = str(cursor.fetchone())

        if "False" in row:
            return True
    return False


class Checkout(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            if (is_db_in_write_mode() == False): # checks if db is in write mode before the user continues to checkout
                 return HttpResponse("Site is temporaily undergoing maintaince. Please try again later.",status=503)

            order = Order.objects.get(user=self.request.user, is_ordered=False)
            allowCheckout = True
            for item in order.items.all():
                count = 0
                for entry in item.item.entries.all():
                    count =+ entry.number_of_tickets_purchased
                if(count >= item.item.ticket_limit or item.item.state != "published"):
                    messages.error(self.request, "One of the items in your basket has sold out. Please remove - " + item.item.name)
                    return redirect("order-summary")
            context = {'object': order}
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")
        


        return render(self.request, 'orders/checkout.html', context)


def payment_processed(request):
    # parse the json payload
    body = json.loads(request.body)
    # get the order object from db
    order = Order.objects.get(pk=body['cartId'])
    # constants from json payload
    purchase_units = body['purchase_units'][0]
    shipping = purchase_units['shipping']
    # data items to save
    full_name = shipping['name']['full_name']
    address_line_one = shipping['address']['address_line_1']
    postal_code = shipping['address']['postal_code']
    payal_payment_id = body['id']
    payee_email = body['payer']['email_address']
    paypal_payer_id = body['payer']['payer_id']
    currency_code = purchase_units['payments']['captures'][0]['amount']['currency_code']
    value = purchase_units['payments']['captures'][0]['amount']['value']
    status = body['status']

    address_qs = Address.objects.filter(
        user= request.user, address_line_1= address_line_one, postal_code=postal_code
    )
    address = None

    if address_qs.exists():
        address = address_qs[0]
    else:
        address = Address.objects.create(
            user=request.user, address_line_1=address_line_one, postal_code=postal_code)

    payment = Payment.objects.create(user=request.user, address=address, status=status, payee_email=payee_email, paypal_payment_id=payal_payment_id,
                                     paypal_payer_id=paypal_payer_id, value=value, currency_code=currency_code, full_name=full_name)



    order.is_ordered = True
    for item in order.items.all():
        answer = item.answer
        correct_answer = item.item.competition_correct_answer
        valid_entry = answer == correct_answer
        entry = Entrie.objects.create(user=request.user, number_of_tickets_purchased=item.quantity, valid_entry=valid_entry)
        item.item.entries.add(entry)
        item.ordered = True
        item.save()
    order.payment = payment
    order.save()

    for item in order.items.all():
        if len(item.item.entries.all()) >= item.item.ticket_limit:
            item.item.state = "awaiting"
            item.item.save()

    request.session['orderId'] = order.pk
    project = 'foot-competition'
    location = 'europe-west2'
    queue = 'task-queue'
    task_handler_relative_uri = '/tasks/handle_order_id_email' 
    create_task(project, queue, location, {'cartID':order.pk, 'email':request.user.email}, None, task_handler_relative_uri)
    return redirect("payment-success")


def payment_success(request):
    cart_id = request.session['orderId']
    context = {'cart_id': cart_id}
    return render(request, 'orders/success.html', context)





    


