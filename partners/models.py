from django.db import models
# from home.models import *
# from projects.models import Project

from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from django.core.validators import RegexValidator


class CommunityPartner (models.Model):
    TRUE_FALSE_CHOICES = (
        ('True', 'Yes'),
        ('False', 'No'),
    )

    name = models.CharField(max_length= 100)

    website_url = models.TextField()
    college = models.CharField(max_length=50,null=False, blank=True)
    k12_level =  models.CharField(max_length=20,null=False, blank=True)
    active = models.BooleanField(default= True)
    weitz_cec_part = models.CharField(max_length=6 , choices= TRUE_FALSE_CHOICES, default= False )


    def __str__(self):
        return str(self. name)


class CommunityType (models.Model):
    partner_name = models.ForeignKey(CommunityPartner, on_delete=models.CASCADE)
    community_type = models.CharField(max_length=50)

    def __str__(self):
        return str(self.partner_name)


class CommunityPartnerMission (models.Model):
    partner_name = models.ForeignKey(CommunityPartner, on_delete=models.CASCADE)
    mission_type = models.CharField(max_length=20)
    mission_code = models.ForeignKey('home.MissionArea', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.partner_name)


class University (models.Model):
    college = models.CharField(max_length=50)
    department = models.CharField(max_length=30)
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class Course(models.Model):
    prefix = models.CharField(max_length=80)
    number = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    project_id = models.ForeignKey('projects.Project', on_delete=models.CASCADE)


class CampusPartner (models.Model):
    TRUE_FALSE_CHOICES = (
        ('True', 'Yes'),
        ('False', 'No'),
    )
    name = models.CharField(max_length=255)
    department_id = models.ForeignKey('University', on_delete=models.CASCADE)
    weitz_cec_part = models.CharField(max_length=6 , choices= TRUE_FALSE_CHOICES, default= False )

