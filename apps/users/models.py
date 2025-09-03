from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin , BaseUserManager
from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    
    """
        custom manager for our custom user model
    """
    
    def create_user(self,email,password,first_name,last_name,**kwargs):
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **kwargs
        )
        
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,first_name,last_name,**validated_fields):
        validated_fields.setdefault('is_active',True)
        validated_fields.setdefault('is_staff',True)
        validated_fields.setdefault('is_superuser',True)
        
        return self.create_user(email,password,first_name,last_name,**validated_fields)


class User(AbstractBaseUser,PermissionsMixin):
    
    """
        changing default username field to email field
    """
    
    email = models.EmailField("email",unique=True,null=False,blank=False)
    
    username = models.CharField(max_length=255,blank=True,null=False)
    first_name = models.CharField(max_length=255,blank=False,null=False)
    last_name = models.CharField(max_length=255,blank=False,null=False)
    created_at = models.DateTimeField(auto_now=True,blank=False,null=False)
    
    
    last_login = None # we dont need this field , as it inherits from base user class
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def save(self,*args,**kwargs):
        self.username = self.first_name + " " + self.last_name
        if self.password and not self.password.startswith(('pbkdf2_','bcrypt','argon2')):
            self.password = make_password(self.password)
        super().save(*args,**kwargs)

    def __str__(self) -> str:
        return self.username

