"""Database models"""

from email.headerregistry import Address
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.core.validators import RegexValidator  # for phone number

# Recipe
from django.conf import settings

# image
import uuid
import os

# method to define the path where we want to store the image


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)


# For user we are extending the exist functions of django user
# Create user manager
class UserManager(BaseUserManager):
    """Manager for User"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        # make sure email add. is inputed
        if not email:
            raise ValueError("User must have an email")
        # than proceed to create user
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # above also encrypt the password
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
    objects = UserManager()

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    follower = models.CharField(max_length=255, blank=True)
    memberType = models.IntegerField(blank=True, null=True)

    # reset the orignal dejango auth. from name to email
    USERNAME_FIELD = "email"

    gender = models.CharField(max_length=2, default='1')
    inrent = models.BooleanField(default=False)
    occupation = models.CharField(max_length=255, blank=True)
    postlist = models.ForeignKey(
        'blog.userPost', on_delete=models.CASCADE, null=True)
    rpoint = models.IntegerField(default=0)
    buyRecord = models.CharField(max_length=255, blank=True)
    nickName = models.CharField(max_length=255, blank=True)
    phone_regex = RegexValidator(
        regex=r'09\d{8}', message="Phone number must be entered in the format: '09xxxxxxxx'. Up to 10 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=10, blank=True)  # Validators should be a list


""" # Recipe ======Below=======
#

class Recipe(models.Model):
    "Recipe object"
    # below use the ForeignKey allow us to set relationship between this model and another model
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # once the user is deleted from the profile, it's going to delete all recipes
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    # add tags into recipe model
    tags = models.ManyToManyField('Tag')
    # add ingredients into recipe model
    ingredients = models.ManyToManyField('Ingredient')
    # image
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    # return the string representation of the object
    def __str__(self):
        return self.title

# Tag ======Below=======


class Tag(models.Model):
    "Tag for filtering recipes"
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


# Ingredients

class Ingredient(models.Model):
    "Ingredient for recipes"
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name """
