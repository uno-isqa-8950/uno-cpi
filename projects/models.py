from django.utils import timezone
from django.db import models


class Project (models.Model):
    name = models.CharField(max_length=255)
    engagement_type = models.ForeignKey('EngagementType',on_delete=models.CASCADE ,null=True)
    activity_type = models.ForeignKey('ActivityType',on_delete=models.CASCADE ,null=True)
    facilitator = models.CharField(max_length=255,blank=True)
    description = models.TextField()
    semester = models.CharField(max_length=255)
    total_uno_students = models.IntegerField()
    total_uno_hours = models.CharField(max_length=20)
    total_k12_students = models.IntegerField(null=True, blank=False)
    total_k12_hours = models.CharField(max_length=10)
    total_uno_faculty = models.IntegerField(blank=True)
    total_other_community_members = models.IntegerField(null=False, blank=True)
    start_date = models.DateField(default=timezone.now,null=False, blank=True)
    end_date = models.DateField(default=timezone.now,null=False, blank=True)
    other_details = models.CharField(max_length=100,null=False, blank=True)
    outcomes = models.CharField(max_length=100,null=False, blank=True)
    status = models.ForeignKey('Status',on_delete=models.CASCADE,null=True)
    total_economic_impact =models.DecimalField(max_digits=15, decimal_places=4,null=True, blank=True)
    address_line1 = models.CharField(max_length=1024, blank=True)
    address_line2 = models.CharField(max_length=1024, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=25, blank=True)
    state = models.CharField(max_length=15, blank=True)
    zip = models.IntegerField(null=True,blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)


    def __str__(self):
        return str(self.name)


class ProjectMission (models.Model):
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    mission_type = models.CharField(max_length=20)
    mission = models.ForeignKey('home.MissionArea', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.project_name)


    def __str__(self):
        return str(self.mission)


class ProjectCommunityPartner (models.Model):
    project = models.ForeignKey('projects.Project',  on_delete=models.CASCADE)
    community_partner = models.ForeignKey('partners.CommunityPartner', on_delete=models.CASCADE)
    total_hours = models.IntegerField(blank=True,null=True)
    total_people = models.IntegerField(blank=True,null=True)
    wages = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return str(self.project)

    def __str__(self):
        return str(self.community_partner)


class ProjectCampusPartner (models.Model):
    project = models.ForeignKey('projects.Project',  on_delete=models.CASCADE)
    campus_partner = models.ForeignKey('partners.CampusPartner', on_delete=models.CASCADE)
    total_hours = models.IntegerField(blank=True,null=True)
    total_people = models.IntegerField(blank=True,null=True)
    wages = models.IntegerField(blank=True,null=True)


    def __str__(self):
        return str(self.project)


    def __str__(self):
        return str(self.campus_partner)


class Status(models.Model):
    name =models.CharField(max_length=80,unique=True)
    description = models.CharField(max_length=255 , unique=True)

    def __str__(self):
        return str(self.name)


class EngagementType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description =models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class ActivityType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description =models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)