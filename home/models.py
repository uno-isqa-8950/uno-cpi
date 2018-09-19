from django.db import models
from partners.models import CommunityPartner, CommunityType, CommunityPartnerMission, CampusPartner
from projects.models import Project,ProjectMission
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from django.core.validators import RegexValidator


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    workphone= models.CharField(max_length=10,  validators=[MinLengthValidator(10)],
                             help_text="Phone Number should be 10 digits",blank=True)
    cellphone= models.CharField(max_length=10, validators=[MinLengthValidator(10)],
                               help_text="Phone Number should be 10 digits" , unique=True, blank=True)
    contact_type = models.CharField(max_length=15)
    email_id = models.CharField(max_length=254)
    partner_name = models.ForeignKey('partners.CommunityPartner', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.first_name)

    def __str__(self):
        return str(self.last_name)


    def __str__(self):
        return str(self.partner_name)


class MissionArea (models.Model):
    mission_code = models.CharField(max_length=10,default= 0)
    mission_name = models.CharField(max_length=100)
    description = models.TextField()
  #  mission_code = models.ManyToManyField(CommunityPartner , through='CPMission')

    def __str__(self):
        return str(self.mission_name)


class Address(models.Model):
    address_line1 = models.CharField(max_length=1024)
    address_line2 = models.CharField(max_length=1024, blank=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=15)
    Zip = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True)











