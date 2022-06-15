"""Database models"""

from django.db import models
from django.contrib.auth.models import(AbstractBaseUser,BaseUserManager,PermissionsMixin)


#Create user manager
class UserManager(BaseUserManager):
    """Manager for User"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        #make sure email add. is inputed
        if not email:
            raise ValueError("User must have an email")
        #than proceed to create user
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        #above also encrypt the password
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):

        user = self.create_user(email, password)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user




class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    follower = models.CharField(max_length=255)
    memberType = models.IntegerField(blank=True, null=True)

    objects = UserManager()

    #reset the orignal dejango auth. from name to email
    USERNAME_FIELD = "email"


