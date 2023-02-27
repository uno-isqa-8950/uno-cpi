from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import LoginForm
from django.contrib import messages

from django.conf import settings
from django.urls import reverse
from django.http import (HttpResponse, HttpResponseRedirect,
                         HttpResponseServerError)
from django.shortcuts import render

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from home.models import *
import os
import json
import re


samlDict = {
    "unomaha.edu": "uno",
    # "unml.edu": "unml",
    # "nebraska.edu": "neb"
}


# Create your views here.
def verifySamlSettingJson():

    setupJson = "false"
    jsonFile = open(settings.SAML_FOLDER + "/settings.json", "r")  # Open the JSON file for reading
    data = json.load(jsonFile)  # Read the JSON into the buffer
    jsonFile.close()  # Close the JSON file

    saml_host = settings.SAML_HOST_URL
    print('saml_host--' + saml_host)
    data['sp']['assertionConsumerService']['url'] = saml_host + 'account/?acs'
    data['sp']['singleLogoutService']['url'] = saml_host + 'account/?sls'

    jsonFile = open(settings.SAML_FOLDER + "/settings.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()
    setupJson = "true"
    return setupJson


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            emailInput = cd['email']
            emailDomain = emailInput.split('@')[1]

            print('print email--', emailInput)
            print('print emailDomain--', emailDomain)

            user = None
            emailInput = cd['email']
            # check if email domain exists in dict, perform user validation and redirect to SSO else perform app authentication
            if emailDomain in samlDict:
                print('emaildomain check--', emailDomain)
                # check if email id exists in CEPI database
                try:
                    user = get_user_model().objects.get(email=emailInput)
                except get_user_model().DoesNotExist:
                    user = None
                # redirect valid user to SSO page else redirect to login page with error message
                if user is not None:
                    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    saml_idp = samlDict[emailDomain]
                    # set the appropriate SAML folder based on required IDP for respective email domain


                    settings.SAML_FOLDER = os.path.join(BASE_DIR, 'saml_' + saml_idp)
                    print('settings.APP_ENV--' + settings.APP_ENV)
                    # reassign the url in settings json based on enviornment running on,


                    # we should avoid checking for prod env ( we need to keep in since current prod url is not finaliszed)
                    setupJson = verifySamlSettingJson()
                    print('setupJson--' + setupJson)
                    return redirect(settings.SAML_HOST_URL + "account/?sso")
                else:
                    messages.error(request,
                                   'You are not registered as a CEPI user. Please contact the administrator for access by emailing partnerships@unomaha.edu and identify what campus partner you are affiliated with.')
                    return render(request, 'registration/login.html', {'form': form})
            else:

                user = authenticate(request, email=cd['email'], password=cd['password'])

            if user is not None:
                print("user")
                print(user)
                if user.is_campuspartner:
                    login(request, user)
                    response = redirect('/myProjects')
                    return response
                elif user.is_communitypartner:
                    login(request, user)
                    response = redirect('/communitypartnerproject')
                    return response
                elif user.is_superuser:
                    login(request, user)
                    return redirect('/')
            else:
                messages.error(request, 'Email or Password is incorrect or contact system administration.')
                return render(request, 'registration/login.html', {'form': form})
                # return HttpResponse('Invalid Credentials')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def campushome(request):
    return render(request, 'projects/myProjects.html', {'campushome': campushome})


def CommunityHome(request):
    return render(request, 'projects/community_partner_projects.html', {'CommunityHome': CommunityHome})


def admin(request):
    return render(request, "home/admin_frame.html", {'admin': admin})


def logout_view(request):
    logout(request)


def redirectUNOUser(request, key):
    if key is not None:
        useremail = key[0]
        try:
            user = get_user_model().objects.get(email=useremail)
        except get_user_model().DoesNotExist:
            user = None

        if user is not None:
            if user.is_campuspartner:
                login(request, user)
                response = redirect('/myProjects')
                return response
            elif user.is_communitypartner:
                login(request, user)
                response = redirect('/communitypartnerproject')
                return response
            elif user.is_superuser:
                login(request, user)
                response = redirect('/admin')
                return response
        else:
            messages.error(request,
                           'You are not registered as a CEPI user. Please contact the administrator for access by emailing partnerships@unomaha.edu and identify what campus partner you are affiliated with.')
            return render(request, 'registration/login.html', {'form': LoginForm()})
    else:
        print('Error in SAML response, Please ccontact system administration.')
        messages.error(request, 'Error in SAML response, Please ccontact system administration.')
        return render(request, 'registration/login.html', {'form': LoginForm()})


def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=settings.SAML_FOLDER)
    return auth


def prepare_django_request(request):
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    result = {
        'https': 'on' if request.is_secure() else 'off',
        'http_host': request.META['HTTP_HOST'],
        'script_name': request.META['PATH_INFO'],
        # 'server_port': request.META['SERVER_PORT'], # uncomment this line for local run
        'server_port': '443',  # uncomment this line for dev, cat and prod env.
        'get_data': request.GET.copy(),
        'post_data': request.POST.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        'query_string': request.META['QUERY_STRING']
    }
    return result


def isValidEmail(emailAdd):
    print("emailAdd--", emailAdd)
    emailAddVal = ""
    validEmailAdd = False

    if (emailAdd is not None):
        emailAddVal = emailAdd[0]

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex, emailAddVal)):
        print("Valid Email")
        validEmailAdd = True
    else:
        print("Invalid Email")
        validEmailAdd = False
    return validEmailAdd


def index(request):
    req = prepare_django_request(request)
    auth = init_saml_auth(req)
    errors = []
    error_reason = None
    not_auth_warn = False
    success_slo = False
    attributes = False
    paint_logout = False

    if 'sso' in req['get_data']:
        return HttpResponseRedirect(auth.login())

    elif 'sso2' in req['get_data']:
        return_to = OneLogin_Saml2_Utils.get_self_url(req) + reverse('attrs')
        return HttpResponseRedirect(auth.login(return_to))
    elif 'slo' in req['get_data']:
        name_id = session_index = name_id_format = name_id_nq = name_id_spnq = None
        if 'samlNameId' in request.session:
            name_id = request.session['samlNameId']
        if 'samlSessionIndex' in request.session:
            session_index = request.session['samlSessionIndex']
        if 'samlNameIdFormat' in request.session:
            name_id_format = request.session['samlNameIdFormat']
        if 'samlNameIdNameQualifier' in request.session:
            name_id_nq = request.session['samlNameIdNameQualifier']
        if 'samlNameIdSPNameQualifier' in request.session:
            name_id_spnq = request.session['samlNameIdSPNameQualifier']
        logout(request)
        return HttpResponseRedirect(
            auth.logout(name_id=name_id, session_index=session_index, nq=name_id_nq, name_id_format=name_id_format,
                        spnq=name_id_spnq))

        # If LogoutRequest ID need to be stored in order to later validate it, do instead
        # slo_built_url = auth.logout(name_id=name_id, session_index=session_index)
        # request.session['LogoutRequestID'] = auth.get_last_request_id()
        # return HttpResponseRedirect(slo_built_url)
    elif 'acs' in req['get_data']:

        request_id = None
        if 'AuthNRequestID' in request.session:
            request_id = request.session['AuthNRequestID']

        auth.process_response(request_id=request_id)
        errors = auth.get_errors()
        print("errors-in saml response-", errors)
        not_auth_warn = not auth.is_authenticated()

        if not errors:
            if 'AuthNRequestID' in request.session:
                del request.session['AuthNRequestID']

            if auth.get_attributes() is not None:
                unoAtt = auth.get_attributes()
                userEmail = unoAtt['urn:oid:0.9.2342.19200300.100.1.3']
                print("user email--", userEmail)
                checkEmail = isValidEmail(userEmail)
                if checkEmail:
                    return redirectUNOUser(request, userEmail)
        else:
            print("errors-in saml response--",errors)
            redirectUNOUser(request,None)

    elif 'sls' in req['get_data']:

        request_id = None
        if 'LogoutRequestID' in request.session:
            request_id = request.session['LogoutRequestID']
        dscb = lambda: request.session.flush()
        url = auth.process_slo(request_id=request_id, delete_session_cb=dscb)
        errors = auth.get_errors()
        if len(errors) == 0:
            if url is not None:
                return HttpResponseRedirect(url)
            else:
                success_slo = True
        elif auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()

    if 'samlUserdata' in request.session:
        paint_logout = True
        if len(request.session['samlUserdata']) > 0:
            attributes = request.session['samlUserdata'].items()

    return render(request, 'registration/login.html', {'form': LoginForm()})


def attrs(request):
    paint_logout = False
    attributes = False

    if 'samlUserdata' in request.session:
        paint_logout = True
        if len(request.session['samlUserdata']) > 0:
            attributes = request.session['samlUserdata'].items()

    return render(request, 'registration/attrs.html',
                  {'paint_logout': paint_logout,
                   'attributes': attributes})


def metadata(request):
    print('settings.SAML_FOLDER--', settings.SAML_FOLDER)
    saml_settings = OneLogin_Saml2_Settings(settings=None, custom_base_path=settings.SAML_FOLDER,
                                            sp_validation_only=True)
    metadata = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = HttpResponse(content=metadata, content_type='text/xml')
    else:
        resp = HttpResponseServerError(content=', '.join(errors))
    return resp