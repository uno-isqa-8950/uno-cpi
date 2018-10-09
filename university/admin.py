from django.contrib import admin

from .models import EducationSystem, University , College, Department,Course


class EducationSystemList(admin.ModelAdmin):

    list_display = ('name',)

    search_fields = ('name',)


class UniversityList(admin.ModelAdmin):

    list_display = ('name', 'education_system')

    search_fields = ('name', 'education_system')


class CollegeList(admin.ModelAdmin):

    list_display = ('college_name', 'university')

    search_fields = ('college_name', 'university')


class DepartmentList(admin.ModelAdmin):

    list_display = ('department_name', 'college_name')

    search_fields = ('department_name', 'college_name')


class CourseList(admin.ModelAdmin):

    list_display = ('prefix', 'number', 'name','project_name', 'university')

    search_fields =  ('prefix', 'number', 'name','project_name', 'university')


admin.site.register(EducationSystem,EducationSystemList)
admin.site.register(University,UniversityList)
admin.site.register(College,CollegeList)
admin.site.register(Department,DepartmentList)
admin.site.register(Course,CourseList)