from django import template
from home.models import Community_Partner_Snippet, Community_Partner_User_Snippet, Campus_Partner_Snippet, \
    Campus_Partner_User_Snippet, Public_Project_Report_Snippet, Private_Project_Report_Snippet, \
    Community_Public_Report_Snippet, Community_Private_Report_Snippet, Engagement_Types_Chart_Snippet, \
    Engagement_Types_Report_Snippet, Mission_Areas_Chart_Snippet, Mission_Areas_Report_Snippet

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
