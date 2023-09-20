from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from memberships.models import Membership, UserMembership
import random
import string


class UserAccountManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password=password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)

class User(AbstractUser):
    full_name = models.CharField(max_length=1000)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserAccountManager()

    def profile(self):
        profile = Profile.objects.get(user=self)

    def save(self, *args, **kwargs):
        # Generate a random username
        if not self.username:
            # Extract the first word from full_name and make it lowercase
            first_word = self.full_name.split()[0].lower()

            # Generate three random digits
            random_digits = ''.join(random.choice(string.digits) for _ in range(3))

            # Combine the first word and random digits with an underscore
            self.username = f"{first_word}_{random_digits}"

        super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)