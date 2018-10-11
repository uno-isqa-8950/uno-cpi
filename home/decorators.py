from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from home.models import Contact


def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account:loginPage'):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def campuspartner_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account:loginPage'):
    '''
    Decorator for views that checks that the logged in user is a Campus Partner,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_campuspartner,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator



def communitypartner_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account:loginPage'):
    '''
    Decorator for views that checks that the logged in user is a Community Partner,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_communitypartner,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator