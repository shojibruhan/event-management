from django.contrib import admin
from .models import Category, Event, EventDetails, RSVP

admin.site.register(Category)
admin.site.register(Event)
admin.site.register(EventDetails)
admin.site.register(RSVP)
