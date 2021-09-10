from django.db import models
from datetime import datetime
from django.conf import settings

# Create your models here.


class Entrie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT)
    number_of_tickets_purchased = models.IntegerField(default=0)
    valid_entry = models.BooleanField(default=False)
    def __str__(self):
        return self.user.email


class Competition(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    size = models.IntegerField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    state_choices = [('unpublished', 'unpublished'),('published', 'published'),('awaiting', 'awaiting'),('done', 'done') ]
    state = models.CharField(default="unpublished", max_length=25,choices=state_choices) # default is unpublished, published, awaiting, done
    ticket_limit = models.IntegerField(default=0)
    entries = models.ManyToManyField(Entrie,  blank=True)
    competition_end_date = models.DateField(blank=False, default=datetime.now)
    competition_question = models.TextField(
        blank=False, default="what is the capital of the uk")
    competition_answers_one = models.CharField(
        max_length=150, blank=False, default="")
    competition_answers_two = models.CharField(
        max_length=150, blank=False, default="")
    competition_answers_three = models.CharField(max_length=150, default="")
    competition_correct_answer = models.IntegerField(default=1)

    def get_total_number_of_entries(self):
        total = 0
        for entry in self.entries.all():
            total += entry.number_of_tickets_purchased
        return total

    def __str__(self):
        return self.name
