from django.db import models
from django.contrib.auth.models import User
from users.forms import EditProfileForm
class UserProfile(models.Model):
    user= models.OneToOneField(User,
                               on_delete=models.CASCADE,
                               related_name='userprofile',
                               primary_key=True)
    profile_image=models.ImageField(upload_to='profile_image', blank= True)
    bio= models.TextField(blank=True)


    def __str__(self):
        return self.user.username
    
