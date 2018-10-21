#coding=utf-8
import xlrd
from geojson import FeatureCollection, Feature, Point
import sys
import json


def yearDict(sheet):
    community = {}
    k_12={}
    rows=sheet.nrows
    print(rows)

    for i in range(1,rows):
        lineString=sheet.row_values(i)
        com=lineString[2].strip()
        k12=lineString[4].strip()
        year=lineString[9].strip()

        if(com!="" and com!="N/A"):
            if(com in community.keys()):
                if(year not in community[com]):
                    community[com].append(year)
            else:
                community[com]=[year]

        if(k12!="" and k12!="N/A"):
            if (k12 in k_12.keys()):
                if(year not in k_12[k12]):
                    k_12[k12].append(year)
            else:
                k_12[k12] = [year]

    result={}
    result["community"]=community
    print(community)
    result["k_12"]=k_12
    print(k_12)
    return result

def geoJsonSheetCK(sheet,semester,coordinates):
    titles=sheet.row_values(0)
    rows=sheet.nrows
    cols=sheet.ncols

    collection=[]
    for i in range(1, rows):
        rowString=sheet.row_values(i)
        properties={}

        partnerName=rowString[0].strip()

        #Add Features
        for j in range(0, cols):
            title=titles[j].strip()
            colMessage=rowString[j]
            if(colMessage=="N/A"):
                continue
            if(title=="Zip" and type(colMessage)==float):
                properties[title]=str(int(colMessage))
            else:
                if(type(colMessage)==str):
                    properties[title]=colMessage.strip()
                else:
                    properties[title] = colMessage

        # Get point
        if(partnerName in coordinates.keys()):
            if(coordinates[partnerName]!="None"):
                point=Point(coordinates[partnerName])
            else:
                point=None
        else:
            point=None

        #Set Year
        if (partnerName in semester.keys()):
            properties["semester"] = semester[partnerName]
            for x in semester[partnerName]:
                pro=properties.copy()
                pro['time']=x
                feature = Feature(id=i, geometry=point, properties=pro)
                collection.append(feature)
                print(collection)
                print("    ")

    featureColloction=FeatureCollection(collection)

    with open("communityPartners.geojson", 'w', encoding='utf-8') as fp:
        json.dump(featureColloction, fp, ensure_ascii=False)

def geoJsonSheetP(sheet,coordinates):
    titles=sheet.row_values(0)
    rows=sheet.nrows
    cols=sheet.ncols

    collection=[]
    for i in range(1, rows):
        rowString=sheet.row_values(i)
        properties={}

        partnerName=rowString[0].strip()

        #Add Features
        for j in range(0, cols):
            title=titles[j].strip()
            colMessage=rowString[j]
            if(colMessage=="N/A"):
                continue
            if(title=="Zip" and type(colMessage)==float):
                properties[title]=str(int(colMessage))
            else:
                if(type(colMessage)==str):
                    properties[title]=colMessage.strip()
                else:
                    properties[title] = colMessage

        # Get point
        if("PrimaryCommunityPartner" in properties.keys()):
            if(properties["PrimaryCommunityPartner"] in coordinates.keys()):
                if (coordinates[properties["PrimaryCommunityPartner"]] != "None"):
                    point = Point(coordinates[properties["PrimaryCommunityPartner"]])
            
            point = None
        else:
            point = None

        feature = Feature(id=i, geometry=point, properties=properties)
        collection.append(feature)

    featureColloction=FeatureCollection(collection)

    with open("project.geojson", 'w', encoding='utf-8') as fp:
        json.dump(featureColloction, fp, ensure_ascii=False)


if __name__=="__main__":
    excelP = xlrd.open_workbook("Projects.xlsx")
    excelC = xlrd.open_workbook("Community_Partner.xlsx")
    result=yearDict(excelP.sheet_by_index(0))
    community = result["community"]

    with open("coordinates.json", "r", encoding="utf-8") as fp:
        coordinates = json.load(fp)

    geoJsonSheetCK(excelC.sheet_by_index(0),community,coordinates)
    geoJsonSheetP(excelP.sheet_by_index(0),coordinates)




