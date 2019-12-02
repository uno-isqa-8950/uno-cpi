from UnoCPI import sqlfiles,settings
import psycopg2
import os
import csv
import xlrd
import datetime

sql = sqlfiles
global connection
global cursor

   # a file in the current directory to read the investments
FILENAME = "Subcategories_Projects.xls"
    
# read content from file
def read_content():
    projects = []
    wb = xlrd.open_workbook(FILENAME) 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0) 
    total_proj_count = 0
    #for i in range(1,2): 
    for i in range(sheet.nrows): 
      project = {}
      project['name'] = sheet.cell_value(i, 0)
      project['mission'] = sheet.cell_value(i, 1)
      project['subcat'] = sheet.cell_value(i, 2)
      project['comm'] = sheet.cell_value(i, 3)
      project['campus'] = sheet.cell_value(i, 4)
      project['eng'] = sheet.cell_value(i, 5)
      project['strt_acd_yr'] = sheet.cell_value(i, 6)

      print(str(project['name']), str(project['mission']))
      if str(project['name']) == 'Projects' and str(project['mission']) == 'Mission Areas':
        print('skip the header')
      else:
        total_proj_count = total_proj_count + 1
        projects.append(project)      
  
    print(str(total_proj_count), " read projects")
    return projects

# function to open add investment page to add investment details.
def addInvestments():

  projects =  read_content() # read the content from csv file
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

        for i in projects:     # iterate the adding operation for records present in csv files      
            comm_list = []
            camp_list = []
            comm = i['comm']
            camp = i['campus']

            if comm.split('  ') is not None:
               for x in comm.split('  '):
                  if x != '':
                    comm_list.append(x)
            else:
              comm_list.append(comm)

            if camp.split('  ') is not None:
               for x in camp.split('  '):
                  if x != '':
                    camp_list.append(x)
            else:
              camp_list.append(camp)

            i['comm_list'] = comm_list
            i['camp_list'] = camp_list
            #print('project--',i)               
        proj_count = 0
        proj_notfound  = 0
        proj_nosubCat = 0
        for x in projects:
          #print('project--',x) 
          mission_name = x['mission']
          print('before split mission_name --',mission_name)
          mission_name = str(mission_name).split(':')[1]
         #print('after split mission_name --',mission_name)
          proj_name = x['name']
          proj_name = str(proj_name).replace("'","''")
          print('proj_name--',proj_name)
          subcat_name = x['subcat']
          subcat_name = str(subcat_name).replace("'","''")
          acd_yr = x['strt_acd_yr']
          engName = x['eng']

          comm_list = x['comm_list']
          comm_name_list = '('

          camp_list = x['camp_list']
          camp_name_list = '('

          if comm_list is not None:
            name_count = 0
            if len(comm_list) > 0:
              for c in comm_list:
                      commName = str(c).replace("'","''")
                      comm_name_list = comm_name_list + str('\'') + str(commName) + str('\'')
                      if name_count < len(comm_list) - 1:
                          comm_name_list = comm_name_list + str(",")
                          name_count = name_count + 1
              
              comm_name_list = comm_name_list + ')'

          if camp_list is not None:
            name_count = 0
            if len(camp_list) > 0:
              for c in camp_list:
                      campName = str(c).replace("'","''")
                      camp_name_list = camp_name_list + str('\'') + str(campName) + str('\'')
                      if name_count < len(camp_list) - 1:
                          camp_name_list = camp_name_list + str(",")
                          name_count = name_count + 1
              
              camp_name_list = camp_name_list + ')'

          #print('comm_name_list---',comm_name_list)
          #print('camp_name_list---',camp_name_list)
          projectId = 0
          subCatId = 0
          subMissnId = 0
          othersubCat = []

          if subcat_name is not None and subcat_name != '':
                
                select_proj="select distinct p.id, p.other_sub_category \
                from projects_project p , \
                projects_projectmission pm, \
                projects_projectcampuspartner pcam, \
                projects_projectcommunitypartner pcomm \
                where p.id = pm.project_name_id and pm.mission_type = 'Primary' \
                and pm.mission_id = (select id from home_missionarea m where mission_name = '"+str(mission_name).strip()+"') \
                and p.id = pcam.project_name_id and \
                pcam.campus_partner_id in (select id from partners_campuspartner where name in "+camp_name_list+") \
                and p.id = pcomm.project_name_id and \
                pcomm.community_partner_id in (select id from partners_communitypartner where name in "+comm_name_list+") \
                and p.academic_year_id = (select id from projects_academicyear where academic_year = '"+str(acd_yr)+"') and \
                p.engagement_type_id = (select id from projects_engagementtype where name ='"+str(engName)+"') \
                and p.project_name like '"+str(proj_name).strip()+"%'"
               
                #print('select_proj---',select_proj)
                cursor.execute(select_proj)#,[mission_name,camp_name_list,comm_name_list,acd_yr,engName,proj_name])
                
                for obj in cursor.fetchall():
                  print('project id --',obj[0])
                  projectId = obj[0]
                  othersubCat = obj[1]
                  print('othersubCat--',othersubCat)
                  print('projectId--',projectId)

                if projectId !=0:
                      select_subcat = "select id from projects_subcategory where upper(sub_category) ='"+str(subcat_name).upper()+"'"
                      #print('select_subcat---',select_subcat)
                      cursor.execute(select_subcat)
                      for obj in cursor.fetchall():
                        #print('subCatId --',obj[0])
                        subCatId = obj[0]

                      print('subCatId -111-',subCatId)
                      if subCatId !=0:
                           select_subcat_msn = "select secondary_mission_area_id from projects_missionsubcategory where sub_category_id ="+str(subCatId)+""
                           #print('select_subcat_msn---',select_subcat_msn)
                           cursor.execute(select_subcat_msn)
                           for obj in cursor.fetchall():
                              print('subMissnId --',obj[0])
                              subMissnId = obj[0]

                      else:
                          select_other_subcat = "select id from projects_subcategory where upper(sub_category) ='OTHER'"
                          #print('select_other_subcat---',select_other_subcat)
                          cursor.execute(select_other_subcat)
                          for obj in cursor.fetchall():
                              print('sub other cat id --',obj[0])
                              subCatId = obj[0]

                      print('subCatId -222-',subCatId)
                      print('subMissnId--',subMissnId)
                      if subCatId != 0:
                          proj_subcatExist = "select id from projects_projectsubcategory \
                          where sub_category_id ="+str(subCatId)+" and project_name_id ="+str(projectId)
                          cursor.execute(proj_subcatExist)
                          result = cursor.fetchall()
                          if len(result) >0:
                            print('mapping already exists')
                          else:                            
                            currdate =datetime.datetime.now()
                            select_max_subid = "select max(id) from projects_projectsubcategory"
                            subPrimaryId = 0
                            cursor.execute(select_max_subid)
                            for id in cursor.fetchall():
                              subPrimaryId = id[0]

                            subPrimaryId = subPrimaryId + 1
                            cursor.execute("insert into projects_projectsubcategory \
                              (id, sub_category_id,project_name_id,created_date,updated_date) VALUES (%s, %s, %s, %s,%s)",(str(subPrimaryId),str(subCatId),str(projectId),str(currdate),str(currdate)))
                            connection.commit()
                      
                      if subMissnId !=0:
                          proj_missionExist = "select id from projects_projectmission \
                          where mission_type = 'Other' and mission_id ="+str(subMissnId)+" and project_name_id ="+str(projectId)
                          cursor.execute(proj_missionExist)
                          missionresult = cursor.fetchall()
                          if len(missionresult) >0:
                            print('mission mapping already exists')
                          else:
                            select_max_id = "select max(id) from projects_projectmission"
                            misnId = 0
                            cursor.execute(select_max_id)
                            for id in cursor.fetchall():
                              misnId = id[0]

                            misnId = misnId + 1
                            insert_project_other_mission = "insert into projects_projectmission( \
                            mission_type,id,mission_id,project_name_id) values('Other',"+str(misnId)+","+str(subMissnId)+","+str(projectId)+")"
                            #print('insert_project_other_mission --',insert_project_other_mission)
                            cursor.execute(insert_project_other_mission)
                            connection.commit()
                      else:
                          if othersubCat is None or othersubCat == '':
                             othersubCat= []

                          if subcat_name is not None:
                              othersubCat.append(subcat_name)                        
                              update_proj_other_sub_desc = "update projects_project \
                              set other_sub_category = %s where id = %s"
                              #print('tuple(othersubCat)--',othersubCat)
                              #print('update_proj_other_sub_desc --',update_proj_other_sub_desc)
                              cursor.execute(update_proj_other_sub_desc,(othersubCat,projectId))
                              connection.commit()

                      proj_count = proj_count +1
                      print(str(proj_name) + " has been updated with "+str(subcat_name))
                else:
                    print(str(proj_name) + " not found in database ")
                    proj_notfound = proj_notfound + 1

          else:
            print(str(proj_name) + " has no sub sub_category "+str(subcat_name))
            proj_nosubCat = proj_nosubCat + 1


        print(str(proj_count) + " has been updated")
        print(str(proj_notfound) + " not found in database")
        print(str(proj_nosubCat) + " has not sub sub_category")
        cursor.close()
        connection.close()
  except (psycopg2.Error) as error:
      print("Error while connecting to Postgres SQL", error)

def main():
  addInvestments()

main()