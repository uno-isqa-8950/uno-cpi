####### This file is to turn an Excel file into GEOJSON. This is for Community Partner #######################
import pandas as pd

df = pd.read_excel('static/Excel/CommunityPartner.xls') #Get the Excel file from static/Excel

collection = {'type': 'FeatureCollection', 'features': []}

df['description'] = df[['Address', 'City', 'State', 'Zip']].apply(lambda x: ' '.join(x.astype(str)), axis=1)


def feature_from_row(CommunityPartner, latitude, longitude, description, Primary, Website, Phone):
    feature = {'type': 'Feature', 'properties': {'PartnerName': '', 'Address': '', 'marker-color': '',
                                                 'Website': '', 'PrimaryMission': '', 'Phone': ''},
               'geometry': {'type': 'Point', 'coordinates': []}
               }
    feature['geometry']['coordinates'] = [longitude, latitude]
    feature['properties']['PartnerName'] = CommunityPartner
    feature['properties']['Address'] = description
    feature['properties']['Website'] = Website
    feature['properties']['PrimaryMission'] = Primary
    feature['properties']['Phone'] = Phone
    if Primary == "Economic Sufficiency":
        feature['properties']['marker-color'] = "FF5733"
    elif Primary == "Social Justice":
        feature['properties']['marker-color'] = "FFF033"
    elif Primary == "Health and Wellness":
        feature['properties']['marker-color'] = "74FF33"
    elif Primary == "Environmental Stewardship":
        feature['properties']['marker-color'] = "338DFF"
    elif Primary == "Educational Support":
        feature['properties']['marker-color'] = "CE33FF"
    else:
        feature['properties']['marker-color'] = "FF3374"
    collection['features'].append(feature)
    return feature


geojson_series = df.apply(
    lambda x: feature_from_row(x['CommunityPartner'], x['Lat'], x['Longitude'], x['description'], x['Primary'],
                               x['Website'], x['Phone']),
    axis=1)

jsonstring = pd.io.json.dumps(collection)

output_filename = 'static/GEOJSON/CommunityPartner.geojson' #The file will be saved under static/GEOJSON
with open(output_filename, 'w') as output_file:
    output_file.write(format(jsonstring))
