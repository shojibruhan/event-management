from django import forms
from tasks.models import Event, EventDetails, Participant, Category



class StyleForMixin:

    default_classes= "border border-indigo-800 px-2 py-3 mb-5 rounded-md bg-gray-200 w-full shadow-sm focus:border-rose-500 focus:ring-rose-500"
    

    def styleWidget(self):
        for field_name, field in self.fields.items():
            placeholder_text= f"Enter {field.label.lower()}"
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': placeholder_text
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': 'space-y-2'
                    
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': placeholder_text
                })
            elif isinstance(field.widget, forms.EmailField):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': placeholder_text
                })
            
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': "border-2 border-gray-300 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500 p-2 mb-5"

                })
           
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'border-2 border-indigo-800 mb-2 rounded-lg space-y-2 p-2',
                    
                })
           
        


class EventModelForm(StyleForMixin, forms.ModelForm):
    class Meta:
        model= Event
        # fields= '__all__'
        fields= ['name', 'category',  'description', 'schedule', 'location', 'participant']

        widgets= {
            'category': forms.Select(),
            'participant': forms.CheckboxSelectMultiple,
            'schedule': forms.SelectDateWidget
        }
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.styleWidget()

class EventDetailsModelForm(StyleForMixin, forms.ModelForm):
    class Meta:
        model= EventDetails
        fields= ['types']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.styleWidget()


class ParticipentModelForm(StyleForMixin, forms.ModelForm):
    class Meta:
        model= Participant
        # fields= '__all__'
        fields= ['name', 'email']

        # widgets= {
        #     'email': forms.EmailField
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.styleWidget()