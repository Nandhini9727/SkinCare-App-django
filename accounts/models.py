from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager

# Create your models here.
"""Need to extend two classes because Django has two classes for users.
   One is the User model and the other is the UserManager.
   MyAccountManager class does NOT have any field names, rather it has two methods.
   One method is used to create regular users, the other method is used to create superusers. 
   These methods are called when we use commands like python manage.py createsuperuser."""

class MyAccountManager(BaseUserManager): # UserManager class
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        user = self.model( # model here refers to BaseUserManager class
            email = self.normalize_email(email), # Normalize the email address by lowercasing the domain part of it.
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password) # inbuilt function to set password
        user.save(using=self._db) # it is going to save user details
        return user
    
    def create_superuser(self,first_name,last_name,username,email,password=None):
        user = self.create_user( # passing the paramter to create_user function
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password,
        )
        # setting all the permission to super user
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

        

class Account(AbstractBaseUser): # User model class
    # following are the list of feilds in the model
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    username = models.CharField(max_length=50,unique=True)
    phone_number = models.CharField(max_length=50)

    #required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' #A string describing the name of the field on the user model that is used as the unique identifier. This will usually be a username of some kind, but it can also be an email address, or any other unique identifier. 
    # USERNAME_FIELD is automatically a required field. other fields that is needed to be required is given in REQUIRED_FIELDS
    REQUIRED_FIELDS = ['username','first_name','last_name'] #A list of the field names that will be prompted for when creating a user via the createsuperuser management command.

    objects = MyAccountManager() # this is inform Account class that we are using MyAccountManager for all these operations

    def __str__(self):
        return self.email # when we return account object in admin panel template the name of the object is email
    
    def has_perm(self, perm, obj=None): # to check if a user has permission
        return self.is_admin # if user is admin then the user has all the permission

    def has_module_perms(self,add_label): # module permissions for user will always be true
        return True