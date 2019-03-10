from django.contrib import admin

from .models import EducationSystem, University , College, Department,Course

from import_export import resources
from import_export.admin import ImportExportModelAdmin

class EducationSystemList(admin.ModelAdmin):

    list_display = ('name',)

    search_fields = ('name',)


class UniversityList(admin.ModelAdmin):

    list_display = ('name', 'education_system')

    search_fields = ('name', 'education_system')


class CollegeResource(resources.ModelResource):

    class Meta:
        model = College

class CollegeList(ImportExportModelAdmin):

    list_display = ('college_name', 'university')

    search_fields = ('college_name', 'university')

    resource_class = CollegeResource


class DepartmentResource(resources.ModelResource):

    class Meta:
        model = Department

class DepartmentList(ImportExportModelAdmin):

    list_display = ('department_name', 'college_name')

    search_fields = ('department_name', 'college_name')

    resource_class = DepartmentResource


class CourseResource(resources.ModelResource):

    class Meta:
        model = Course

class CourseList(ImportExportModelAdmin):

    list_display = ('prefix', 'number', 'name','project_name', 'university')

    search_fields =  ('prefix', 'number', 'name','project_name', 'university')

    resource_class = CourseResource


admin.site.register(EducationSystem,EducationSystemList)
admin.site.register(University,UniversityList)
admin.site.register(College,CollegeList)
admin.site.register(Department,DepartmentList)
admin.site.register(Course,CourseList)