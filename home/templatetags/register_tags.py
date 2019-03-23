from django import template
from home.models import Community_Partner_Snippet, Community_Partner_User_Snippet, Campus_Partner_Snippet, Campus_Partner_User_Snippet

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