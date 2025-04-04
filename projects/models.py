from django.utils import timezone
from django.db import models
from simple_history.models import HistoricalRecords
from crum import get_current_user
from django.contrib.postgres.fields import ArrayField
from UnoCPI import settings


class Project(models.Model):
    objects = None
    project_choices = (
        ('Event', 'Event'),
        ('Project', 'Project'),
    )
    project_name = models.CharField(max_length=255, unique=True)
    engagement_type = models.ForeignKey('EngagementType', on_delete=models.CASCADE, null=True, blank=True)
    activity_type = models.ForeignKey('ActivityType', on_delete=models.CASCADE, null=True, blank=True)
    facilitator = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    semester = models.CharField(max_length=20, null=True, blank=True)
    end_semester = models.CharField(max_length=20, null=True, blank=True)
    academic_year = models.ForeignKey('AcademicYear', on_delete=models.CASCADE, null=True, blank=True,
                                      related_name="academic_year1")
    end_academic_year = models.ForeignKey('AcademicYear', on_delete=models.CASCADE, null=True, blank=True,
                                          related_name="academic_year2")
    total_uno_students = models.PositiveIntegerField(null=True, default=0)
    total_uno_hours = models.PositiveIntegerField(null=True, default=0)
    k12_flag = models.BooleanField(default=False)
    address_update_flag = models.BooleanField(default=False)
    total_k12_students = models.PositiveIntegerField(null=True, default=0)
    total_k12_hours = models.PositiveIntegerField(null=True, default=0)
    total_uno_faculty = models.PositiveIntegerField(null=True, default=0)
    total_other_community_members = models.PositiveIntegerField(null=True, default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    other_details = models.CharField(max_length=1000, null=True, blank=True)
    outcomes = models.CharField(max_length=100, null=True, blank=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, null=True, blank=True, default=1)
    total_economic_impact = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True, default=0)
    address_line1 = models.CharField(max_length=1024, blank=True, null=True)
    address_line2 = models.CharField(max_length=1024, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    zip = models.CharField(max_length=10, null=True, blank=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    legislative_district = models.IntegerField(null=True, blank=True)
    median_household_income = models.IntegerField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='Projects_created_by')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='Projects_updated_by')
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    campus_lead_staff = ArrayField(base_field=models.CharField(max_length=100), size=10, blank=True, null=True)
    project_type = models.CharField(max_length=20, choices=project_choices, default='Project')
    subcategory = models.ManyToManyField('SubCategory')
    other_sub_category = ArrayField(base_field=models.CharField(max_length=100), size=10, blank=True, null=True)
    other_activity_type = ArrayField(base_field=models.CharField(max_length=100), size=10, blank=True, null=True)
    recursive_project = models.BooleanField(default=False)
    university = models.ForeignKey('university.University', null=True, blank=True, on_delete=models.CASCADE,
                                   default=1)
    mission_area = models.ManyToManyField('home.MissionArea')
    community_partner = models.ManyToManyField('partners.CommunityPartner')
    campus_partner = models.ManyToManyField('partners.CampusPartner')
    history = HistoricalRecords()

    def get_name(self):
        return self.project_name

    #         return self.project_name

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.updated_by = user
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.project_name)


class SubCategory(models.Model):
    sub_category = models.CharField(max_length=30, blank=True, null=False)
    sub_category_descr = models.CharField(max_length=250, blank=True, null=True)
    sub_category_tags = models.CharField(max_length=1024, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords()

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.sub_category)


class MissionSubCategory(models.Model):
    sub_category = models.ForeignKey('projects.SubCategory', on_delete=models.CASCADE)
    secondary_mission_area = models.ForeignKey('home.MissionArea', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords()

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def _str_(self):
        return str(self.sub_category)


class ProjectSubCategory(models.Model):
    project_name = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('projects.SubCategory', on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords()

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def _str_(self):
        return str(self.project_name)


class ProjectRelatedLink(models.Model):
    project_name = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    link_descr = models.CharField(max_length=250, blank=True, null=False)
    link = models.CharField(max_length=250, blank=True, null=False)
    isAccessible = models.BooleanField(default=True)
    history = HistoricalRecords()

    def _str_(self):
        return str(self.project_name)


class ProjectMission(models.Model):
    mission_choices = (
        ('Primary', 'Primary'),
        ('Other', 'Other'),
    )
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    mission_type = models.CharField(max_length=20, choices=mission_choices)
    mission = models.ForeignKey('home.MissionArea', on_delete=models.CASCADE, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.mission)


class ProjectCommunityPartner(models.Model):
    project_name = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    community_partner = models.ForeignKey('partners.CommunityPartner', on_delete=models.CASCADE, blank=True, null=True)
    total_hours = models.IntegerField(blank=True, null=True)
    total_people = models.IntegerField(blank=True, null=True)
    wages = models.IntegerField(default=22)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.project_name)


class ProjectCampusPartner(models.Model):
    project_name = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    campus_partner = models.ForeignKey('partners.CampusPartner', on_delete=models.CASCADE, blank=True, null=True)
    total_hours = models.IntegerField(blank=True, null=True, default=0)
    total_people = models.IntegerField(blank=True, null=True, default=0)
    wages = models.IntegerField(blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.project_name)


# Models below are Project lookup tables, must have values to insert project data


class Status(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"


class EngagementType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=1500, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.name)


class ActivityType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.name)


class EngagementActivityType(models.Model):
    EngagementTypeName = models.ForeignKey('EngagementType', on_delete=models.CASCADE)
    ActivityTypeName = models.ForeignKey('ActivityType', on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.ActivityTypeName)


class ProjectEngagementActivity(models.Model):
    ProjectName = models.ForeignKey('Project', on_delete=models.CASCADE)
    ProjectEngagementActivityName = models.ForeignKey('EngagementActivityType', on_delete=models.CASCADE)
    # ProjectEngagementActivityName =  OneToMany(to=EngagementActivityType)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.ProjectName)


class AcademicYear(models.Model):
    academic_year = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.academic_year)
