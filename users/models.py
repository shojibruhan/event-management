from django.db import models
from django.contrib.auth.models import AbstractUser, User


'''
class UserProfile(models.Model):
    user= models.OneToOneField(User,
                               on_delete=models.CASCADE,
                               related_name='userprofile',
                               primary_key=True)
    profile_image=models.ImageField(upload_to='profile_image', blank= True)
    bio= models.TextField(blank=True)


    def __str__(self):
        return self.user.username

'''  
class CustomUser(AbstractUser):
    profile_image=models.ImageField(upload_to='profile_image', blank= True, default='profile_image/profile.jpg')
    bio= models.TextField(blank=True)
    mobile= models.CharField(blank=True)


    def __str__(self):
        return self.username