from django.db import models


class EducationSystem (models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)


class University (models.Model):
    name = models.CharField(max_length=255, unique=True)
    education_system = models.ForeignKey(EducationSystem, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class College (models.Model):
    college_name = models.CharField(max_length=255, unique=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.college_name)


class Department(models.Model):
    department_name = models.CharField(max_length=30)
    college_name = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.department_name)


class Course(models.Model):
    prefix = models.CharField(max_length=80)
    number = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    project_name = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    university = models.ForeignKey('university', on_delete=models.CASCADE, null=True)
