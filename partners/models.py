from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils import timezone


class CommunityPartner(models.Model):
    TRUE_FALSE_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    name = models.CharField(max_length=255, unique=True)
    website_url = models.URLField(max_length=300, blank=True)
    community_type = models.ForeignKey('CommunityType', max_length=50, on_delete=models.SET_NULL, null=True,verbose_name="Community Type")
    k12_level =  models.CharField(max_length=20,null=False, blank=True)
    address_line1 = models.CharField(max_length=1024, blank=True)
    address_line2 = models.CharField(max_length=1024, blank=True)
    county = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=25, blank=True)
    state = models.CharField(max_length=15, blank=True)
    zip = models.CharField(max_length=10, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    active = models.BooleanField(default=False)
    weitz_cec_part = models.CharField(max_length=6, choices=TRUE_FALSE_CHOICES, default=False)
    legislative_district = models.IntegerField(null=True, blank=True)
    median_household_income = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class CommunityPartnerMission(models.Model):
    mission_choices = (
        ('Primary', 'Primary'),
        ('Other', 'Other'),
    )
    mission_type = models.CharField(max_length=20, choices=mission_choices, default=False)
    mission_area = models.ForeignKey('home.MissionArea', on_delete=models.CASCADE, related_name='mission_area', null=True)
    community_partner = models.ForeignKey('partners.CommunityPartner', on_delete=models.CASCADE,
                                          related_name='communitypartnermission', null=True)


class CommunityType(models.Model):
    community_type = models.CharField(max_length=50,verbose_name="Community Type")

    def __str__(self):
        return str(self.community_type)


class CampusPartner(models.Model):
    TRUE_FALSE_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    name = models.CharField(max_length=255,unique=True)
    college_name = models.ForeignKey('university.College', on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey('university.Department', on_delete=models.SET_NULL, null=True, blank=True)
    university = models.ForeignKey('university.University', on_delete=models.SET_NULL, null=True,blank=True)
    education_system = models.ForeignKey('university.EducationSystem',on_delete=models.CASCADE, null=True,blank=True)
    weitz_cec_part = models.CharField(max_length=6, choices=TRUE_FALSE_CHOICES, default=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class CampusPartnerUser(models.Model):
    campus_partner = models.ForeignKey('CampusPartner', on_delete=models.CASCADE, null=False,unique=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)


class CommunityPartnerUser(models.Model):
     community_partner = models.ForeignKey('CommunityPartner', on_delete=models.CASCADE,
                                           related_name='communitypartner', null=True)
     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)


