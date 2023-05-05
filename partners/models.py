from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from projects.models import AcademicYear
from django.utils import timezone
from simple_history.models import HistoricalRecords


class CommunityPartner(models.Model):
    TRUE_FALSE_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    name = models.CharField(max_length=255, unique=True)
    acronym = models.CharField(max_length=255, blank=True, null=True)
    website_url = models.URLField(max_length=300, blank=True)
    community_type = models.ForeignKey('CommunityType', max_length=50, on_delete=models.SET_NULL, null=True,verbose_name="Community Type")
    k12_level =  models.CharField(max_length=20,null=False, blank=True)
    online_only = models.BooleanField(default=False)
    address_line1 = models.CharField(max_length=1024, blank=True, null=True)
    address_line2 = models.CharField(max_length=1024, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    active = models.BooleanField(default=False)
    partner_status = models.ForeignKey('PartnerStatus', max_length=30, on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name="Community Partner Status")
    weitz_cec_part = models.CharField(max_length=6, choices=TRUE_FALSE_CHOICES, default='No')
    cec_partner_status = models.ForeignKey('CecPartnerStatus',on_delete=models.CASCADE, null=True,blank=True,
                                           verbose_name="Community CEC Partner Status",default=3)
    legislative_district = models.IntegerField(null=True, blank=True)
    median_household_income = models.IntegerField(null=True, blank=True)
    address_update_flag = models.BooleanField(default=False)
    history = HistoricalRecords()

    class Meta:
        ordering = ('name',)

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
    history = HistoricalRecords()


class CommunityType(models.Model):
    community_type = models.CharField(max_length=50,verbose_name="Community Type")
    history = HistoricalRecords()

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
    weitz_cec_part = models.CharField(max_length=6, choices=TRUE_FALSE_CHOICES, default='No')
    cec_partner_status = models.ForeignKey('CecPartnerStatus',on_delete=models.CASCADE, null=True, blank=True, default=3,
                                           verbose_name="Campus CEC Partner Status")
    active = models.BooleanField(default=True)
    partner_status = models.ForeignKey('PartnerStatus', max_length=30, on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name="Campus Partner Status")
    history = HistoricalRecords()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(self.name)


class CampusPartnerUser(models.Model):
    campus_partner = models.ForeignKey('CampusPartner', on_delete=models.CASCADE, null=False,unique=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    history = HistoricalRecords()


class CommunityPartnerUser(models.Model):
    community_partner = models.ForeignKey('CommunityPartner', on_delete=models.CASCADE,
                                           related_name='communitypartner', null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    history = HistoricalRecords()


class CecPartActiveYrs(models.Model):
    SEMESTER = [
        ("", "----------"), ("Fall", "Fall"), ("Spring", "Spring"), ("Summer", "Summer")]
    start_semester = models.CharField(max_length=20, choices=SEMESTER, blank=True)
    start_acad_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=False,
                                        related_name="cec_academic_year1")
    end_semester = models.CharField(max_length=20, choices=SEMESTER, blank=True)
    end_acad_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name="cec_academic_year2")
    comm_partner = models.ForeignKey(CommunityPartner, on_delete=models.CASCADE, null=True, blank=True)
    camp_partner = models.ForeignKey(CampusPartner, on_delete=models.CASCADE, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "CEC Building Partner Active Year"
        verbose_name_plural = "CEC Building Partner Active Year"

# Models below are Partner lookup tables, must have values to insert project data


class PartnerStatus(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Partner Status"
        verbose_name_plural = "Partner Statuses"
            
    
class CecPartnerStatus(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "CEC Partner Status"
        verbose_name_plural = "CEC Partner Statuses"
