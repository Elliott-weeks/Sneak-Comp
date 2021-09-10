from django.contrib import admin

# Register your models here.

from .models import Competition, Entrie

admin.site.register(Competition)
admin.site.register(Entrie)
