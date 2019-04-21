from django.db import models
from simple_history.models import HistoricalRecords


class EducationSystem (models.Model):
    name = models.CharField(max_length=255, unique=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.name)


class University (models.Model):
    name = models.CharField(max_length=255, unique=True)
    education_system = models.ForeignKey(EducationSystem, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universities"


class College (models.Model):
    college_name = models.CharField(max_length=255, unique=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        ordering = ('college_name',)

    def __str__(self):
        return str(self.college_name)


class Department(models.Model):
    department_name = models.CharField(max_length=30)
    college_name = models.ForeignKey(College, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.department_name)


class Course(models.Model):
    prefix = models.CharField(max_length=80)
    number = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    section = models.PositiveIntegerField(default=0)
    project_name = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    university = models.ForeignKey('university', on_delete=models.CASCADE, null=True)
    history = HistoricalRecords()
