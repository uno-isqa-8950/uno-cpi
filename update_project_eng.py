from UnoCPI import sqlfiles,settings
import psycopg2
import os

sql = sqlfiles
global connection
global cursor
try:
    connection = psycopg2.connect(user=settings.DATABASES['default']['USER'],
                                  password=settings.DATABASES['default']['PASSWORD'],
                                  host=settings.DATABASES['default']['HOST'],
                                  port=settings.DATABASES['default']['PORT'],
                                  database=settings.DATABASES['default']['NAME'],
                                  sslmode="require")

    if connection:
        print("Postgres SQL Database successful connection")

    cursor = connection.cursor()

    print("Executing Community Partner status inactive")

    #UPDATE Community partner to show status 'Inactive' from newly added Partner Status Table

    activityTypeDict_SL = []
        
    activityTypeDict_SL.append({'oldValue':'Meeting / Gathering','newValue':'Other'})
    activityTypeDict_SL.append({'oldValue':'Course','newValue':'Course'})
    activityTypeDict_SL.append({'oldValue':'Unpaid Services','newValue':'Other'})
    activityTypeDict_SL.append({'oldValue':'General Activity','newValue':'Course'})
    activityTypeDict_SL.append({'oldValue':'Event / Exhibit / Performance','newValue':'Course'})
    
    for x in activityTypeDict_SL:
      print(x['oldValue'],x['newValue'])
      query = "update projects_project set activity_type_id = \
        (select a.id from projects_activitytype as a where a.name = '%s') \
        where engagement_type_id = \
        (select e.id from projects_engagementtype as e where e.name = 'Service Learning') \
         and activity_type_id = \
         (select c.id from projects_activitytype as c where c.name = '%s')"
      print('query--',query)
      cursor.execute(query, (x['newValue'],x['oldValue'], ))
      
      connection.commit()

    activityTypeDict_AH = []
    activityTypeDict_AH.append({"oldValue":'Unpaid Services',"newValue":'Other'})
    activityTypeDict_AH.append({"oldValue":'Course',"newValue":'Other'})
    activityTypeDict_AH.append({"oldValue":'Event / Exhibit / Performance',"newValue":'Other'})
    activityTypeDict_AH.append({"oldValue":'Capstone',"newValue":'Other'})
    activityTypeDict_AH.append({"oldValue":'Workshop',"newValue":'Other'})
    activityTypeDict_AH.append({"oldValue":'Internships',"newValue":'Other'})

    for x in activityTypeDict_AH:
      print(x['oldValue'],x['newValue'])
      query_AH = "update projects_project set activity_type_id = \
        (select a.id from projects_activitytype as a where a.name = '%s') \
        where engagement_type_id = \
        (select e.id from projects_engagementtype as e where e.name = 'Access to Higher Education') \
         and activity_type_id = \
         (select c.id from projects_activitytype as c where c.name = '%s')"
      print('query--',query_AH)
      cursor.execute(query_AH, (x['newValue'],x['oldValue'], ))
      connection.commit()

    activityTypeDict_CM = []
    activityTypeDict_CM.append({"oldValue":'Unpaid Services',"newValue":'Other'})
    activityTypeDict_CM.append({"oldValue":'Course',"newValue":'Other'})
    activityTypeDict_CM.append({"oldValue":'General Activity',"newValue":'Other'})
    activityTypeDict_CM.append({"oldValue":'Contract Services',"newValue":'Other'})
    activityTypeDict_CM.append({"oldValue":'Training / Workshop / Presentation',"newValue":'Other'})
    activityTypeDict_CM.append({"oldValue":'Event / Exhibit / Performance',"newValue":'Other'})

    for x in activityTypeDict_CM:
      print(x['oldValue'],x['newValue'])
      query_CM = "update projects_project set activity_type_id = \
        (select a.id from projects_activitytype as a where a.name = '%s') \
        where engagement_type_id = \
        (select e.id from projects_engagementtype as e where e.name = 'Community-Based Learning') \
         and activity_type_id = \
         (select c.id from projects_activitytype as c where c.name = '%s')"
      print('query--',query_CM)
      cursor.execute(query_CM, (x['newValue'],x['oldValue'], ))
      connection.commit()

    activityTypeDict_ER = []
    activityTypeDict_ER.append({"oldValue":'Unpaid Services',"newValue":'Other'})
    activityTypeDict_ER.append({"oldValue":'Course',"newValue":'Other'})
    activityTypeDict_ER.append({"oldValue":'Contract Services',"newValue":'Other'})
    activityTypeDict_ER.append({"oldValue":'Mentoring',"newValue":'Other'})
    activityTypeDict_ER.append({"oldValue":'Workshop',"newValue":'Other'})
    activityTypeDict_ER.append({"oldValue":'Internships',"newValue":'Other'})

    for x in activityTypeDict_ER:
      print(x['oldValue'],x['newValue'])
      query_ER = "update projects_project set activity_type_id = \
        (select a.id from projects_activitytype as a where a.name = '%s') \
        where engagement_type_id = \
        (select e.id from projects_engagementtype as e where e.name = 'Engaged Research') \
         and activity_type_id = \
         (select c.id from projects_activitytype as c where c.name = '%s')"
      print('query--',query_ER)
      cursor.execute(query_ER, (x['newValue'],x['oldValue'], ))
      connection.commit()


    activityTypeDict_KR = []
    activityTypeDict_KR.append({"oldValue":'General Activity',"newValue":'Other'})
    activityTypeDict_KR.append({"oldValue":'Course',"newValue":'Other'})
    activityTypeDict_KR.append({"oldValue":'Meeting/Gathering',"newValue":'Community-oriented lecture/event'})
    activityTypeDict_KR.append({"oldValue":'Unpaid Services',"newValue":'Other'})
    activityTypeDict_KR.append({"oldValue":'Event / Exhibit / Performance',"newValue":'Community-oriented lecture/event'})
    activityTypeDict_KR.append({"oldValue":'Contract Services',"newValue":'Specialized Service Contract'})
    activityTypeDict_KR.append({"oldValue":'Training / Workshop / Presentation',"newValue":'Workshop'})
    activityTypeDict_KR.append({"oldValue":'Service Activity',"newValue":'Workshop'})
    activityTypeDict_KR.append({"oldValue":'Student Research',"newValue":'Workshop'})

    for x in activityTypeDict_KR:
      print(x['oldValue'],x['newValue'])
      query_KR = "update projects_project set activity_type_id = \
        (select a.id from projects_activitytype as a where a.name = '%s') \
        where engagement_type_id = \
        (select e.id from projects_engagementtype as e where e.name = 'Knowledge and Resource Sharing') \
         and activity_type_id = \
         (select c.id from projects_activitytype as c where c.name = '%s')"
      print('query--',query_KR)
      cursor.execute(query_KR, (x['newValue'],x['oldValue'], ))
      connection.commit()

    activityTypeDict_VL = []
    activityTypeDict_VL.append({"oldValue":'Unpaid Services',"newValue":'Service Activity'})
    activityTypeDict_VL.append({"oldValue":'Course',"newValue":'Other'})
    activityTypeDict_VL.append({"oldValue":'General Activity',"newValue":'Service Activity'})
    activityTypeDict_VL.append({"oldValue":'Contract Services',"newValue":'Other'})
    activityTypeDict_VL.append({"oldValue":'Workshop',"newValue":'Other'})
    activityTypeDict_VL.append({"oldValue":'Training / Workshop / Presentation',"newValue":'Other'})
    activityTypeDict_VL.append({"oldValue":'Meeting / Gathering',"newValue":'Other'})
   

    for x in activityTypeDict_VL:
      print(x['oldValue'],x['newValue'])
      query_VL = "update projects_project set activity_type_id = \
        (select a.id from projects_activitytype as a where a.name = '%s') \
        where engagement_type_id = \
        (select e.id from projects_engagementtype as e where e.name = 'Volunteering') \
         and activity_type_id = \
         (select c.id from projects_activitytype as c where c.name = '%s')"
      print('query--',query_VL)
      cursor.execute(query_VL, (x['newValue'],x['oldValue'], ))
     
      connection.commit()

except (psycopg2.Error) as error:
    print("Error while connecting to Postgres SQL", error)

cursor.close()
connection.close()
print("Postgres SQL connection is closed")