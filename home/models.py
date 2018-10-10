from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    is_campuspartner = models.BooleanField(default=False)
    is_communitypartner =models.BooleanField(default=False)


class Contact(models.Model):
    contacttype_choices = (
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
        ('Other' ,'Other')
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    work_phone= models.CharField(max_length=10,  validators=[MinLengthValidator(10)], blank=True)
    cell_phone= models.CharField(max_length=10, validators=[MinLengthValidator(10)], unique=True, blank=True)
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
    description = models.TextField()

    def __str__(self):
        return str(self.mission_name)



