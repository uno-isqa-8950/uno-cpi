import xlrd
from geojson import FeatureCollection, Feature, Point
import sys
import json



def readExcel(fileName):
    excel=xlrd.open_workbook(fileName)
    result=yearDict(excel.sheet_by_index(0))#Receive data

    community=result["community"]#get community Dict
    k_12=result["k_12"]#Get k12 Dict
    geoJsonSheet(excel.sheet_by_index(1),k_12)#Change k12 togeojson
    geoJsonSheet(excel.sheet_by_index(2),community)#Change k12 to geojson


def yearDict(sheet):#1st sheet
    community = {}#community Dict
    k_12={}#k12 Dict
    rows=sheet.nrows

    for i in range(1,rows):
        lineString=sheet.row_values(i)

        com=lineString[5].strip()#Get community
        k12=lineString[6].strip()#Get k12
        year=lineString[12].strip()#Get semester

        if(lineString[0]==''):#when no more data
            break              

        if(com!="" and com!="None"):#if community is not""/None, .append
            if(com in community.keys()):#check if communityPartner exists, if exists
                                        
                if(year not in community[com]):#check if semeter exsits if not, add
                    community[com].append(year)
            else:#add communityPartner
                community[com]=[year]

        if(k12!="" and k12!="None"):
            if (k12 in k_12.keys()):
                if(year not in k_12[k12]):
                    k_12[k12].append(year)
            else:
                k_12[k12] = [year]

    result={}
    result["community"]=community
    result["k_12"]=k_12
    return result


def geoJsonSheet(sheet,semester):
    titles=sheet.row_values(0)
    rows=sheet.nrows
    cols=sheet.ncols

    collection=[]
    for i in range(1, rows):
        rowString=sheet.row_values(i)
        properties={}

        partnerName=rowString[0].strip()

        for j in range(0, cols):
            title=titles[j].strip()
            colMessage=rowString[j]
            if(title=="Zip" and type(colMessage)==float):
                properties[title]=str(int(colMessage))
            else:
                if(type(colMessage)==str):
                    properties[title]=colMessage.strip()
                else:
                    properties[title] = colMessage

        if (type(properties["Longitude"]) == float and type(properties["Latitude"]) == float):
            point=Point((properties["Longitude"],properties["Latitude"]))
        else:
            point=None

        
        if (partnerName in semester.keys()):
            properties["semester"] = semester[partnerName]

            for x in semester[partnerName]:
                pro=properties.copy()
                pro['time']=x
                feature = Feature(id=i, geometry=point, properties=pro)
                collection.append(feature)

    featureColloction=FeatureCollection(collection)

    with open(sheet.name+".geojson", 'w', encoding='utf-8') as fp:
        json.dump(featureColloction, fp, ensure_ascii=False)

if __name__=="__main__":
    if sys.argv[1]:  
        readExcel(sys.argv[1])
    # readExcel(r"201718SLA projects.xls")



