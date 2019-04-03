from django.contrib import admin

from .models import EducationSystem, University , College, Department,Course

from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin


class EducationSystemList(admin.ModelAdmin):

    list_display = ('name',)

    search_fields = ('name',)


class UniversityList(admin.ModelAdmin):

    list_display = ('name', 'education_system')

    search_fields = ('name', 'education_system__name')


class CollegeResource(resources.ModelResource):
    college_name = fields.Field(attribute='college_name', column_name="College Name")
    university = fields.Field(attribute='university', column_name="University")

    class Meta:
        model = College
        fields = ('college_name', 'university')

class CollegeList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('college_name', 'university')

    search_fields = ('college_name', 'university__name')

    resource_class = CollegeResource


class DepartmentResource(resources.ModelResource):

    class Meta:
        model = Department

class DepartmentList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('department_name', 'college_name')

    search_fields = ('department_name', 'college_name__college_name')

    resource_class = DepartmentResource


class CourseResource(resources.ModelResource):
    project_name = fields.Field(attribute='project_name', column_name="Project Name")
    university = fields.Field(attribute='university', column_name="University")

    class Meta:
        model = Course
        fields = ('prefix', 'number', 'name','project_name', 'university')

class CourseList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('prefix', 'number', 'name','project_name', 'university')

    search_fields =  ('prefix', 'number', 'name','project_name__project_name', 'university__name')

    resource_class = CourseResource


admin.site.register(EducationSystem,EducationSystemList)
admin.site.register(University,UniversityList)
admin.site.register(College,CollegeList)
admin.site.register(Department,DepartmentList)
admin.site.register(Course,CourseList)