from django import template

from orders.models import Order

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, is_ordered=False)
        if qs.exists() :
            count = 0
            for item in qs[0].items.all():
                count += item.quantity
            return count
    return 0