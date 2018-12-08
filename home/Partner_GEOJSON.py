import pandas as pd
import googlemaps
import json
from shapely.geometry import shape, Point


with open('static/GEOJSON/USCounties_final.geojson') as f:
    geojson1 = json.load(f)

county = geojson1["features"]

with open('static/GEOJSON/ID2.geojson') as f:
    geojson = json.load(f)

district = geojson["features"]
project = pd.read_csv('static/Excel/CleanedProject.csv')
df = pd.read_csv('static/Excel/Community Partners.csv') #Get the Excel file from static/Excel

gmaps = googlemaps.Client(key='AIzaSyBoBkkxBnB7x_GKESVPDLguK0VxSTSxHiI')
collection = {'type': 'FeatureCollection', 'features': []}

df['fulladdress'] = df[['address_line1', 'city', 'state']].apply(lambda x: ' '.join(x.astype(str)), axis=1)

def feature_from_row(Community, Address, Mission, CommunityType, Website):
    feature = {'type': 'Feature', 'properties': {'CommunityPartner': '', 'Address': '',
                                                 'Legislative District Number': '', 'Number of projects': '',
                                                 'Income': '', 'County': '', 'Mission Area': '',
                                                 'CommunityType': '', 'Campus Partner': '',
                                                 'Academic Year': '', 'Website': ''},
               'geometry': {'type': 'Point', 'coordinates': []}
               }
    geocode_result = gmaps.geocode(Address)  # get the coordinates
    print(Address)
    print(geocode_result)
    if (geocode_result[0]):
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
        feature['geometry']['coordinates'] = [longitude, latitude]
        coord = Point([longitude, latitude])
        for i in range(len(district)):  # iterate through a list of district polygons
            property = district[i]
            polygon = shape(property['geometry'])  # get the polygons
            if polygon.contains(coord):  # check if a partner is in a polygon
                feature['properties']['Legislative District Number'] = property["properties"]["id"]  # assign the district number to a partner
        for m in range(len(county)):  # iterate through the County Geojson
            properties2 = county[m]
            polygon = shape(properties2['geometry'])  # get the polygon
            if polygon.contains(coord):  # check if the partner in question belongs to a polygon
                feature['properties']['County'] = properties2['properties']['NAME']
                feature['properties']['Income'] = properties2['properties']['Income']
        # projectlist = 0
    yearlist = []
    campuslist = []

    partners = project['community_partner']
    years = project['academic_year']
    campuses = project['campus_partner']
    count = 0
    for n in range(len(partners)):
        if (partners[n] == Community):
            if (years[n] not in yearlist):
                yearlist.append(years[n])
            if (campuses[n] not in campuslist):
                campuslist.append(campuses[n])
            count += 1
    feature['properties']['Number of projects'] = count
    feature['properties']['Campus Partner'] = campuslist
    feature['properties']['Academic Year'] = yearlist
    feature['properties']['CommunityPartner'] = Community
    feature['properties']['CommunityType'] = CommunityType
    feature['properties']['Website'] = Website
    feature['properties']['Mission Area'] = Mission

    collection['features'].append(feature)
    return feature


geojson_series = df.apply(
    lambda x: feature_from_row(x['name'], x['fulladdress'], x['mission_area'], x['community_type'], x['website_url']),
    axis=1)
#
jsonstring = pd.io.json.dumps(collection)

output_filename = 'static/GEOJSON/Partner.geojson' #The file will be saved under static/GEOJSON
with open(output_filename, 'w') as output_file:
    output_file.write(format(jsonstring))