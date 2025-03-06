from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import Group, Permission
from tasks.forms import StyleForMixin
from users.models import CustomUser
from django.contrib.auth import get_user_model

User= get_user_model()

class RegisterUserForm(StyleForMixin, forms.ModelForm):
    
    password= forms.CharField(widget= forms.PasswordInput)
    confirm_password= forms.CharField(widget= forms.PasswordInput)
    class Meta:
        model= User
        fields= ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        

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


class AssignRoleForm(StyleForMixin, forms.Form):
    role= forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    )


class CreateGroupForm(StyleForMixin, forms.ModelForm):
    permissions= forms.ModelMultipleChoiceField(
        queryset= Permission.objects.all(),
        widget= forms.CheckboxSelectMultiple,
        required= False,
        label= "Assign Permission"
    )

    class Meta:
        model= Group
        fields= ['name', 'permissions']


class CustomPasswordChangeForm(StyleForMixin, PasswordChangeForm):
    pass

class CustomPasswordResetForm(StyleForMixin, PasswordResetForm):
    pass

class CustomSetPasswordForm(StyleForMixin, SetPasswordForm):
    pass

class EditProfileForm(StyleForMixin, forms.ModelForm):
    class Meta:
        model= CustomUser
        fields= ['first_name', 'last_name', 'email', 'mobile', 'profile_image', 'bio']