from django.shortcuts import render
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from paypalcheckoutsdk.core import SandboxEnvironment, PayPalHttpClient
from django.conf import settings
from orders.models import Order
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotFound


@login_required
def create(request):
    if request.method == 'GET':
        return HttpResponseNotFound('<h1>Page not found</h1>')
    elif request.method == 'POST':

        order_qs = Order.objects.filter(
            user=request.user,
            is_ordered=False
        )
        if order_qs.exists:
            order = order_qs[0]
            environment = SandboxEnvironment(
                client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_SECRET_ID)
            client = PayPalHttpClient(environment)
            paypalRequest = OrdersCreateRequest()
            paypalRequest.prefer('return=representation')
            paypalRequest.request_body(
                {
                    "intent": "CAPTURE",
                    "purchase_units": [
                        {
                            "amount": {
                                "currency_code": "GBP",
                                "value": str(order.get_total())
                            }
                        }
                    ]
                }
            )
            paypal_response = client.execute(paypalRequest)
            return JsonResponse(paypal_response.result.__dict__['_dict'])
        else:
            messages.error(request, "You do not have an active checkout")
            return redirect("/")


@login_required
def capture(request, order_id, cart_id):
    if request.method == "POST":
        capture_order = OrdersCaptureRequest(order_id)
        environment = SandboxEnvironment(
            client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_SECRET_ID)
        client = PayPalHttpClient(environment)

        response = client.execute(capture_order)
        data = response.result.__dict__['_dict']

        return JsonResponse(data)
    else:
        return JsonResponse({'details': "invalide request"})
