from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from django.core.validators import RegexValidator


class Project (models.Model):
    name = models.CharField(max_length=100)
    engagementType = models.CharField(max_length=20)
    activityType = models.CharField(max_length=20)
    facilitator = models.CharField(max_length=20,blank=True)
    description = models.TextField()
    semester = models.CharField(max_length=20)
    totalNumUnoStudents = models.IntegerField()
    totalUnoHours = models.CharField(max_length=20)
    totalNumK12Students = models.IntegerField()
    totalK12Hours = models.CharField(max_length=10)
    numUnoFacultyStaff = models.IntegerField(blank=True)
    numOtherCommunityMembers =  models.IntegerField(null=False, blank=True)
    startDate = models.DateField(default=timezone.now,null=False, blank=True)
    endDate = models.DateField(default=timezone.now,null=False, blank=True)
    otherDetails = models.CharField(max_length=100,null=False, blank=True)
    outcomes = models.CharField(max_length=100,null=False, blank=True)
    isActive = models.BooleanField()
    totalEconomicImpact =models.DecimalField(max_digits=15, decimal_places=4,null=False, blank=True)
    partners = models.ManyToManyField('partners.CommunityPartner', related_name='p_name')

    def __str__(self):
        return str(self.name)


class ProjectMission (models.Model):
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    mission_type = models.CharField(max_length=20)
    mission_code = models.ForeignKey('home.MissionArea', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.project_name)


class ProjectPartner (models.Model):
    project_id = models.ForeignKey('projects.Project',  on_delete=models.CASCADE)
    partner_id = models.ForeignKey('partners.CommunityPartner', on_delete=models.CASCADE)
    no_hours = models.IntegerField()
    no_people = models.IntegerField()
    partner_type = models.CharField(max_length=30)
    wages = models.IntegerField()