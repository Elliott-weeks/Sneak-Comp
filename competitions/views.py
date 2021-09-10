from django.shortcuts import render, get_object_or_404

# Create your views here
from .models import Competition


def competition(request, competition_id):
    comp = get_object_or_404(Competition, pk=competition_id)

    context = {
        'competition': comp
    }
   
    return render(request, 'competitions/competition.html', context)
