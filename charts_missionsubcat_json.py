import pandas as pd
import json
import datetime
import boto3
import logging
import os
import psycopg2
from UnoCPI import settings

currentDT = datetime.datetime.now()
logger=logging.getLogger("UNO CPI Application")
conn = psycopg2.connect("dbname = 'UNO_CPI_DEV' user = 'postgres' host = 'localhost' password = 'horcrux'")
if (conn):
    logger.info("Connection Successful!")
else:
    logger.info("Connection Error!")
cursor = conn.cursor()

dirname = os.path.dirname(__file__)
mission_file = os.path.join(dirname,'home/static/charts_json/mission_subcategories.json')

q = "SELECT id, mission_name " \
    "FROM home_missionarea ;"
cursor.execute(q)
missions = cursor.fetchall()
records = len(missions)
json_data = []
for m in missions:
    q = "select sub_category_id, " \
        "(select sub_category from projects_subcategory where id = sub_category_id) as sub_category_name " \
        "from projects_missionsubcategory " \
        "where secondary_mission_area_id = %(x1)s ;"
    cursor.execute(q, {'x1': m[0]})
    subcats = cursor.fetchall()
    subs = []
    for s in subcats:
        res = {'subcategory_id': s[0], 'subcategory_name':s[1]}
        subs.append(res)
    res = {'mission_area_id': m[0], 'mission_area_name': m[1], 'subcategories': subs}
    json_data.append(res)
jsonstring = pd.io.json.dumps(json_data)

if records != 0:
    logger.info("Write Mission Subcategories JSON for charts  in output directory")
    with open(mission_file, 'w') as output_file:
        output_file.write(format(jsonstring))

#writing into amazon aws s3
ACCESS_ID=settings.AWS_ACCESS_KEY_ID
ACCESS_KEY=settings.AWS_SECRET_ACCESS_KEY
s3 = boto3.resource('s3',
         aws_access_key_id=ACCESS_ID,
         aws_secret_access_key= ACCESS_KEY)

if records == 0:
    print("Mission Subcategories JSON for charts NOT written having total records of " +repr(records)+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
    logger.info("Mission Subcategories JSON for charts NOT written having total records of " +repr(records)+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
else:
    s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/mission_subcategories.json').put(Body=format(jsonstring))
    print("Mission Subcategories JSON for charts written having total records of " +repr(records)+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
    logger.info("Mission Subcategories JSON for charts written having total records of " +repr(records)+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))

