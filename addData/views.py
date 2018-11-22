from django.shortcuts import render
from django.http import HttpResponse
from addData import uploadData,databaseToGeojson
import os

# Create your views here.
def test(requeset):
    uploadData.InitMedianHouseholdIncome()
    uploadData.uploadCommunity(os.getcwd()+r"\addData\file\Community_Partner.xlsx")
    uploadData.uploadCampus(os.getcwd()+r"\addData\file\Campus_Partner.xlsx")
    uploadData.uploadProject(os.getcwd()+r"\addData\file\Projects.xlsx")
    databaseToGeojson.databaseToCommunityAndK12(os.getcwd()+r"\addData\static\GEOJSON")
    databaseToGeojson.databaseToProject(os.getcwd()+r"\addData\static\GEOJSON")
    return HttpResponse("ok")