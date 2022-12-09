from university.models import University

def get_hostname(request):
    return request.get_host().split(':')[0].lower()

def get_tenant(request):
    hostname = get_hostname(request)
    print(hostname)
    # if your on local, return all tenants
    subdomain = hostname.split('.')[1]
    try:
        # try to get the university subdomain
        print(University.objects.get(subdomain=subdomain))
        return University.objects.get(subdomain=subdomain)
    except:
        # if it cant, return all subdomains
        print('Couldnt get a subdomain, returning all')
        return University.objects.all()

def tenant_processor(request):
    tenants = get_tenant(request)
    print(tenants.__len__())
    if tenants.__len__() > 1:
        name = 'University of Nebraska Omaha'
        logo = 'https://www.unomaha.edu/_files/images/logo-subsite-o-2.png'
        primary_color = '#0a0a0a'
        secondary_color = '#d71920'
    else:
        name = tenants[0].name
        logo = tenants[0].logo
        primary_color = tenants[0].primary_color
        secondary_color = tenants[0].secondary_color
    return {'logo':logo,
            'primary_color': primary_color,
            'secondary_color': secondary_color,
            'name':name,}
