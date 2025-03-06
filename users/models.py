from django.db import models
from django.contrib.auth.models import AbstractUser, User



class CustomUser(AbstractUser):
    profile_image=models.ImageField(upload_to='profile_image', blank= True, default='profile_image/profile.jpg')
    bio= models.TextField(blank=True)
    mobile= models.CharField(blank=True)


    def __str__(self):
        return self.username