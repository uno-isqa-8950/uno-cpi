import pandas as pd
import googlemaps
import json
from shapely.geometry import shape, Point

df = pd.read_csv('static/Excel/CleanedProject.csv') #Get the Excel file from static/Excel
gmaps = googlemaps.Client(key='AIzaSyBoBkkxBnB7x_GKESVPDLguK0VxSTSxHiI')
collection = {'type': 'FeatureCollection', 'features': []}
# df['fulladdress'] = df[['Address Line1', 'City', 'State', 'Zip']].apply(lambda x: ' '.join(x.astype(str)), axis=1)

with open('static/GEOJSON/ID2.geojson') as f:
    geojson = json.load(f)

district = geojson["features"]

def feature_from_row(Projectname, Engagement, Activity, Description, Facilitator, Year, Campus, Community, Mission, Address, City, State, Zip):
    feature = {'type': 'Feature', 'properties': {'Project Name': '', 'Engagement Type': '', 'Activity Type': '',
                                                 'Description': '', 'Facilitator': '', 'Academic Year': '',
                                                 'Legislative District Number':'',
                                                 'Campus Partner': '', 'Community Partner':'', 'Mission Area':'',
                                                 'Address Line1':'', 'City':'', 'State':'', 'Zip':''},
               'geometry': {'type': 'Point', 'coordinates': []}
               }
    if (Address != "nan"):
        if (Address):
            fulladdress = str(Address) + ' ' + str(City) + ' ' + str(State)
            geocode_result = gmaps.geocode(fulladdress)  # get the coordinates
            latitude = geocode_result[0]['geometry']['location']['lat']
            longitude = geocode_result[0]['geometry']['location']['lng']
            feature['geometry']['coordinates'] = [longitude, latitude]
            coord = Point([longitude, latitude])
            for i in range(len(district)):  # iterate through a list of district polygons
                property = district[i]
                polygon = shape(property['geometry'])  # get the polygons
                if polygon.contains(coord):  # check if a partner is in a polygon
                    feature['properties']['Legislative District Number'] = property["properties"][
                        "id"]  # assign the district number to a partner
            feature['properties']['Project Name'] = Projectname
            feature['properties']['Engagement Type'] = Engagement
            feature['properties']['Activity Type'] = Activity
            feature['properties']['Description'] = Description
            feature['properties']['Facilitator'] = Facilitator
            feature['properties']['Academic Year'] = Year
            feature['properties']['Campus Partner'] = Campus
            feature['properties']['Community Partner'] = Community
            feature['properties']['Mission Area'] = Mission
            feature['properties']['Address Line1'] = Address
            feature['properties']['City'] = City
            feature['properties']['State'] = State
            feature['properties']['Zip'] = Zip
            collection['features'].append(feature)
            return feature


geojson_series = df.apply(
    lambda x: feature_from_row(x['project_name'], x['engagement_type'], x['activity_type'], x['description'], x['facilitator'],
                               x['academic_year'], x['campus_partner'], x['community_partner'], x['mission'],
                               str(x['address_line1']), str(x['city']), str(x['state']), str(x['zip'])),
    axis=1)
#
jsonstring = pd.io.json.dumps(collection)

output_filename = 'static/GEOJSON/Project.geojson' #The file will be saved under static/GEOJSON
with open(output_filename, 'w') as output_file:
    output_file.write(format(jsonstring))