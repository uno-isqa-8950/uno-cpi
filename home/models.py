from django.db import models
from partners.models import *
from projects.models import Project
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Contact(models.Model):
    contacttype_choices = (('Phone', 'Phone'), ('Email', 'Email'))
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    workphone= models.CharField(max_length=10,  validators=[MinLengthValidator(10)],
                             help_text="Phone Number should be 10 digits",blank=True)
    cellphone= models.CharField(max_length=10, validators=[MinLengthValidator(10)],
                               help_text="Phone Number should be 10 digits" , unique=True, blank=True)
    contact_type = models.CharField(max_length=15, choices=contacttype_choices, default='Select')
    email_id = models.EmailField()
    CommunityPartnerName = models.ForeignKey('partners.CommunityPartner', on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return str(self.email_id)

#    def __str__(self):
#        return str(self.last_name)


#    def __str__(self):
#        return str(self.partner_name)


class CampusPartnerContact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_id = models.EmailField()
    partner_name = models.ForeignKey('partners.CampusPartner', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.first_name)

    def __str__(self):
        return str(self.last_name)

    def __str__(self):
        return str(self.partner_name)


        
class MissionArea (models.Model):
    mission_name = models.CharField(max_length=100)
    description = models.TextField()
 

def __str__(self):
        return str(self.mission_name)



