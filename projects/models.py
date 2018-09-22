from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from django.core.validators import RegexValidator


class Project(models.Model):
    name = models.CharField(max_length=255)
    # engagementType = models.CharField(max_length=40)
    # activityType = models.CharField(max_length=40)
    # campusFacilitator = models.CharField(max_length=20)
    # description = models.TextField()
    # semester = models.CharField(max_length=20)
    # numOfUnoStudents = models.IntegerField(blank=True)
    # unoStudentHours = models.CharField(max_length=20)
    # numOfCommPartnerMembers = models.IntegerField(blank=True)
    # commPartnerHours = models.CharField(max_length=10)
    # startDate = models.DateField(default=timezone.now)
    # endDate = models.DateField(default=timezone.now)
    # details = models.CharField(max_length=100)
    # numOfUnoFaculty = models.IntegerField(blank=True)
    # otherCommPartnerMembers = models.IntegerField(blank=True)
    # outcomes = models.CharField(max_length=100)
    campusPartnerName = models.CharField(max_length=255)
    communityPartnerName = models.CharField(max_length=255)
    mission = models.ForeignKey('home.MissionArea', on_delete=models.CASCADE)

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