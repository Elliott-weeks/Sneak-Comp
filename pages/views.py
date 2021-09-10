from django.shortcuts import render
from django.http import HttpResponse

from competitions.models import Competition
from competitions.tasks import send_email_now, send_plain_text_email
from .models import HomePageImage
from django.views.decorators.http import require_http_methods
from .forms import ContactUsForm
from django.contrib import messages
from task.http_task_creator import create_task




@require_http_methods(["GET"])
def index(request):
    competion_list = Competition.objects.all()
    home_page_images = HomePageImage.objects.all()

    only_visable_comps = []
    for comp in competion_list:
        if comp.state != "unpublished" and comp.state != "done":
            only_visable_comps.append(comp)

    context = {
        'comps': only_visable_comps,
        'banner':home_page_images
    }
    return render(request, 'pages/index.html', context)

@require_http_methods(["GET"])
def faq(request):
    return render(request, 'pages/faq.html')

@require_http_methods(["GET"])
def how_to_play(request):
    return render(request, 'pages/how_to_play.html')

@require_http_methods(["GET"])
def postal_entry(request):
    return render(request, 'pages/free_postal_entry.html')

@require_http_methods(["GET", "POST"])
def contact_us(request):
    contact_form = ContactUsForm()
    if request.method == "POST":
        contact_form = ContactUsForm(data=request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            email = contact_form.cleaned_data['email']
            phone_number = contact_form.cleaned_data['phone_number']
            message = contact_form.cleaned_data['message']
            to_list =["elliott.weeks99@gmail.com"]
            subject = '%s is requesting help with a query.'%(name)
            content = ' %s,\n %s ,\n %s ,\n %s ,\n  '%(name,email,phone_number,message)
            send_plain_text_email.delay(subject, content, to_list)
            messages.info(request, "Thankyou for your query!! We will get back to you as soon as possible.")
            return render(request, 'pages/contact_us.html', {"form": contact_form})
        else:
            return render(request, 'pages/contact_us.html', {"form": contact_form})
    else:
        return render(request, 'pages/contact_us.html', {"form": contact_form})

