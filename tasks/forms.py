from django import forms
from tasks.models import Event, EventDetails, Category
from django.contrib.auth import get_user_model

User= get_user_model()

class StyleForMixin:
    """Mixin to apply consistent styling to form fields."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styles()

    
    default_classes = "border border-indigo-800 px-2 py-3 mb-5 rounded-md bg-gray-200 w-full shadow-sm focus:border-rose-500 focus:ring-rose-500 text-black"

    def apply_styles(self):
        for field_name, field in self.fields.items():
            placeholder_text = f"Enter {field.label}"

            widget_classes = {
                forms.TextInput: self.default_classes,
                forms.Textarea: self.default_classes,
                forms.EmailInput: self.default_classes,  # Fixed EmailField widget issue
                forms.Select: "border-2 border-indigo-800 mb-2 rounded-lg space-y-2 p-2 text-black",
                forms.SelectDateWidget: "border-2 border-gray-300 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500 p-2 mb-5",
                forms.CheckboxSelectMultiple: "space-y-2",
                forms.PasswordInput: self.default_classes,
                forms.ModelChoiceField: self.default_classes
            }

            for widget_type, css_class in widget_classes.items():
                if isinstance(field.widget, widget_type):
                    field.widget.attrs.update({'class': css_class, 'placeholder': placeholder_text})


class EventModelForm(StyleForMixin, forms.ModelForm):
    """Form for Event model."""
    
    class Meta:
        model = Event
        fields = ['name', 'category', 'description', 'schedule', 'location', 'participant']
        widgets = {
            'category': forms.Select(),
            'participant': forms.CheckboxSelectMultiple(),
            'schedule': forms.SelectDateWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styles()


class EventDetailsModelForm(StyleForMixin, forms.ModelForm):
    """Form for EventDetails model."""

    class Meta:
        model = EventDetails
        fields = ['types', 'asset']
        widgets= {
            'asset': forms.ClearableFileInput()
        }

    

class ParticipantModelForm(StyleForMixin, forms.ModelForm):
    """Form for Participant model."""

    class Meta:
        model = User
        fields = ['username', 'email']

   