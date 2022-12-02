from university.models import University

def get_hostname(request):
    return request.get_host().split(':')[0].lower()

def get_tenant(request):
    hostname = get_hostname(request)
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

