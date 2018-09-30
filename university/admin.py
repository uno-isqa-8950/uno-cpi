from django.contrib import admin

from .models import EducationSystem, University , College, Department,Course

admin.site.register(EducationSystem)
admin.site.register(University)
admin.site.register(College)
admin.site.register(Department)
admin.site.register(Course)