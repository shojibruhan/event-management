from django.contrib import admin
from .models import Category, Event, EventDetails, Participant

admin.site.register(Category)
admin.site.register(Event)
admin.site.register(EventDetails)
admin.site.register(Participant)
