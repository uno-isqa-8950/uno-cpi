#coding=utf-8
from geojson import FeatureCollection,Feature,Point
import sys
import os
import json
from partners.models import CommunityPartner,CommunityType,CommunityPartnerMission
from projects.models import Project

def databaseToCommunityAndK12(path):
    communityPartners=CommunityPartner.objects.all()

    if(communityPartners.count()>0):
        community_i=0
        k12_i=0
        community_collection=[]
        k12_collection=[]
        for community in communityPartners:
            properties={}

            try:
                longitude = float(community.longitude)
                latitude = float(community.latitude)
            except Exception as e:
                longitude=None
                latitude=None

            properties['Latitude'] = latitude
            properties['Longitude'] = longitude

            # change to Geo information
            try:
                if(longitude!=None and latitude!=None):
                    point = Point((longitude, latitude))
                else:
                    point=[]
            except Exception as ex:
                point=[]
                print(e)

            primary_mission = ""
            secondary_mission = ""
            mission = community.communitypartnermission.filter()
            for mis in mission:
                if (mis.mission_type == 'primary'):
                    primary_mission = mis.mission_area.mission_name
                elif (mis.mission_type == "secondary"):
                    secondary_mission = mis.mission_area.mission_name

            properties["PrimaryMissionFocus"] = primary_mission
            properties["SecondaryMissionFocus"] = secondary_mission

            Website = community.website_url
            properties["Website"] = Website

            address_line1 = community.address_line1
            properties['Address'] = address_line1

            address_line2 = community.address_line2
            properties['Address2'] = address_line2

            city = community.city
            properties['City'] = city

            state = community.state
            properties['State'] = state

            zip = community.zip
            properties['Zip'] = zip

            phoneNumber = community.phone
            properties['PhoneNumber'] = phoneNumber

            weitzCECPartner = community.weitz_cec_part
            properties['WeitzCECPartner'] = weitzCECPartner

            county = community.county
            properties['County'] = county

            district = community.legislative_district
            properties['district'] = district

            income = community.income
            properties['income'] = income

            semster = []

            # Get semester projectcommunitypartner_set.all()[0].project_name.semester
            his_projects = community.projectcommunitypartner_set.all()
            for pro in his_projects:
                semsters = pro.project_name.semester
                semster.append(semsters)

            properties['semester'] = semster

            # if it is "communityPartner"
            if (community.community_type.community_type != "K-12"):
                name = community.name
                properties["CommunityPartner"] = name
                for pro in his_projects:
                    semesters = pro.project_name.semester
                    semes = semesters.split("-")
                    for every in semes:
                        this_properties=properties.copy()
                        this_properties['time']=every
                        feature=Feature(id=community_i,geometry=point,properties=this_properties)
                        community_collection.append(feature)
                        community_i+=1
            else: #if it is "K12Partner"
                name = community.name
                properties["K-12 Partner"] = name
                for pro in his_projects:
                    semesters = pro.project_name.semester
                    semes = semesters.split("-")
                    for every in semes:
                        this_properties=properties.copy()
                        this_properties['time']=every
                        feature=Feature(id=k12_i,geometry=point,properties=this_properties)
                        k12_collection.append(feature)
                        k12_i+=1

        featureColloction=FeatureCollection(community_collection)
        print(path+r'\CommunityPartner.geojson')
        # print(featureColloction)
        with open(path+r"\CommunityPartner.geojson",'w',encoding='utf-8') as fp:
            json.dump(featureColloction,fp,ensure_ascii=False)
            print("create CommunityPartner.geojson successful")

        featureColloction = FeatureCollection(k12_collection)
        # print(featureColloction)
        with open(path + r"\K12Partner.geojson", 'w', encoding='utf-8') as fp:
            json.dump(featureColloction, fp, ensure_ascii=False)
            print("create K12Partner.geojson successful")



def databaseToProject(path):
    projects=Project.objects.all()

    if(projects.count()>0):
        collection=[]
        i=0
        for project in projects:
            properties = {}

            try:
                longitude=float(project.longitude)
                latitude=float(project.latitude)
            except Exception as e :
                longitude=''
                latitude=''

            properties['Longitude']=longitude
            properties['Latitude']=latitude

            # Change to Geo information
            if(longitude!='' and latitude!=''):
                point = Point((longitude, latitude))
                print(point)
            else:
                point=[]

            address_line1=project.address_line1
            address_line2=project.address_line2
            properties['Address']=address_line1
            properties['Address2']=address_line2

            state=project.state
            properties['State']=state

            zip=project.zip
            properties['Zip']=zip

            try:
                primary_mission=project.projectmission_set.filter()[0].mission.mission_name

            except Exception as e:
                print(e)
                primary_mission='N/A'

            properties['PrimaryMission']=primary_mission

            project_mission = primary_mission
            properties['ProjectMission']=project_mission

            totalK12Hours=project.total_k12_hours
            properties['totalK12Hours']=totalK12Hours

            totalOfNumberK12Member=project.total_k12_students
            properties['totalOfNumberK12Member']=totalOfNumberK12Member

            totalUnoStudent=project.total_uno_students
            properties['Total Of Number UNO Student']=totalUnoStudent

            total_uno_hours=project.total_uno_hours
            properties['Total UNO Students Hours']=total_uno_hours

            engagementType=project.engagement_type.name
            properties['EngagementType']=engagementType

            academicYear=project.academic_year.academic_year
            properties['AcademicYear']=academicYear

            status=project.status.name
            properties['Status']=status

            activityType=project.activity_type
            properties['ActivityType']=activityType

            district=project.legislative_district
            properties['district']=district

            income=project.median_household_income
            properties['income']=income

            county=project.county
            properties['county']=county



            try:
                communityPartner=project.projectcommunitypartner_set.filter()[0].community_partner.name

                website=project.projectcommunitypartner_set.filter()[0].community_partner.website_url

                campusPartner=project.projectcampuspartner_set.filter()[0].campus_partner.name
            except Exception as e:
                print("No matching data in database")
                communityPartner='N/A'
                website='N/A'
                campusPartner='N/A'

            properties['CommunityPartner']=communityPartner
            properties['CampusPartner']=campusPartner
            properties['Website']=website

            semester = project.semester
            properties['semester'] = semester
            sems = semester.split("-")
            for every in sems:
                this_properties = properties.copy()
                this_properties['time'] = every
                feature = Feature(id=i, geometry=point, properties=this_properties)
                collection.append(feature)
                i += 1

        featureColloction = FeatureCollection(collection)
        # print(path + r'\Projects.geojson')
        # print(featureColloction)
        with open(path + r"\Projects.geojson", 'w', encoding='utf-8') as fp:
            json.dump(featureColloction, fp, ensure_ascii=False)
            print("create Projects.geojson successful")
















