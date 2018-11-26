from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_campuspartner', False)
        extra_fields.setdefault('is_communitypartner', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def create_campuspartner(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_campuspartner') is not True:
            raise ValueError('Campus Partner must have is_campuspartner=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    is_campuspartner = models.BooleanField(default=False)
    is_communitypartner = models.BooleanField(default=False)
    avatar = models.ImageField(default='profile_image/default.jpg', upload_to='profile_image', null=True, blank=True)
    username = None
    email = models.EmailField(('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Contact(models.Model):
    contacttype_choices = (
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
        ('Other' ,'Other')
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    work_phone= models.CharField(max_length=14)
    cell_phone= models.CharField(max_length=14)
    email_id = models.EmailField(unique=True)
    contact_type = models.CharField(max_length=15, choices=contacttype_choices, default='Select')
    community_partner = models.ForeignKey('partners.CommunityPartner', on_delete=models.CASCADE,null=True,blank=True)
    campus_partner = models.ForeignKey('partners.CampusPartner', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.email_id)

    def __str__(self):
        return '%s %s ' % (self.first_name, self.last_name)


class MissionArea (models.Model):
    mission_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.mission_name)


class HouseholdIncome(models.Model):
    id2 = models.IntegerField(null=False, blank=False)
    county = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    median_income = models.IntegerField(null=False, blank=False)
    margin_error = models.IntegerField(null=False, blank=False)
    rank = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return str(self.county)
