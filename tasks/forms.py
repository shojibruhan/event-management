from django import forms
from tasks.models import Event, EventDetails, Participant, Category

class EventForm(forms.Form):
    title= forms.CharField()
    description= forms.CharField(widget= forms.Textarea, label= "Event Description")
    due_date= forms.DateTimeField(widget= forms.SelectDateWidget, label="Due Date")
    participant= forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EventModelForm(forms.ModelForm):
    class Meta:
        model= Event
        # fields= '__all__'
        fields= ['name', 'description', 'schedule', 'location']