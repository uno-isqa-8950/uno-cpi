from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from django.core.validators import RegexValidator


class CommunityPartner (models.Model):
    TRUE_FALSE_CHOICES = (
        ('True', 'Yes'),
        ('False', 'No'),
    )
    communityPartnerName = models.CharField(max_length=100)
    website_url = models.TextField()
    college = models.CharField(max_length=50, null=False, blank=True)
    k12_level = models.CharField(max_length=20, null=False, blank=True)
    active = models.BooleanField(default=True)
    weitz_cec_part = models.CharField(max_length=6, choices= TRUE_FALSE_CHOICES, default= False )

    def __str__(self):
        return str(self. communityPartnerName)


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


# class CampusPartnerUser(models.Model):
#     campuspartner = models.ForeignKey('CampusPartner', on_delete=models.CASCADE)
#     user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)


class CampusPartner(models.Model):
    TRUE_FALSE_CHOICES = (
        ('True', 'Yes'),
        ('False', 'No'),
    )
    campus_partner_name = models.CharField(max_length=255)
    college = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    weitz_cec_part = models.CharField(max_length=6, choices= TRUE_FALSE_CHOICES, default=False)

    def __str__(self):
        return str(self.campus_partner_name)


class CampusPartnerUser(models.Model):
    campuspartner = models.ForeignKey('CampusPartner', on_delete=models.CASCADE)
    #communitypartner = models.ForeignKey('CommunityPartner', on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE,)
    #emailid = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null = False)
    #email_id = models.ForeignKey('home.CampusPartnerContact', on_delete=models.CASCADE)


class CommunityPartnerUser(models.Model):
    #campuspartner = models.ForeignKey('CampusPartner', on_delete=models.CASCADE)
    communitypartner = models.ForeignKey('CommunityPartner', on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE,)