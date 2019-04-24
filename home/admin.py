from django.contrib import admin
from .models import User
from .models import Contact, MissionArea, HouseholdIncome, DataDefinition,DataDefinitionGroup
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
#from django.contrib.admin import AdminSite
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

class UserResource(resources.ModelResource):

    class Meta:
        model = User


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name','avatar')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','is_campuspartner', 'is_communitypartner',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    resource_class = UserResource

# class ContactList(admin.ModelAdmin):
#
#     list_display = ('first_name', 'last_name', 'work_phone', 'cell_phone', 'email_id', 'contact_type','community_partner', 'campus_partner')
#
#     search_fields = ('first_name', 'last_name', 'email_id', 'contact_type', 'community_partner', 'campus_partner')


class MissionAreaList(admin.ModelAdmin):

    list_display = ('mission_name', 'description')

    search_fields = ('mission_name', 'description')

class HouseholdIncomeResource(resources.ModelResource):
    class Meta:
        model = HouseholdIncome

class HouseholdIncomeAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    resource_class = HouseholdIncomeResource
    list_display = ('county', 'median_income')
    search_fields = ('county', )

class DataDefinitionGroupResource(resources.ModelResource):
    class Meta:
        model = DataDefinitionGroup


class DataDefinitionGroupList(ImportExportModelAdmin):
    list_display = ('group',)
    search_fields = ('group',)
    resource_class = DataDefinitionGroupResource

class DataDefinitionResource(resources.ModelResource):
    class Meta:
        model = DataDefinition

class DataDefinitionList(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ('title','description','group')
    search_fields = ('title','group__group')
    resource_class = DataDefinitionResource


# class HouseholdIncomeList(admin.ModelAdmin):
#
#     list_display = ('county', 'median_income')
#
#     search_fields = ('county', )

class ContactResource(resources.ModelResource):
    community_partner = fields.Field(attribute='community_partner', column_name="Community Partner")
    campus_partner = fields.Field(attribute='campus_partner', column_name="Campus Partner")
    
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'work_phone', 'cell_phone', 'email_id', 'contact_type','community_partner', 'campus_partner')

class ContactAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    resource_class = ContactResource
    list_display = ('first_name', 'last_name', 'work_phone', 'cell_phone', 'email_id', 'contact_type','community_partner', 'campus_partner')

    search_fields = ('first_name', 'last_name', 'email_id', 'contact_type', 'community_partner__name', 'campus_partner__name')



# admin.site.register(User)
admin.site.register(Contact, ContactAdmin)
admin.site.register(MissionArea, MissionAreaList)
admin.site.register(HouseholdIncome, HouseholdIncomeAdmin)
admin.site.register(DataDefinition, DataDefinitionList)
admin.site.register(DataDefinitionGroup, DataDefinitionGroupList)
admin.site.site_header = "UNO CPI Admin"
admin.site.site_title = "Community Partnership Initiative"
admin.site.index_title = " "

admin.site.site_url = False
