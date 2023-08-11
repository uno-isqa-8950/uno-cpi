#This file holds SQL used around the project.

#This query is for myprojects for campus partners and community partners
my_projects="""
select distinct p.project_name
                          ,array_agg(distinct hm.mission_name) mission_area
                          ,array_agg(distinct pc.name) CommPartners
                            ,array_agg(distinct c.name) CampPartners
                            ,array_agg(distinct e.name) engagement_type 
                            ,pa.academic_year
                            ,p.semester
                            ,ps.name status
                          ,case when p.start_date is null then 'None' end start_date
                            ,case when p.end_date is null then 'None' end end_date
                            ,p.outcomes
                            ,p.total_uno_students
                            ,p.total_uno_hours
                            ,p.total_uno_faculty
                            ,p.total_k12_students
                            ,p.total_k12_hours
                            ,p.total_other_community_members
                            ,a.name activity_type
                            ,p.description
							,p.id
                            ,p.project_type project_type
                            ,p.end_semester end_semester
                            , ea.academic_year end_academic_year
                            , array_agg(distinct s.sub_category) sub_category
                            ,  p.campus_lead_staff campus_lead_staff
                            , hm.mission_image_url mission_image
                            ,p.other_activity_type act_type
                            ,p.other_sub_category other_subCat
                        from projects_project p
                          left join projects_projectmission m on p.id = m.project_name_id and lower(m.mission_type) = 'primary' 
                          left join home_missionarea hm on hm.id = m.mission_id
                          left join projects_engagementtype e on e.id = p.engagement_type_id
                            left join projects_projectcommunitypartner pp on p.id = pp.project_name_id
                          left join partners_communitypartner pc on pp.community_partner_id = pc.id
                            left join projects_projectcampuspartner pp2 on p.id = pp2.project_name_id
                            left join partners_campuspartner c on pp2.campus_partner_id = c.id
                            inner join projects_academicyear pa on p.academic_year_id = pa.id
                            left join projects_academicyear ea on p.end_academic_year_id = ea.id
                            inner join projects_status ps on p.status_id = ps.id
                            left join projects_activitytype a on p.activity_type_id = a.id
                            left join projects_projectsubcategory psub on psub.project_name_id = p.id
                            left join projects_subcategory s on psub.sub_category_id = s.id
                            left join projects_status status on status.id = p.status_id
                        where status.name != 'Drafts' and p.id = ANY(%s)       
                        group by p.project_name
							,p.id
                            ,pa.academic_year
                            ,p.semester
                            ,ps.name
                            ,p.start_date
                            ,p.end_date
                            ,p.outcomes
                            ,p.total_uno_students
                            ,p.total_uno_hours
                            ,p.total_uno_faculty
                            ,p.total_k12_students
                            ,p.total_k12_hours
                            ,p.total_other_community_members
                            ,a.name
                            ,p.description
                            , project_type
                            , end_semester
                            , end_academic_year
                            ,campus_lead_staff
                            ,mission_image
                        order by p.project_name;
"""

#This query is for returning draft projects for campus partners or community partners
my_drafts="""
select distinct p.project_name
                          ,array_agg(distinct hm.mission_name) mission_area
                          ,array_agg(distinct pc.name) CommPartners
                            ,array_agg(distinct c.name) CampPartners
                            ,array_agg(distinct e.name) engagement_type 
                            ,pa.academic_year
                            ,p.semester
                            ,ps.name status
                          ,case when p.start_date is null then 'None' end start_date
                            ,case when p.end_date is null then 'None' end end_date
                            ,p.outcomes
                            ,p.total_uno_students
                            ,p.total_uno_hours
                            ,p.total_uno_faculty
                            ,p.total_k12_students
                            ,p.total_k12_hours
                            ,p.total_other_community_members
                            ,a.name activity_type
                            ,p.description
							,p.id
                            ,p.project_type project_type
                            ,p.end_semester end_semester
                            , ea.academic_year end_academic_year
                            , array_agg(distinct s.sub_category) sub_category
                            ,  p.campus_lead_staff campus_lead_staff
                            , hm.mission_image_url mission_image
                            ,p.other_activity_type act_type
                            ,p.other_sub_category other_subCat
            
                        from projects_project p
                          left join projects_projectmission m on p.id = m.project_name_id and lower(m.mission_type)='primary'
                          left join home_missionarea hm on hm.id = m.mission_id
                          left join projects_engagementtype e on e.id = p.engagement_type_id
                            left join projects_projectcommunitypartner pp on p.id = pp.project_name_id
                          left join partners_communitypartner pc on pp.community_partner_id = pc.id
                            left join projects_projectcampuspartner pp2 on p.id = pp2.project_name_id
                            left join partners_campuspartner c on pp2.campus_partner_id = c.id
                            inner join projects_academicyear pa on p.academic_year_id = pa.id
                            left join projects_academicyear ea on p.end_academic_year_id = ea.id
                            inner join projects_status ps on p.status_id = ps.id
                            left join projects_activitytype a on p.activity_type_id = a.id
                            left join projects_projectsubcategory psub on psub.project_name_id = p.id
                            left join projects_subcategory s on psub.sub_category_id = s.id
                            left join projects_status status on status.id = p.status_id
                        where status.name = 'Drafts' and p.id = ANY(%s)       
                        group by p.project_name
							,p.id
                            ,pa.academic_year
                            ,p.semester
                            ,ps.name
                            ,p.start_date
                            ,p.end_date
                            ,p.outcomes
                            ,p.total_uno_students
                            ,p.total_uno_hours
                            ,p.total_uno_faculty
                            ,p.total_k12_students
                            ,p.total_k12_hours
                            ,p.total_other_community_members
                            ,a.name
                            ,p.description
                            , project_type
                            , end_semester
                            , end_academic_year
                            ,campus_lead_staff
                            ,mission_image
                        order by p.project_name;
"""

def showSelectedProjects():
	return ( """select distinct p.project_name 
                                , array_agg(distinct hm.mission_name) mission_area 
                                , array_agg(distinct pc.name) CommPartners 
                                , array_agg(distinct c.name) CampPartners 
                                , array_agg(distinct e.name) engagement_type 
                                , pa.academic_year 
                                , p.semester 
                                , status.name status 
                                , case when p.start_date is null then 'None' end start_date 
                                , case when p.end_date is null then 'None' end end_date 
                                , p.outcomes 
                                , p.total_uno_students 
                                , p.total_uno_hours 
                                , p.total_uno_faculty 
                                , p.total_k12_students 
                                , p.total_k12_hours 
                                , p.total_other_community_members 
                                , a.name activity_type 
                                , p.description 
                                , p.project_type project_type 
                                , p.end_semester end_semester 
                                , ea.academic_year end_academic_year 
                                , array_agg(distinct s.sub_category) sub_category 
                                , p.campus_lead_staff campus_lead_staff 
                                , hm.mission_image_url mission_image 
                                , p.other_activity_type act_type 
                                , p.other_sub_category other_subCat
                                , array_agg(distinct s.sub_category_tags) sub_tags
                                from projects_project p 
                                left join projects_projectmission m on p.id = m.project_name_id and lower(m.mission_type) = 'primary' 
                                left join home_missionarea hm on hm.id = m.mission_id 
                                left join projects_engagementtype e on e.id = p.engagement_type_id 
                                left join projects_projectcommunitypartner pp on p.id = pp.project_name_id 
                                left join partners_communitypartner pc on pp.community_partner_id = pc.id 
                                left join projects_projectcampuspartner pp2 on p.id = pp2.project_name_id 
                                left join partners_campuspartner c on pp2.campus_partner_id = c.id 
                                left join projects_academicyear pa on p.academic_year_id = pa.id 
                                left join projects_academicyear ea on p.end_academic_year_id = ea.id 
                                left join projects_activitytype a on p.activity_type_id = a.id 
                                left join projects_projectsubcategory psub on psub.project_name_id = p.id 
                                left join projects_subcategory s on psub.sub_category_id = s.id 
                                left join projects_status status on status.id = p.status_id 
                                where status.name !='Drafts' and  p.id in %s
                        group by p.project_name 
                                  , pa.academic_year \
                                  , p.semester 
                                  , status.name 
                                  , p.start_date 
                                  , p.end_date 
                                  , p.outcomes 
                                  , p.total_uno_students 
                                  , p.total_uno_hours 
                                  , p.total_uno_faculty 
                                  , p.total_k12_students 
                                  , p.total_k12_hours 
                                  , p.total_other_community_members 
                                  , a.name 
                                  , p.description 
                                  , project_type 
                                  , end_semester 
                                  , end_academic_year 
                                  , campus_lead_staff 
                                  , mission_image 
                                  , act_type 
                                  , other_subCat 
                                  order by pa.academic_year desc;""" )

def checkProjectsql():
    return ("""SELECT  distinct p.project_name as project_names, 
                        array_agg(distinct pc.name) As pcnames,
                                        pa.academic_year, 
                           array_agg(distinct c.name) As cnames,
                                array_agg(distinct p.id)
FROM projects_project p
left join projects_projectcommunitypartner pp on p.id = pp.project_name_id
                            left join partners_communitypartner pc on pp.community_partner_id = pc.id
                            left join projects_projectcampuspartner pp2 on p.id = pp2.project_name_id
                            left join partners_campuspartner c on pp2.campus_partner_id = c.id
                            inner join projects_academicyear pa on p.academic_year_id = pa.id
                            where lower(p.project_name) LIKE %s
                            AND pc.name LIKE %s
                            AND c.name LIKE %s
                            AND (p.academic_year_id <= %s
                            AND (COALESCE(p.end_academic_year_id,p.academic_year_id) >= %s))
GROUP BY project_names, pa.academic_year, p.id
ORDER BY pa.academic_year DESC;
""")

community_private_report = """
select pc.name commpartners
  ,array_agg(distinct hm.mission_name) mission
  ,count(distinct p.project_name) Projects
  , pc.website_url website
  , array_agg(distinct p.id) ProjectID
  , pc.partner_status_id CommStatus
  , ps.name cstatus
from partners_communitypartner pc 
 join projects_projectcommunitypartner pcp on pc.id = pcp.community_partner_id
left join projects_project p on p.id = pcp.project_name_id
left join projects_projectcampuspartner pcam on pcam.project_name_id = p.id
left join partners_communitypartnermission CommMission on CommMission.community_partner_id = pc.id and  CommMission.mission_type='Primary'
left join home_missionarea hm on hm.id = CommMission.mission_area_id
left join partners_campuspartner c on pcam.campus_partner_id = c.id 
left join partners_partnerstatus ps on ps.id = pc.partner_status_id 
left join projects_status s on s.id = p.status_id
where  s.name != 'Drafts'
and pc.community_type_id::text like %s
 and((p.academic_year_id <= %s))
 and  pcam.campus_partner_id::text like %s  
 and COALESCE(pc.legislative_district::TEXT,'0') LIKE %s    
 and c.college_name_id::text like %s 
 and pc.cec_partner_status_id in (select id from partners_cecpartnerstatus where name like %s)     

group by commpartners, website, CommStatus, cstatus
order by commpartners;"""

selected_community_public_report = """
select pc.name commpartners
  ,array_agg(distinct hm.mission_name) mission
  ,COALESCE (count(distinct p.project_name),0) Projects
  , pc.website_url website
  , pc.partner_status_id CommStatus
  , ps.name cstatus
  , array_agg(distinct p.id) ProjectID
from partners_communitypartner pc 
 join projects_projectcommunitypartner pcp on pc.id = pcp.community_partner_id
left join projects_project p on p.id = pcp.project_name_id
left join projects_projectcampuspartner pcam on pcam.project_name_id = p.id
left join partners_communitypartnermission CommMission on CommMission.community_partner_id = pc.id and  CommMission.mission_type='Primary'
left join home_missionarea hm on hm.id = CommMission.mission_area_id
left join partners_campuspartner c on pcam.campus_partner_id = c.id 
left join partners_partnerstatus ps on ps.id = pc.partner_status_id 
left join projects_status s on s.id = p.status_id
where  s.name != 'Drafts' 
and pc.id in %s  

group by commpartners, website, CommStatus, cstatus
order by commpartners;
"""

selected_One_community_public_report = """
select pc.name commpartners
  ,array_agg(distinct hm.mission_name) mission
  ,COALESCE (count(distinct p.project_name),0) Projects
  , pc.website_url website
  , pc.partner_status_id CommStatus
  , ps.name cstatus
  , array_agg(distinct p.id) ProjectID
from partners_communitypartner pc 
left join projects_projectcommunitypartner pcp on pc.id = pcp.community_partner_id
left join projects_project p on p.id = pcp.project_name_id
left join projects_projectcampuspartner pcam on pcam.project_name_id = p.id
left join partners_communitypartnermission CommMission on CommMission.community_partner_id = pc.id and  CommMission.mission_type='Primary'
left join home_missionarea hm on hm.id = CommMission.mission_area_id
left join partners_campuspartner c on pcam.campus_partner_id = c.id
left join partners_partnerstatus ps on ps.id = pc.partner_status_id 
left join projects_status s on s.id = p.status_id
where  s.name != 'Drafts' 
and pc.id::text = %s  

group by commpartners, website, CommStatus, cstatus
order by commpartners;
"""

community_public_report = """
select pc.name commpartners
  ,array_agg(distinct hm.mission_name) mission
  ,COALESCE (count(distinct p.project_name),0) Projects
  , pc.website_url website
  , pc.partner_status_id CommStatus
  , ps.name cstatus
  , array_agg(distinct p.id) ProjectID
from partners_communitypartner pc 
left join projects_projectcommunitypartner pcp on pc.id = pcp.community_partner_id
left join projects_project p on p.id = pcp.project_name_id
left join projects_projectcampuspartner pcam on pcam.project_name_id = p.id
left join partners_communitypartnermission CommMission on CommMission.community_partner_id = pc.id and  CommMission.mission_type='Primary'
left join home_missionarea hm on hm.id = CommMission.mission_area_id
left join partners_campuspartner c on pcam.campus_partner_id = c.id
left join partners_partnerstatus ps on ps.id = pc.partner_status_id
left join projects_status s on s.id = p.status_id
where  s.name != 'Drafts' 
and pc.community_type_id::text like %s
 and((p.academic_year_id <= %s))
 and  pcam.campus_partner_id::text like %s  
 and COALESCE(pc.legislative_district::TEXT,'0') LIKE %s    
 and c.college_name_id::text like %s  
and pc.cec_partner_status_id in (select id from partners_cecpartnerstatus where name like %s)     

group by commpartners, website, CommStatus, cstatus
order by commpartners;
"""

def createproj_othermission():
    return ("select secondary_mission_area_id from projects_missionsubcategory pms inner join projects_subcategory ps on ps.id = pms.sub_category_id where ps.sub_category = %s")

def createproj_addothermission():
    return ( """insert into projects_projectmission (mission_type,mission_id,project_name_id) values ('Other',%s,%s); """)


primaryFocusTopic_report_sql='''
select rec_type, focus_id, focus_name, focus_desc, 
       focus_image_url, focus_color, 
       topic_id, topic_name, topic_desc,
       proj proj_count, proj_ids proj_list, 
       comm comm_count, comm_id comm_list,
       camp camp_count,
       unostu, unohr,
       k12stu, k12hr
from ((with focus_filter as (select pm.mission_id focus_id
                                  , m.mission_name focus_area_name			   
                                  , count(distinct p.project_name) Projects
                                  , array_agg(distinct p.id) projects_id
                                  , count(distinct pcomm.community_partner_id) CommPartners
                                  , array_agg(distinct pcomm.community_partner_id) CommPartners_id
                                  , count(distinct pcamp.campus_partner_id) CampPartners
                                  , sum(p.total_uno_students) numberofunostudents
                                  , sum(p.total_uno_hours) unostudentshours
                                  , sum(p.total_k12_students) numberofk12students
                                  , sum(p.total_k12_hours) k12studentshours
                             from home_missionarea m
                                 left join projects_projectmission pm on m.id = pm.mission_id
                                 left join projects_project p on pm.project_name_id = p.id
                                 left join projects_projectengagementactivity pea on pea."ProjectName_id" = p.id
                                 left join projects_engagementactivitytype ea on ea.id = pea."ProjectEngagementActivityName_id"
                                 left join projects_projectcampuspartner pcamp on pcamp.project_name_id = p.id
                                 left join projects_projectcommunitypartner pcomm on pcomm.project_name_id = p.id
                                 left join partners_communitypartner comm on comm.id = pcomm.community_partner_id
                                 left join projects_status s on s.id = p.status_id	
                                 left join partners_campuspartner c on pcamp.campus_partner_id = c.id  
                             where COALESCE(s.name,'None') != 'Drafts'
                               and COALESCE(pm.mission_id::text,'None') like %s
                               and COALESCE(comm.community_type_id::text,'None') like %s
                               and COALESCE(pcamp.campus_partner_id::text,'None') like %s
                               and COALESCE(c.college_name_id::text,'None') like %s
                               and COALESCE(ea."EngagementTypeName_id"::text,'None') like %s
                               and ((p.academic_year_id <= %s) AND 
                                    (COALESCE(p.end_academic_year_id,p.academic_year_id) >= %s))
                               and COALESCE(comm.cec_partner_status_id,(select id from partners_cecpartnerstatus where name like 'Never')) in  (select id from partners_cecpartnerstatus where name like %s)
                               and COALESCE(c.cec_partner_status_id,(select id from partners_cecpartnerstatus where name like 'Never')) in (select id from partners_cecpartnerstatus where name like %s)                                    
                             group by focus_area_name, focus_id
                             order by focus_area_name)
       Select distinct 'Focus' rec_type
                     , focus.id focus_id
                     , focus.mission_name focus_name
                     , COALESCE(focus.description,'None') focus_desc
                     , focus.mission_image_url focus_image_url
                     , focus.mission_color focus_color                     
                     , -1 topic_id
                     , 'None' topic_name
                     , 'None' topic_desc	      
                     , COALESCE(focus_filter.Projects, 0) proj
                     , focus_filter.projects_id proj_ids
                     , COALESCE(focus_filter.CommPartners, 0) comm
                     , focus_filter.CommPartners_id comm_id
                     , COALESCE(focus_filter.CampPartners, 0) camp
                     , COALESCE(focus_filter.numberofunostudents, 0) unostu
                     , COALESCE(focus_filter.unostudentshours, 0) unohr
                     , COALESCE(focus_filter.numberofk12students, 0) k12stu
                     , COALESCE(focus_filter.k12studentshours, 0) k12hr	      
       from home_missionarea focus
           left join focus_filter on focus_filter.focus_id = focus.id
       group by rec_type, focus.id, focus.mission_name, focus_desc, proj, proj_ids, comm, comm_id, camp, unostu, unohr, k12stu, k12hr
       order by focus_name)
       UNION
      (with topic_filter as (select ms.secondary_mission_area_id focus_id
                                  , ms.sub_category_id topic_id
                                  , count(distinct p.project_name) Projects
                                  , array_agg(distinct p.id) projects_id
                                  , count(distinct pcomm.community_partner_id) CommPartners
                                  , array_agg(distinct pcomm.community_partner_id) CommPartners_id
                                  , count(distinct pcamp.campus_partner_id) CampPartners
                                  , sum(p.total_uno_students) numberofunostudents
                                  , sum(p.total_uno_hours) unostudentshours
                                  , sum(p.total_k12_students) numberofk12students
                                  , sum(p.total_k12_hours) k12studentshours			   
                             from projects_missionsubcategory ms
                                 left join projects_projectsubcategory psc on psc.sub_category_id = ms.sub_category_id
                                 left join projects_project p on p.id = psc.project_name_id
                                 left join projects_projectengagementactivity pea on pea."ProjectName_id" = p.id
                                 left join projects_engagementactivitytype ea on ea.id = pea."ProjectEngagementActivityName_id"
                                 left join projects_projectcampuspartner pcamp on pcamp.project_name_id = p.id
                                 left join projects_projectcommunitypartner pcomm on pcomm.project_name_id = p.id
                                 left join partners_communitypartner comm on comm.id = pcomm.community_partner_id
                                 left join projects_status s on s.id = p.status_id	
                                 left join partners_campuspartner c on pcamp.campus_partner_id = c.id  
                             where COALESCE(s.name,'None') != 'Drafts'
                               and COALESCE(ms.secondary_mission_area_id::text,'None') like %s
                               and COALESCE(comm.community_type_id::text,'None') like %s
                               and COALESCE(pcamp.campus_partner_id::text,'None') like %s
                               and COALESCE(c.college_name_id::text,'None') like %s
                               and COALESCE(ea."EngagementTypeName_id"::text,'None') like %s
                               and ((p.academic_year_id <= %s) AND 
                                    (COALESCE(p.end_academic_year_id,p.academic_year_id) >= %s))
                               and COALESCE(comm.cec_partner_status_id,(select id from partners_cecpartnerstatus where name like 'Never')) in  (select id from partners_cecpartnerstatus where name like %s)
                               and COALESCE(c.cec_partner_status_id,(select id from partners_cecpartnerstatus where name like 'Never')) in (select id from partners_cecpartnerstatus where name like %s)                                    
                             group by focus_id, topic_id
                             order by focus_id,topic_id)		      
       Select distinct 'Topic' rec_type
                      , focus_topic.secondary_mission_area_id focus_id
                      , 'None' focus_name
                      , 'None' focus_desc
                      , 'None' focus_image_url
                      , 'black' focus_color
                      , topic.id topic_id
                      , topic.sub_category topic_name
                      , topic.sub_category_descr topic_desc
                      , COALESCE(topic_filter.Projects, 0) proj
                      , topic_filter.projects_id proj_ids
                      , COALESCE(topic_filter.CommPartners, 0) comm
                      , topic_filter.CommPartners_id comm_id
                      , COALESCE(topic_filter.CampPartners, 0) camp
                      , COALESCE(topic_filter.numberofunostudents, 0) unostu
                      , COALESCE(topic_filter.unostudentshours, 0) unohr
                      , COALESCE(topic_filter.numberofk12students, 0) k12stu
                      , COALESCE(topic_filter.k12studentshours, 0) k12hr	      
       from projects_missionsubcategory focus_topic
           join projects_subcategory topic on topic.id = focus_topic.sub_category_id
           left join topic_filter on topic_filter.topic_id = topic.id
       group by focus_topic.secondary_mission_area_id, topic.id, topic.sub_category, topic_desc, proj, proj_ids, comm, comm_id, camp, unostu, unohr, k12stu, k12hr
       order by focus_id,topic_name)) focus_topic_data
order by rec_type, focus_name, topic_name;
'''


def editproj_addprimarymission():
    return ( """insert into projects_projectmission (mission_type,mission_id,project_name_id) values ('Primary','%s','%s'); """)

def editproj_updateprimarymission():
    return ( """update projects_projectmission set mission_id= '%s',project_name_id ='%s' where project_name_id ='%s' and mission_type = 'Primary'; """)