from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from tasks.forms import StyleForMixin


class RegisterUserForm(StyleForMixin, forms.ModelForm):
    
    password= forms.CharField(widget= forms.PasswordInput)
    confirm_password= forms.CharField(widget= forms.PasswordInput)
    class Meta:
        model= User
        fields= ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        # errors= []

    def clean_password(self):
        password= self.cleaned_data.get('password')

        if len(password) < 5:
            raise forms.ValidationError('Password must be minimum 5 charecter long')
        
        return password
    
    def clean(self):
        cleaned_data= super().clean()
        password= cleaned_data.get('password')
        confirm_password= cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password didn't match")
        
        print(cleaned_data)
        return cleaned_data
    
    def clean_email(self):
        email= self.cleaned_data.get('email')
        email_exist= User.objects.filter(email= email).exists()

        if email_exist:
            raise forms.ValidationError("E-mail already exists.")
        
        return email


class LogInForm(StyleForMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)