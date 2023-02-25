from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    hash_key = models.TextField(max_length=100000,null=True,blank=True,default='none')
    login_key = models.CharField(max_length=10000,null=True,blank=True)


class Password (models.Model) :
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_pas')
    name = models.CharField(max_length=100)
    password = models.TextField(max_length=10000)

    def __str__(self) :
        return str(self.user)