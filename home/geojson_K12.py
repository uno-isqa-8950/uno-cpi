####### This file is to turn an Excel file into GEOJSON. This is for K12 #######################
import pandas as pd

df = pd.read_excel('static/Excel/K12Partner.xls') #Get the Excel file from static/Excel

collection = {'type': 'FeatureCollection', 'features': []}

df['description'] = df[['Address', 'City', 'State', 'Zip']].apply(lambda x: ' '.join(x.astype(str)), axis=1)


def feature_from_row(CommunityPartner, latitude, longitude, description, Website, Phone):
    feature = {'type': 'Feature',
               'properties': {'PartnerName': '', 'Address': '', 'marker-color': '',
                              'Website': '', 'Phone': ''},
               'geometry': {'type': 'Point', 'coordinates': []}
               }
    feature['geometry']['coordinates'] = [longitude, latitude]
    feature['properties']['PartnerName'] = CommunityPartner
    feature['properties']['Address'] = description
    feature['properties']['marker-color'] = '74FF33'
    feature['properties']['Website'] = Website
    feature['properties']['Phone'] = Phone
    collection['features'].append(feature)
    return feature


geojson_series = df.apply(
    lambda x: feature_from_row(x['Community Partner'], x['Latitude'], x['Longitude'], x['description'],
                               x['Website'], x['Phone Number']),
    axis=1)

jsonstring = pd.io.json.dumps(collection)

output_filename = 'static/GEOJSON/K12Partner.geojson' #The file will be saved under static/GEOJSON
with open(output_filename, 'w') as output_file:
    output_file.write(format(jsonstring))
