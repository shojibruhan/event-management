from django import template
from datetime import datetime
from django.utils import timezone

register= template.Library()

@register.filter
def humanized_date(value):
    if value:
        today= datetime.now().date()
        value= timezone.localtime(value)

        if value.date() == today:
            return f"Today at {value.strftime('%I:%M %p')}"
        elif value.date() == today.replace(day=today.day - 1):
            return f"Yesterday at {value.strftime('%I:%M %p')}"
        else:
            return value.strftime('%I:%M %p')
    return "No record available"
        

"""
from django import template
from datetime import datetime
from django.utils import timezone

register= template.Library()

@register.filter
def humenized_data(value):
    
    if value:
        today= datetime.now().date()
        value= timezone.localtime(value)


        if value.date() == today:
            return f"Today at {value.strftime('%I: %M %p')}"
        elif value.date() == today.replace(today.day - 1):
            return f"Yesterday at {value.strftime('%I: %M %p')}"
        else:
            return value.strftime('%I: %M %p')
    
    return "No login record available"


"""