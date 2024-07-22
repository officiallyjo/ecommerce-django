from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

# creating a model for the superadmin
# This class helps us create and manage user accounts, especially our custom superadmin accounts
class MyAccountManager(BaseUserManager):
    # This method helps us create a normal user with the necessary details
    def create_user(self,first_name, last_name,username,email,password =None):
        if not email:
            raise ValueError ('user must have an email address')# Ensures the email is provided
        if not username :
            raise ValueError('user must have a user name ') # Ensures the username is provided
        
        user = self.model(
            email = self.normalize_email(email), # Standardizes the email format
            username = username,
            first_name = first_name,
            last_name = last_name,
        
        )
        user.set_password(password)# Sets the user's password securely
        user.save()  # Saves the user to the database
        return user
    

    # This method helps us create a superuser (an admin with all permissions)
    def create_superuser(self,first_name, last_name,username,email,password):
        
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        
        )
        user.is_admin=True  # Grant admin privileges
        user.is_active=True # Set as active
        user.is_staff=True # Set as staff
        user.is_superadmin=True # Grant superadmin privileges
        user.save(using =self._db) # Saves the superuser to the database with the necessary privileges
        return user 
    
    
# This class defines the structure of our user account in the database
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username  = models.CharField(max_length=50,unique= True)
    email = models.EmailField(max_length =50 ,unique =True)
    phone_number = models.CharField(max_length=50)
    
    # required
    date_joined = models.DateTimeField(auto_now_add =True) # Record the date and time the account was created
    last_login = models.DateTimeField(auto_now_add =True)# Record the last login date and time
    is_admin = models.BooleanField(default=True )# Boolean field to check if the user is an admin
    is_staff = models.BooleanField(default=True )# Boolean field to check if the user is a staff member
    is_active = models.BooleanField(default=True ) # Boolean field to check if the user account is active
    is_superadmin = models.BooleanField(default=True )# Boolean field to check if the user is a superadmin
    
    # part of required models
    # Setting the login field to email
    USERNAME_FIELD ='email'
    # Additional required fields when creating a user
    REQUIRED_FIELDS =['username','first_name','last_name']
    
    # Link the custom manager to this model
    objects = MyAccountManager()
    
    
    # defining mandatory methods 
    # Method to return the email as the string representation of the user
    def __str__(self):
        return self.email
    
    # Method to check if the user has a specific permission
    def has_perm(self, perm, obj=None):
        return self.is_admin

 
    # Method to check if the user has permissions to view a specific app
    def has_module_perms(self, app_label):
        return True
    
    