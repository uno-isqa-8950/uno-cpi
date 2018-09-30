from django.contrib import admin
from .models import User
from .models import Contact, MissionArea

admin.site.register(User)
admin.site.register(Contact)
admin.site.register(MissionArea)

