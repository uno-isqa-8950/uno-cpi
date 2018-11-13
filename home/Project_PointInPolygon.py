import json
from shapely.geometry import shape, Point
import pandas as pd
# depending on your version, use: from shapely.geometry import shape, Point

# load GeoJSON file containing sectors
#with open('sectors.json') as f:
#    js = json.load(f)
with open('static/GEOJSON/Projects.geojson') as json_data:
    project = json.load(json_data)

project = project["features"]
# construct point based on lon/lat returned by geocoder
#point = Point(-96.003958, 41.242062)
with open('static/GEOJSON/ID2.geojson') as f:
    geojson = json.load(f)

df = geojson["features"]

with open('static/GEOJSON/NEcounties2.geojson') as f:
    geojson1 = json.load(f)

county = geojson1["features"]

for j in range(len(project)):
    if project[j]['geometry']:
        coord = Point(project[j]['geometry']['coordinates'])
        for i in range(len(df)):
            properties = df[i]
            polygon = shape(properties['geometry'])
            if polygon.contains(coord):
                project[j]['properties']['district'] = properties['id']
        for m in range(len(county)):
            properties2 = county[m]
            polygon = shape(properties2['geometry'])
            if polygon.contains(coord):
                project[j]['properties']['income'] = properties2['properties']['Income']
                project[j]['properties']['County'] = properties2['properties']['NAME']

    else:
        project[j]['properties']['district'] = "N/A"
        project[j]['properties']['income'] = "N/A"
        project[j]['properties']['County'] = "N/A"

collection = {'type': 'FeatureCollection', 'features': project}
jsonstring = pd.io.json.dumps(collection)

output_filename = 'static/GEOJSON/Projects_new.geojson' #The file will be saved under static/GEOJSON
with open(output_filename, 'w') as output_file:
    output_file.write(format(jsonstring))
