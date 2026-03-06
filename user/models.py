from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from api1.models.products import Products
# Create your models here.

class Mybaseuser(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('The email is required')
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.is_active=False
        user.is_staff=False
        user.is_superuser=False
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        
        if not email:
            raise ValueError('email is required')
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.is_active=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    username=None
    email=models.EmailField(unique=True,max_length=200)
    name=models.CharField(default='zaki')
    # is_active = models.BooleanField(default=False)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=Mybaseuser()
   
class Addtocart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product=models.ManyToManyField(Products,related_name='cart_product')
    created_at=models.DateTimeField(default=timezone.now)
    updated_at=models.DateTimeField(default=timezone.now)

