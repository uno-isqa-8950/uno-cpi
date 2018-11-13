import json
from shapely.geometry import shape, Point
import pandas as pd
# depending on your version, use: from shapely.geometry import shape, Point

# load GeoJSON file containing sectors
#with open('sectors.json') as f:
#    js = json.load(f)
with open('static/GEOJSON/CommunityPartners.geojson') as json_data:
    commpartner = json.load(json_data)

commpartner = commpartner["features"]
# construct point based on lon/lat returned by geocoder
#point = Point(-96.003958, 41.242062)
with open('static/GEOJSON/ID2.geojson') as f:
    geojson = json.load(f)

df = geojson["features"]

with open('static/GEOJSON/NEcounties2.geojson') as f:
    geojson1 = json.load(f)

county = geojson1["features"]

for j in range(len(commpartner)):
    if commpartner[j]['geometry']:
        coord = Point(commpartner[j]['geometry']['coordinates'])
        for i in range(len(df)):
            properties = df[i]
            polygon = shape(properties['geometry'])
            if polygon.contains(coord):
                commpartner[j]['properties']['district'] = properties['id']
        for m in range(len(county)):
            properties2 = county[m]
            polygon = shape(properties2['geometry'])
            if polygon.contains(coord):
                commpartner[j]['properties']['income'] = properties2['properties']['Income']
                commpartner[j]['properties']['County'] = properties2['properties']['NAME']
    else:
        commpartner[j]['properties']['district'] = "N/A"
        commpartner[j]['properties']['income'] = "N/A"
        commpartner[j]['properties']['County'] = "N/A"

collection = {'type': 'FeatureCollection', 'features': commpartner}
jsonstring = pd.io.json.dumps(collection)

output_filename = 'static/GEOJSON/CommunityPartners_new.geojson' #The file will be saved under static/GEOJSON
with open(output_filename, 'w') as output_file:
    output_file.write(format(jsonstring))
