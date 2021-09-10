from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from competitions.tasks import send_email_now
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.


@require_http_methods(["POST"])
@csrf_exempt
def handle_order_id_email(request):
    data = json.loads(request.body.decode())
    email = data['email']
    cartID = data['cartID']
    send_email_now(cartID, email)
    return JsonResponse({'message':'success'})




