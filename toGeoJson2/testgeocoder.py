#coding=utf-8
from mapbox import Geocoder
import xlrd
from geojson import FeatureCollection, Feature, Point
import sys
import json


#Get coordinate by address
def addressToCOORDINATE(name):
    geocoder = Geocoder(access_token="pk.eyJ1IjoibG9va3VwbWFuIiwiYSI6ImNqbW41cmExODBxaTEzeHF0MjhoZGg1MnoifQ.LGL5d5zGa1z6ms-IVyn7sw")
    response = geocoder.forward(name, limit=1)
    if(response.status_code==200):
        try:
            collection = response.json()
            result=collection['features'][0]["geometry"]['coordinates']
        except Exception as e:
            result="None"
            print("Unknown Error")
        return result
    else:                        
        return False

def getCommunityPartnerCOORDINATE(fileName):
    excel=xlrd.open_workbook(fileName)
    sheet = excel.sheet_by_index(0)
    rows=sheet.nrows
    coordinates={}
    for i in range(1,rows):

        lineString=sheet.row_values(i)
        name=lineString[0].strip()
        address= lineString[1].strip()
        city=lineString[2].strip()
        state=lineString[3].strip()

        detail=""
        if(address!="N/A"):
            detail+=address
            if(city!="N/A"):
                detail+=city
                if(state!="N/A"):
                    detail+=state
        if(detail!=""):
            print(".",end="")
            COORDINATE=addressToCOORDINATE(detail)
            coordinates[name]=COORDINATE
           

    with open("coordinates.json", 'w', encoding='utf-8') as fp:
        json.dump(coordinates, fp, ensure_ascii=False)


getCommunityPartnerCOORDINATE("Community_Partner.xlsx")
# name="4383 Nicholas St Suite 24,Omaha,NE"
# COORDINATE=addressToCOORDINATE(name)
# print(COORDINATE)