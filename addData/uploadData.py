#coding=utf-8
from mapbox import Geocoder
import xlrd
from partners.models import CommunityPartner, CommunityPartnerMission,CommunityType,CampusPartner
from projects.models import MedianHouseholdIncome,Project,EngagementType,ProjectMission,Status,ActivityType,AcademicYear
from projects.models import ProjectCommunityPartner,ProjectCampusPartner
from university.models import Department, College, EducationSystem, University
from home.models import MissionArea
import os
import json
from shapely.geometry import shape, Point
import pandas as pd


def planData():
    path=os.getcwd()
    with open(path+r'\home\static\GEOJSON\ID2.geojson') as f:
        geojson = json.load(f)

    df = geojson["features"]

    with open(path+r'\home\static\GEOJSON\NEcounties2.geojson') as f:
        geojson1 = json.load(f)

    county = geojson1["features"]
    return [df, county]

#A B C D E F G H I J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
#0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
def uploadProject(fileName):
    excel=xlrd.open_workbook(fileName)
    sheet=excel.sheet_by_index(0)
    rows=sheet.nrows

    for i in range(1,rows):
        lineData=sheet.row_values(i)
        projectName=lineData[0].strip()
        facilitator=lineData[6].strip()
        description=lineData[7]
        if(lineData[8].strip()==lineData[9].strip()):
            semester = lineData[8].strip()
        else:
            semester=lineData[8].strip()+"-"+lineData[9].strip()

        total_uno_students=lineData[11]
        total_uno_hours=lineData[12]
        total_k12_students=lineData[13]
        total_k12_hours=lineData[14]
        total_uno_faculty=lineData[16]
        total_other_community_members=lineData[17]

        start_date=lineData[18]
        if(start_date=='N/A'):
            start_date=None
        else:
            start_datetime=xlrd.xldate_as_datetime(start_date,0)
            start_date=start_datetime.date()

        end_date=lineData[19]
        if (end_date == 'N/A'):
            end_date = None
        else:
            end_datetime=xlrd.xldate_as_datetime(end_date,0)
            end_date=end_datetime.date()

        other_details=lineData[20]
        outcomes=lineData[21].strip()
        total_economic_impact=lineData[15]
        address_line1=""
        address_line2=""
        country=""
        city=""
        state=""
        zip=None
        # legislative_district=lineData[23].strip()
        # median_household_income
        latitude=None
        longitude=None
        academic_year=lineData[10].strip()
        activity_type=lineData[5].strip()
        engagement_type=lineData[4].strip()
        project_status = lineData[22].strip()

        missionArea=lineData[1]
        community_partner = lineData[2].strip()
        campus_partner = lineData[3].strip()
        legislative_district=None
        county=None

        try:
            # Execute table "EngagementType"
            result = EngagementType.objects.filter(name=engagement_type)
            if (result.count() == 0):
                eng = EngagementType(name=engagement_type)
                eng.save()
            engagement_type_id = EngagementType.objects.get(name=engagement_type).id

            # Execute table "Status"
            result = Status.objects.filter(name=project_status)
            if (result.count() == 0):
                st = Status(name=project_status)
                st.save()
            status_id = Status.objects.get(name=project_status).id

            # Processing table "ActivityType"
            result = ActivityType.objects.filter(name=activity_type)
            if (result.count() == 0):
                acType = ActivityType(name=activity_type)
                acType.save()
            activity_type_id = ActivityType(name=activity_type).id

            # Processing table "AcademicYear"
            result = AcademicYear.objects.filter(academic_year=academic_year)
            if (result.count() == 0):
                acdYear = AcademicYear(academic_year=academic_year)
                acdYear.save()
            academic_year_id = AcademicYear.objects.get(academic_year=academic_year).id

            # Get "address_line1,address_line2,country,state,zip,latitude,longitude" information according to "communityPartner"
            result = CommunityPartner.objects.filter(name=community_partner)
            if (result.count() > 0):
                address_line1 = result[0].address_line1
                address_line2 = result[0].address_line2
                country = result[0].country
                state = result[0].state
                zip = result[0].zip
                latitude = result[0].latitude
                longitude = result[0].longitude
                legislative_district=result[0].legislative_district
                county=result[0].county


            # Get "median_household_income" from table "MedianHouseholdIncome" according to "state"
            result = MedianHouseholdIncome.objects.filter(state=state)
            if (result.count() == 0):
                median_household_income = 0
            else:
                median_household_income = result[0].income

            # Processing table "project"
            result = Project.objects.filter(project_name=projectName)
            if (result.count() == 0):
                project = Project(project_name=projectName, facilitator=facilitator, description=description,
                                  semester=semester,county=county,legislative_district=legislative_district,
                                  total_uno_students=total_uno_students, total_uno_hours=total_uno_hours,
                                  total_k12_students=total_k12_students,
                                  total_k12_hours=total_k12_hours, total_uno_faculty=total_uno_faculty,
                                  total_other_community_members=total_other_community_members, start_date=start_date,
                                  end_date=end_date, other_details=other_details, outcomes=outcomes,
                                  total_economic_impact=total_economic_impact,
                                  address_line1=address_line1, address_line2=address_line2, country=country, city=city,
                                  state=state, zip=zip,
                                  median_household_income=median_household_income,
                                  latitude=latitude, longitude=longitude, academic_year_id=academic_year_id,
                                  activity_type_id=activity_type_id,
                                  engagement_type_id=engagement_type_id, status_id=status_id)
                project.save()
                project_id = Project.objects.get(project_name=projectName).id

                # Processing "missionArea"
                result = MissionArea.objects.filter(mission_name=missionArea)
                if (result.count() == 0):
                    msi = MissionArea(mission_name=missionArea)
                    msi.save()
                mission_id = MissionArea.objects.get(mission_name=missionArea).id
                result = ProjectMission.objects.filter(mission_type="primary", mission_id=mission_id,
                                                       project_name_id=project_id)
                if (result.count() == 0):
                    proMission = ProjectMission(mission_type="primary", mission_id=mission_id, project_name_id=project_id)
                    proMission.save()

                total_hours = total_uno_hours + total_k12_hours
                total_people = total_k12_students + total_uno_students
                wages = 9
                # Processing table "ProjectCommunityPartner"
                # Gain "community_partner_id"
                result = CommunityPartner.objects.filter(name=community_partner)
                if (result.count() > 0):
                    community_partner_id = result[0].id
                    proComPartner = ProjectCommunityPartner(total_hours=total_hours, total_people=total_people,
                                                            wages=wages, community_partner_id=community_partner_id,
                                                            project_name_id=project_id)
                    proComPartner.save()

                # Processing "ProjectCampusPartner"
                # Gain "campus_partner_id"
                result = CampusPartner.objects.filter(name=campus_partner)
                if (result.count() > 0):
                    campus_partner_id = result[0].id
                    proCampusPartner = ProjectCampusPartner(total_hours=total_hours, total_people=total_people, wages=wages,
                                                            campus_partner_id=campus_partner_id, project_name_id=project_id)
                    proCampusPartner.save()
                print("success")
        except Exception as e:
            print(e)
            print("Executing Database Error")




def uploadCommunity(fileName):
    excel=xlrd.open_workbook(fileName)
    sheet=excel.sheet_by_index(0)
    rows=sheet.nrows

    planResult=planData()
    df=planResult[0]
    countys=planResult[1]

    for i in range(1,rows):
        lineData=sheet.row_values(i)
        name=lineData[0].strip()
        website_url=lineData[7].strip()
        address_line1=lineData[1].strip()
        address_line2=lineData[2].strip()
        county=None
        country=lineData[14]
        city=lineData[3].strip()
        state=lineData[4].strip()
        zip=lineData[5]
        latitude=0
        longitude=0
        weitz_cec_part=lineData[10].strip()
        community_type=lineData[12].strip()

        phone=lineData[6]
        primary_mission=lineData[8].strip()
        secondary_mission=lineData[9].strip()

        legislative_district = None
        income=None

        result=CommunityPartner.objects.filter(name=name)
        if(result.count()==0):
            # 解析经纬度 Parsing latitude&longitude
            lalgitude = addressToCOORDINATE(address_line1, city, state)
            if (lalgitude == None):
                latitude = None
                longitude = None
            else:
                longitude = lalgitude[0]
                latitude = lalgitude[1]
                #Determine "legislative_district" according to "latitude&longtitude"
                coord=Point((float(longitude),float(latitude)))
                for d in df:
                    polygon = shape(d['geometry'])
                    if polygon.contains(coord):
                        legislative_district=d['id']

                # Gain "County"
                for m in countys:
                    polygon = shape(m['geometry'])
                    if (polygon.contains(coord)):
                        county = m['properties']['NAME']
                        income = m['properties']['Income']

            # Gain "community_type_id"
            community_type_id=None
            try:
                result = CommunityType.objects.filter(community_type=community_type)
                if (result.count() == 0):
                    cType = CommunityType(community_type=community_type)
                    cType.save()
                result = CommunityType.objects.filter(community_type=community_type)
                community_type_id = result[0].id
            except Exception as e:
                print("Error when executing communityType database")

            #Save data to "communityPartner" table 
            community_id=None
            try:
                community = CommunityPartner(name=name, website_url=website_url, address_line1=address_line1,
                                             address_line2=address_line2,county=county,legislative_district=legislative_district,
                                             country=country, city=city, state=state, zip=zip, phone=phone,
                                             latitude=latitude, longitude=longitude,income=income,
                                             active=False, weitz_cec_part=weitz_cec_part,community_type_id=community_type_id)
                community.save()
                community_id=CommunityPartner.objects.get(name=name).id
            except Exception as e:
                print("操作表CommunityPartner出现错误")


            # Set "primary_mission_id"
            try:
                result = MissionArea.objects.filter(mission_name=primary_mission)
                if (result.count() == 0):
                    mission = MissionArea(mission_name=primary_mission)
                    mission.save()
                result = MissionArea.objects.filter(mission_name=primary_mission)
                primary_id = result[0].id
                cMission=CommunityPartnerMission(mission_type="primary",community_partner_id=community_id,mission_area_id=primary_id)
                cMission.save()
            except Exception as e:
                print("Error when executing MissionArea")


            # Set "second_mission_id"
            try:
                result = MissionArea.objects.filter(mission_name=secondary_mission)
                if (result.count() == 0):
                    mission = MissionArea(mission_name=secondary_mission)
                    mission.save()
                result = MissionArea.objects.filter(mission_name=secondary_mission)
                second_id = result[0].id
                cMission=CommunityPartnerMission(mission_type="secondary",community_partner_id=community_id,mission_area_id=second_id)
                cMission.save()
            except Exception as e:
                print("Error when processing MissionArea table")


def uploadCampus(fileName):
    excel=xlrd.open_workbook(fileName)
    sheet=excel.sheet_by_index(0)
    rows=sheet.nrows

    for i in range(1,rows):
        lineData=sheet.row_values(i)
        name=lineData[0].strip()
        college=lineData[1].strip()
        department=lineData[2].strip()
        university=lineData[3].strip()
        educationSystem=lineData[4].strip()
        weitz_cec_part=lineData[5].strip()

        try:
            #Processing "EducationSystem"
            result=EducationSystem.objects.filter(name=educationSystem)
            if (result.count() == 0):
                eduSystem=EducationSystem(name=educationSystem)
                eduSystem.save()
            education_system_id=EducationSystem.objects.get(name=educationSystem).id

            # Processing "University"
            result=University.objects.filter(name=university,education_system_id=education_system_id)
            if (result.count() == 0):
                univ=University(name=university,education_system_id=education_system_id)
                univ.save()
            university_id=University.objects.get(name=university,education_system_id=education_system_id).id

            # Processing "College"
            result=College.objects.filter(college_name=college,university_id=university_id)
            if(result.count()==0):
                col=College(college_name=college,university_id=university_id)
                col.save()
            college_name_id=College.objects.get(college_name=college,university_id=university_id).id

            # Processing "Department"
            result=Department.objects.filter(department_name=department,college_name_id=college_name_id)
            if(result.count()==0):
                dep=Department(department_name=department,college_name_id=college_name_id)
                dep.save()
            department_id=Department.objects.get(department_name=department,college_name_id=college_name_id).id

            #Processing "CamputnersPartner"
            result=CampusPartner.objects.filter(name=name)
            if(result.count()==0):
                camp=CampusPartner(name=name,weitz_cec_part=weitz_cec_part,active=False,college_name_id=college_name_id,
                                   department_id=department_id,education_system_id=education_system_id,university_id=university_id)
                camp.save()
        except Exception as e:
            print(e)
            print("Error when processing database")


#Processing only once while initiating the data of "MedianHouseholdIncome"
def InitMedianHouseholdIncome():
    path=os.getcwd() + r"\addData\file\median_household_income.xlsx"
    excel=xlrd.open_workbook(path)
    sheet=excel.sheet_by_index(0)

    for i in range(2,54):
        lineData=sheet.row_values(i)
        state=lineData[1].strip()
        income=lineData[2]
        try:
            result=MedianHouseholdIncome.objects.filter(state=state)
            if(result.count()==0):
                median=MedianHouseholdIncome(state=state,income=income)
                median.save()
        except Exception as e:
            print("表MedianHouseholdIncome操作异常")



# Gain Geo information by "address"
def addressToCOORDINATE(address,city,state):
    detail=""
    if (address != "N/A"):
        detail += address
        if (city != "N/A"):
            detail += " "+city
            if (state != "N/A"):
                detail +=","+ state

    print(detail)
    try:
        geocoder = Geocoder(access_token="pk.eyJ1IjoibG9va3VwbWFuIiwiYSI6ImNqbW41cmExODBxaTEzeHF0MjhoZGg1MnoifQ.LGL5d5zGa1z6ms-IVyn7sw")
        response = geocoder.forward(detail, limit=1)
        if(response.status_code==200):
            collection = response.json()
            result=collection['features'][0]["geometry"]['coordinates']
            return result
        else:
            return None
    except Exception as e:
        print("Parsing Error")
        print(e)
        return None

