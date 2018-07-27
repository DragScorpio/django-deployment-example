from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
    #we do the following in order to add two extra attributes: "extend the default User model!!"
    user = models.OneToOneField(User, on_delete=models.CASCADE) #this is adding additional information that the default User class doesn't have!!
    #anything that is related to ForeignKey should have one_delete field!!

    #additional
    portfolio_site = models.URLField(blank=True)

    #dealing with images!! First thing first, install the pillow lib!!!    pip install pillow
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username #print the default attribute "username" of User class
