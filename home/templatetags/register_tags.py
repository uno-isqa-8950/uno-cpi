from django import template
from home.models import Community_Partner_Snippet, Community_Partner_User_Snippet, Campus_Partner_Snippet, \
    Campus_Partner_User_Snippet, Public_Project_Report_Snippet, Private_Project_Report_Snippet, \
    Community_Public_Report_Snippet, Community_Private_Report_Snippet, Engagement_Types_Chart_Snippet, \
    Engagement_Types_Report_Snippet, Mission_Areas_Chart_Snippet, Mission_Areas_Report_Snippet, \
    Register_Campus_Partner_Snippet, Register_Campus_Partner_User_Snippet, Register_Community_Partner_Snippet, \
    Register_Community_Partner_User_Snippet, All_Projects_Snippet, Create_Projects_Snippet, My_Projects_Snippet, \
    Community_Partner_Project_Snippet, Create_Projects_Form_Snippet, Login_Snippet, Logout_Snippet, \
    Partners_Organizatiion_Profile_Contacts_Snippet, Partners_Organizatiion_Profile_Partners_Add_Snippet, \
    Partners_Organizatiion_Profile_Partners_Update_Snippet, Partners_Organizatiion_Profile_Snippet, \
    Partners_User_Profile_Snippet, Partners_User_Profile_Update_Snippet, Password_Reset_Done_Snippet, \
    Password_Reset_Snippet, Register_Community_Partner_Form_Snippet

register = template.Library()


@register.inclusion_tag('tags/community_partner_snippet.html', takes_context=True)
def comm_parts(context):
    return {
        'comm_parts': Community_Partner_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/community_partner_user_snippet.html', takes_context=True)
def comm_part_users(context):
    return {
        'comm_part_users': Community_Partner_User_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/campus_partner_snippet.html', takes_context=True)
def cam_parts(context):
    return {
        'cam_parts': Campus_Partner_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/campus_partner_user_snippet.html', takes_context=True)
def cam_part_users(context):
    return {
        'cam_part_users': Campus_Partner_User_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/public_project_report_snippet.html', takes_context=True)
def pub_projs(context):
    return {
        'pub_projs': Public_Project_Report_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/private_project_report_snippet.html', takes_context=True)
def priv_projs(context):
    return {
        'priv_projs': Private_Project_Report_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/community_public_report_snippet.html', takes_context=True)
def pub_comms(context):
    return {
        'pub_comms': Community_Public_Report_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/community_private_report_snippet.html', takes_context=True)
def priv_comms(context):
    return {
        'priv_comms': Community_Private_Report_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/engagement_types_report_snippet.html', takes_context=True)
def eng_types(context):
    return {
        'eng_types': Engagement_Types_Report_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/mission_areas_report_snippet.html', takes_context=True)
def miss_areas(context):
    return {
        'miss_areas': Mission_Areas_Report_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/engagement_types_chart_snippet.html', takes_context=True)
def eng_charts(context):
    return {
        'eng_charts': Engagement_Types_Chart_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/mission_areas_chart_snippet.html', takes_context=True)
def miss_charts(context):
    return {
        'miss_charts': Mission_Areas_Chart_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/register_campus_partner_snippet.html', takes_context=True)
def cam_part_regs(context):
    return {
        'cam_part_regs': Register_Campus_Partner_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/register_community_partner_snippet.html', takes_context=True)
def com_part_regs(context):
    return {
        'com_part_regs': Register_Community_Partner_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/register_campus_partner_user_snippet.html', takes_context=True)
def cam_part_user_regs(context):
    return {
        'cam_part_user_regs': Register_Campus_Partner_User_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/register_community_partner_user_snippet.html', takes_context=True)
def com_part_user_regs(context):
    return {
        'com_part_user_regs': Register_Community_Partner_User_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/all_projects_snippet.html', takes_context=True)
def all_projects(context):
    return {
        'all_projects': All_Projects_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/my_projects_snippet.html', takes_context=True)
def my_projects(context):
    return {
        'my_projects': My_Projects_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/create_projects_snippet.html', takes_context=True)
def create_projects(context):
    return {
        'create_projects': Create_Projects_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/create_projects_form_snippet.html', takes_context=True)
def create_project_forms(context):
    return {
        'create_project_forms': Create_Projects_Form_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/register_community_partner_form_snippet.html', takes_context=True)
def reg_comm_forms(context):
    return {
        'reg_comm_forms': Register_Community_Partner_Form_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/community_partner_project_snippet.html', takes_context=True)
def comm_part_projs(context):
    return {
        'comm_part_projs': Community_Partner_Project_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/partners_user_profile_snippet.html', takes_context=True)
def part_user_profs(context):
    return {
        'part_user_profs': Partners_User_Profile_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/partners_user_profile_update_snippet.html', takes_context=True)
def part_user_prof_ups(context):
    return {
        'part_user_prof_ups': Partners_User_Profile_Update_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/partners_organization_profile_snippet.html', takes_context=True)
def part_org_profs(context):
    return {
        'part_org_profs': Partners_Organizatiion_Profile_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/partners_organization_profile_contacts_snippet.html', takes_context=True)
def part_org_prof_cons(context):
    return {
        'part_org_prof_cons': Partners_Organizatiion_Profile_Contacts_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/partners_organization_profile_updates_snippet.html', takes_context=True)
def part_org_prof_ups(context):
    return {
        'part_org_prof_ups': Partners_Organizatiion_Profile_Partners_Update_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/partners_organization_profile_add_snippet.html', takes_context=True)
def part_org_prof_adds(context):
    return {
        'part_org_prof_adds': Partners_Organizatiion_Profile_Partners_Add_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/logout_snippet.html', takes_context=True)
def logouts(context):
    return {
        'logouts': Logout_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/login_snippet.html', takes_context=True)
def logins(context):
    return {
        'logins': Login_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/password_reset_snippet.html', takes_context=True)
def pass_resets(context):
    return {
        'pass_resets': Password_Reset_Snippet.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('tags/password_reset_done.html', takes_context=True)
def pass_dones(context):
    return {
        'pass_dones': Password_Reset_Done_Snippet.objects.all(),
        'request': context['request'],
    }