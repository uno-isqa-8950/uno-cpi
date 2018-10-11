from django.contrib import admin
from .models import User
from .models import Contact, MissionArea



class ContactList(admin.ModelAdmin):

    list_display = ('first_name', 'last_name', 'work_phone', 'cell_phone', 'email_id', 'contact_type','community_partner', 'campus_partner')

    search_fields = ('first_name', 'last_name', 'email_id', 'contact_type', 'community_partner', 'campus_partner')


class MissionAreaList(admin.ModelAdmin):

    list_display = ('mission_name', 'description')

    search_fields = ('mission_name', 'description')


admin.site.register(User)
admin.site.register(Contact,ContactList)
admin.site.register(MissionArea,MissionAreaList)

