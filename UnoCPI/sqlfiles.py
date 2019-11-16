tables_sql = "SELECT table_schema || '.' || table_name "\
           "FROM information_schema.tables "\
           "WHERE table_type = 'BASE TABLE' "\
           "AND table_schema NOT IN ('pg_catalog', 'information_schema');"

# Please dont make changes to this query, it directly affects AllProjects Page
all_projects_sql = """select distinct p.project_name
                          ,array_agg(distinct m.mission_type||': '||hm.mission_name) mission_area
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
                        -- 	,pc.name CommPartners
                        -- 	,c.name CampPartners
                        -- 	,e.name engagement_type
                        from projects_project p
                          inner join projects_projectmission m on p.id = m.project_name_id
                          inner join home_missionarea hm on hm.id = m.mission_id
                          inner join projects_engagementtype e on e.id = p.engagement_type_id
                            left join projects_projectcommunitypartner pp on p.id = pp.project_name_id
                          left join partners_communitypartner pc on pp.community_partner_id = pc.id
                            left join projects_projectcampuspartner pp2 on p.id = pp2.project_name_id
                            left join partners_campuspartner c on pp2.campus_partner_id = c.id
                            inner join projects_academicyear pa on p.academic_year_id = pa.id
                            inner join projects_status ps on p.status_id = ps.id
                            inner join projects_activitytype a on p.activity_type_id = a.id
                        group by p.project_name
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
                        order by p.project_name limit 10;"""

                    

selected_projects_sql = """select distinct p.project_name
                          ,array_agg(distinct m.mission_type||': '||hm.mission_name) mission_area
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
                        -- 	,pc.name CommPartners
                        -- 	,c.name CampPartners
                        -- 	,e.name engagement_type
                        from projects_project p
                          inner join projects_projectmission m on p.id = m.project_name_id
                          inner join home_missionarea hm on hm.id = m.mission_id
                          inner join projects_engagementtype e on e.id = p.engagement_type_id
                            left join projects_projectcommunitypartner pp on p.id = pp.project_name_id
                          left join partners_communitypartner pc on pp.community_partner_id = pc.id
                            left join projects_projectcampuspartner pp2 on p.id = pp2.project_name_id
                            left join partners_campuspartner c on pp2.campus_partner_id = c.id
                            inner join projects_academicyear pa on p.academic_year_id = pa.id
                            inner join projects_status ps on p.status_id = ps.id
                            inner join projects_activitytype a on p.activity_type_id = a.id
                        where p.project_name = %(p_name)s
                        group by p.project_name
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
                        order by p.project_name;"""

drop_temp_table_all_projects_start_and_end_dates_sql = "DROP TABLE all_projects_start_and_end_dates;"

start_and_end_dates_temp_table_sql = """CREATE TEMP TABLE all_projects_start_and_end_dates AS (
	select p3.id
		,start_date
		,end_date
		,case 
			when current_date < start_date then 'Pending'
            when current_date > end_date then 'Inactive'
            when current_date >= start_date and current_date <= end_date then 'Active'
		end proj_status
	from 
			(select p2.id
				,cast ((cast(start_year as varchar(4))||'-'||cast(start_month as varchar(4))||'-'||'1') as date) start_date
				,cast ((cast(end_year as varchar(4))||'-'||cast(end_month as varchar(4))||'-'||'31') as date) end_date
			from
				(select p1.*
					,case
						when end_month = 5 then cast((substring(end_academic_year,1,4)) as integer)+1
						when end_month = 7 then cast((substring(end_academic_year,1,4)) as integer)+1
						when end_month = 12 then cast((substring(end_academic_year,1,4)) as integer)
					end end_year
                    ,case
                        when start_month = 1 then cast((substring(start_academic_year,1,4)) as integer)+1
                        when start_month = 6 then cast((substring(start_academic_year,1,4)) as integer)+1
                        when start_month = 8 then cast((substring(start_academic_year,1,4)) as integer)
                    end start_year
				from
					(select p0.id
						,p0.start_academic_year
                        ,p0.end_academic_year
						,case 
							when p0.start_semester like 'Fall%' then 8
							when p0.start_semester like 'Spring%' then 1
							when p0.start_semester like 'Summer%' then 6
						end start_month
						,case 
							when p0.end_semester like 'Fall%' then 12
							when p0.end_semester like 'Spring%' then 5
							when p0.end_semester like 'Summer%' then 7
						end end_month
					FROM
                        (
                        select p.id
                            ,p.semester start_semester
                            ,ay.academic_year start_academic_year
                            ,case
                                when end_semester = '' then semester
                                else end_semester
                             end end_semester
                            ,coalesce(ay2.academic_year, ay.academic_year) end_academic_year
                        from public.projects_project p
						inner join projects_academicyear ay on p.academic_year_id = ay.id
                        left join projects_academicyear ay2 on p.end_academic_year_id = ay2.id
                        )p0
					)p1
				)p2
			)p3
);"""



comm_partners_to_be_set_to_active ="""select community_partner_id
from
	(-- ALL COMMUNITY PARTNERS ATTACHED TO A PROJECT
	select distinct community_partner_id
		,max(case when proj_status = 'Active' then proj_status end) active_prj
		,max(case when proj_status = 'Inactive' then proj_status end) inactive_prj
	from    
		--ALL COMMUNITY PARTNERS ATTACHED TO A PROJECT ACTIVE AND/OR INACTIVE
		(select distinct cp.community_partner_id
			,p.project_name
			,cp1.name as comm_partner_name
			,p4.id as project_id
			,p4.start_date
			,p4.end_date
			,cp1.active
			,p4.proj_status
		from all_projects_start_and_end_dates p4
			INNER JOIN public.projects_project p on p.id = p4.id
			INNER JOIN public.projects_projectcommunitypartner cp on p4.id = cp.project_name_id
			INNER JOIN public.partners_communitypartner cp1 on cp1.id = cp.community_partner_id
		)p
	group by p.community_partner_id
)p
where coalesce(active_prj,'') = 'Active'
order by p.community_partner_id;"""

comm_partners_to_be_set_to_inactive ="""select community_partner_id
from
	(-- ALL COMMUNITY PARTNERS ATTACHED TO A PROJECT
	select distinct community_partner_id
		,max(case when proj_status = 'Active' then proj_status end) active_prj
		,max(case when proj_status = 'Inactive' then proj_status end) inactive_prj
		,max(case when proj_status = 'Pending' then proj_status end) pend_prj
	from    
		--ALL COMMUNITY PARTNERS ATTACHED TO A PROJECT ACTIVE AND/OR INACTIVE
		(select distinct cp.community_partner_id
			,p.project_name
			,cp1.name as comm_partner_name
			,p4.id as project_id
			,p4.start_date
			,p4.end_date
			,cp1.active
			,p4.proj_status
		from all_projects_start_and_end_dates p4
			INNER JOIN public.projects_project p on p.id = p4.id
			INNER JOIN public.projects_projectcommunitypartner cp on p4.id = cp.project_name_id
			INNER JOIN public.partners_communitypartner cp1 on cp1.id = cp.community_partner_id
		)p
	group by p.community_partner_id
)p
where coalesce(active_prj,'') = ''
order by p.community_partner_id;"""

update_comm_partner_to_inactive_sql = """
--UPDATE COMMUNITY PARTNER WHEN TIED TO A INACTIVE PROJECTS ONLY TO FALSE (INACTIVE)
UPDATE public.partners_communitypartner SET active = FALSE WHERE id in
(select community_partner_id
from
	(-- ALL COMMUNITY PARTNERS ATTACHED TO A PROJECT
	select distinct community_partner_id
		,max(case when proj_status = 'Active' then proj_status end) active_prj
		,max(case when proj_status = 'Inactive' then proj_status end) inactive_prj
		,max(case when proj_status = 'Pending' then proj_status end) pend_prj
	from    
		--ALL COMMUNITY PARTNERS ATTACHED TO A PROJECT ACTIVE AND/OR INACTIVE
		(select distinct cp.community_partner_id
			,p.project_name
			,cp1.name as comm_partner_name
			,p4.id as project_id
			,p4.start_date
			,p4.end_date
			,cp1.active
			,p4.proj_status
		from all_projects_start_and_end_dates p4
			INNER JOIN public.projects_project p on p.id = p4.id
			INNER JOIN public.projects_projectcommunitypartner cp on p4.id = cp.project_name_id
			INNER JOIN public.partners_communitypartner cp1 on cp1.id = cp.community_partner_id
		)p
	group by p.community_partner_id
)p
where coalesce(active_prj,'') = ''
order by p.community_partner_id
)
;"""

update_comm_partner_to_active_sql = """
--UPDATE COMMUNITY PARTNER WHEN TIED TO A BOTH ACTIVE and/or INACTIVE or JUST ACTIVE PROJECTS ONLY TO TRUE (ACTIVE)
UPDATE public.partners_communitypartner SET active = TRUE WHERE id in
(select community_partner_id
from
	(-- ALL COMMUNITY PARTNERS ATTACHED TO A PROJECT
	select distinct community_partner_id
		,max(case when proj_status = 'Active' then proj_status end) active_prj
		,max(case when proj_status = 'Inactive' then proj_status end) inactive_prj
		,max(case when proj_status = 'Pending' then proj_status end) pend_prj
	from    
		--ALL COMMUNITY PARTNERS ATTACHED TO A PROJECT ACTIVE AND/OR INACTIVE
		(select distinct cp.community_partner_id
			,p.project_name
			,cp1.name as comm_partner_name
			,p4.id as project_id
			,p4.start_date
			,p4.end_date
			,cp1.active
			,p4.proj_status
		from all_projects_start_and_end_dates p4
			INNER JOIN public.projects_project p on p.id = p4.id
			INNER JOIN public.projects_projectcommunitypartner cp on p4.id = cp.project_name_id
			INNER JOIN public.partners_communitypartner cp1 on cp1.id = cp.community_partner_id
		)p
	group by p.community_partner_id
)p
where coalesce(active_prj,'') = 'Active'
order by p.community_partner_id)
;"""

update_project_to_inactive_sql = """
--UPDATE PROJECT STATUS TO COMPLETED
UPDATE public.projects_project SET status_id = 2 WHERE id in
(select p.id 
from all_projects_start_and_end_dates p
where proj_status = 'Inactive'
)
; """

update_project_to_active_sql = """
--UPDATE PROJECT STATUS TO ACTIVE
UPDATE public.projects_project SET status_id = 1 WHERE id in
(select p.id 
from all_projects_start_and_end_dates p
where proj_status = 'Active'
)
; """

update_project_to_pending_sql = """
--UPDATE PROJECT STATUS TO ACTIVE
UPDATE public.projects_project SET status_id = 4 WHERE id in
(select p.id 
from all_projects_start_and_end_dates p
where proj_status = 'Pending'
)
; """

mission_areas_report_sql = """
-- MISSION AREA REPORT
select hm.mission_name mission_area
  ,cpm.CommPartners
  ,count(distinct p.project_name) Projects
  ,sum(p.total_uno_students) numberofunostudents
  ,sum(p.total_uno_hours) unostudentshours
from projects_project p
  inner join projects_projectmission m on p.id = m.project_name_id
  	and m.mission_type = 'Primary'
  inner join home_missionarea hm on hm.id = m.mission_id
  inner join  (select hm.mission_name mission_area
								,mission_area_id
								,count(distinct cp.name) CommPartners
							from partners_communitypartner cp
								inner join partners_communitypartnermission cpm on cpm.community_partner_id = cp.id
							  	and cpm.mission_type = 'Primary'
								inner join home_missionarea hm on hm.id = cpm.mission_area_id
							group by mission_area, mission_area_id
    					) cpm on cpm.mission_area_id = m.mission_id
group by hm.mission_name,CommPartners
order by mission_area;"""

engagement_types_report_sql = """
-- ENGAGEMENT TYPE REPORT
select distinct e.name engagement_type
   ,p.engagement_type_id
  ,count(distinct p.project_name) Projects
	,count(distinct pp.community_partner_id) CommPartners
	,count(distinct pp2.campus_partner_id) CampPartners
	,e.numberofunostudents
	,e.unostudentshours
from projects_project p
 	left join projects_projectcommunitypartner pp on p.id = pp.project_name_id
	left join projects_projectcampuspartner pp2 on p.id = pp2.project_name_id
	inner join
  	(select p.engagement_type_id
     	,e.name --engagement_type
			,sum(p.total_uno_students) numberofunostudents
			,sum(p.total_uno_hours) unostudentshours
		from projects_project p
			inner join projects_engagementtype e on e.id = p.engagement_type_id
		group by p.engagement_type_id,e.name
		order by e.name) e on e.engagement_type_id = p.engagement_type_id
group by e.name, e.numberofunostudents, e.unostudentshours,p.engagement_type_id
order by engagement_type;"""

comm_part_report_sql = """
-- COMMUNITY PARTNER REPORT
select pc.name commpartners
	,count(pcp.project_name_id) projects
from projects_projectcommunitypartner pcp
	inner join partners_communitypartner pc on pcp.community_partner_id = pc.id
group by pc.name
order by commpartners;"""

all_projects_report_sql = """
-- ALL PROJECTS
select distinct p.project_name
  ,array_agg(distinct pc.name) CommPartners
  ,array_agg(distinct c.name) CampPartners
  ,array_agg(distinct e.name) engagement_type
from projects_project p
  left join projects_engagementtype e on e.id = p.engagement_type_id
  left join projects_projectcommunitypartner pp on p.id = pp.project_name_id
  inner join partners_communitypartner pc on pp.community_partner_id = pc.id
  left join projects_projectcampuspartner pp2 on p.id = pp2.project_name_id
  inner join partners_campuspartner c on pp2.campus_partner_id = c.id
group by p.project_name
order by p.project_name;"""


# This Query is used by Projects Report (Dont delete)
projects_report = """
select distinct p.project_name
    ,array_agg(distinct pc.name) CommPartners
    ,array_agg(distinct c.name) CampPartners
    ,e.name engagement_type
from projects_project p
    left join projects_engagementtype e on e.id = p.engagement_type_id
    left join projects_projectcommunitypartner pp on p.id = pp.project_name_id
    left join partners_communitypartner pc on pp.community_partner_id = pc.id
    left join projects_projectcampuspartner pp2 on p.id = pp2.project_name_id
    inner join partners_campuspartner c on pp2.campus_partner_id = c.id
where p.id = ANY(%s)
group by p.project_name, e.name
order by p.project_name;
"""


#This query is for myprojects for campus partners and community partners

my_projects="""
select distinct p.project_name
  ,array_agg(distinct m.mission_type||': '||hm.mission_name) mission_area
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
from projects_project p
  inner join projects_projectmission m on p.id = m.project_name_id  
  inner join home_missionarea hm on hm.id = m.mission_id
  inner join projects_engagementtype e on e.id = p.engagement_type_id
    left join projects_projectcommunitypartner pp on p.id = pp.project_name_id
    left join partners_communitypartner pc on pp.community_partner_id = pc.id
    left join projects_projectcampuspartner pp2 on p.id = pp2.project_name_id
    left join partners_campuspartner c on pp2.campus_partner_id = c.id
    inner join projects_academicyear pa on p.academic_year_id = pa.id
    inner join projects_status ps on p.status_id = ps.id
    inner join projects_activitytype a on p.activity_type_id = a.id
where p.id =  ANY(%s)
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
order by p.project_name;
"""

#This query is for returning draft projects for campus partners or community partners


my_drafts="""
select distinct p.project_name
  ,array_agg(distinct m.mission_type||': '||hm.mission_name) mission_area
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
from projects_project p
  left join projects_projectmission m on p.id = m.project_name_id
  left join home_missionarea hm on hm.id = m.mission_id
  left join projects_engagementtype e on e.id = p.engagement_type_id
    left join projects_projectcommunitypartner pp on p.id = pp.project_name_id
    left join partners_communitypartner pc on pp.community_partner_id = pc.id
    left join projects_projectcampuspartner pp2 on p.id = pp2.project_name_id
    left join partners_campuspartner c on pp2.campus_partner_id = c.id
    inner join projects_academicyear pa on p.academic_year_id = pa.id
    inner join projects_status ps on p.status_id = ps.id
    inner join projects_activitytype a on p.activity_type_id = a.id
    where p.status_id = '5' and p.id =  ANY(%s)
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
order by p.project_name;        
"""


#This query is for issues addressed analysis chart
missions_sql = """SELECT MA.id, COALESCE(count,0) 
                   FROM home_missionarea MA 
                   LEFT JOIN 
                   (SELECT mission_id, count(*) as count 
                   FROM projects_projectmission PM 
                   INNER JOIN projects_project P 
                      ON PM.project_name_id = P.id 
                   WHERE P.academic_year_id <= %(yr_id)s 
                      AND P.end_academic_year_id is null OR P.end_academic_year_id >= %(yr_id)s 
                   GROUP BY PM.mission_id) as TB 
                   ON MA.id = TB.mission_id;\
                   """

#This query is for mission areas on y Axis for issues addressed analysis chart
missionareas_sql = """SELECT MA.id  FROM home_missionarea MA"""

academic_sql="""SELECT min(AC.id)as min,max(AC.id)as max  FROM projects_academicyear AC"""

def showSelectedProjects(project_name_list):
	return ( """select distinct p.project_name
                          ,array_agg(distinct m.mission_type||': '||hm.mission_name) mission_area
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
                        -- 	,pc.name CommPartners
                        -- 	,c.name CampPartners
                        -- 	,e.name engagement_type
                        from projects_project p
                          inner join projects_projectmission m on p.id = m.project_name_id
                          inner join home_missionarea hm on hm.id = m.mission_id
                          inner join projects_engagementtype e on e.id = p.engagement_type_id
                            left join projects_projectcommunitypartner pp on p.id = pp.project_name_id
                          left join partners_communitypartner pc on pp.community_partner_id = pc.id
                            left join projects_projectcampuspartner pp2 on p.id = pp2.project_name_id
                            left join partners_campuspartner c on pp2.campus_partner_id = c.id
                            inner join projects_academicyear pa on p.academic_year_id = pa.id
                            inner join projects_status ps on p.status_id = ps.id
                            inner join projects_activitytype a on p.activity_type_id = a.id 
                            where p.id in """+str(project_name_list)+"""
                        group by p.project_name
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
                        order by p.project_name;"""    )

def checkProjectsql(projectName, comPartner, campPartner, acadYear):
    return ("""SELECT (regexp_split_to_array(p.project_name, E'\:+'))[1] as project_names, STRING_AGG(distinct pc.name, ', ' ORDER BY pc.name) As pcnames,
pa.academic_year, STRING_AGG(distinct c.name, ', ' ORDER BY c.name) As cnames
FROM projects_project p
left join projects_projectcommunitypartner pp on p.id = pp.project_name_id
                            left join partners_communitypartner pc on pp.community_partner_id = pc.id
                            left join projects_projectcampuspartner pp2 on p.id = pp2.project_name_id
                            left join partners_campuspartner c on pp2.campus_partner_id = c.id
                            inner join projects_academicyear pa on p.academic_year_id = pa.id
                            where lower(p.project_name) LIKE '%""" + projectName.lower() + """%'
                            AND pc.name LIKE '%""" + comPartner + """%'
                            AND c.name LIKE '%""" + campPartner + """%'
                            AND pa.academic_year LIKE '%""" + acadYear + """%'
GROUP BY project_names, pa.academic_year
ORDER BY pa.academic_year DESC;
""")



projects_report_filter = """
select distinct p.project_name
    ,array_agg(distinct pc.name) CommPartners
    ,array_agg(distinct c.name) CampPartners
    ,e.name engagement_type
from projects_project p
    left join projects_engagementtype e on e.id = p.engagement_type_id
    left join projects_projectmission pm on pm.project_name_id = p.id
    left join projects_projectcommunitypartner pp on p.id = pp.project_name_id
    left join partners_communitypartner pc on pp.community_partner_id = pc.id
    left join projects_projectcampuspartner pp2 on p.id = pp2.project_name_id  
    inner join partners_campuspartner c on pp2.campus_partner_id = c.id  
where e.id::text like %s
  and pm.mission_id::text like %s
  and pc.community_type_id::text like %s
  and pp2.campus_partner_id::text like %s
  and c.college_name_id::text like %s
  and COALESCE(p.legislative_district::TEXT,'0') LIKE %s
  and COALESCE (p.k12_flag::text, 'no') LIKE %s
  and ((p.academic_year_id <= %s) AND 
       (COALESCE(p.end_academic_year_id,(SELECT max(id) from projects_academicyear)) >= %s))

  
group by p.project_name,e.name
order by p.project_name;
"""


projects_public_report_filter = """
select distinct p.project_name
    ,array_agg(distinct pc.name) CommPartners
    ,array_agg(distinct c.name) CampPartners
    ,e.name engagement_type
    , p.total_uno_students total_uno_students
    , p.total_uno_hours total_uno_hours
    , p.total_economic_impact total_economic_impact
from projects_project p
    left join projects_engagementtype e on e.id = p.engagement_type_id
    left join projects_status s on s.id = p.status_id
    left join projects_projectmission pm on pm.project_name_id = p.id
    left join projects_projectcommunitypartner pp on p.id = pp.project_name_id
    left join partners_communitypartner pc on pp.community_partner_id = pc.id
    left join projects_projectcampuspartner pp2 on p.id = pp2.project_name_id  
    inner join partners_campuspartner c on pp2.campus_partner_id = c.id  
where s.name != 'Draft'
  and  e.id::text like %s
  and pm.mission_id::text like %s
  and pc.community_type_id::text like %s
  and pp2.campus_partner_id::text like %s
  and c.college_name_id::text like %s
  and COALESCE(p.legislative_district::TEXT,'0') LIKE %s
  and ((p.academic_year_id <= %s) AND 
       (COALESCE(p.end_academic_year_id,(SELECT max(id) from projects_academicyear)) >= %s))
  and COALESCE (p.k12_flag::text, 'no') LIKE %s     
        
  
group by p.project_name,e.name, p.total_uno_students, p.total_uno_hours, p.total_economic_impact
order by p.project_name;
"""


community_private_report = """
select pc.name commpartners
  ,array_agg(distinct hm.mission_name) mission
  ,COALESCE (count(distinct p.project_name),0) Projects
  ,COALESCE (sum(p.total_uno_students),0) numberofunostudents
  ,COALESCE (sum(p.total_uno_hours),0) unostudentshours
  , pc.website_url website
from partners_communitypartner pc 
left join projects_projectcommunitypartner pcp on pc.id = pcp.community_partner_id
left join projects_project p on p.id = pcp.project_name_id
left join projects_projectcampuspartner pcam on pcam.project_name_id = p.id
left join partners_communitypartnermission CommMission on CommMission.community_partner_id = pc.id and  CommMission.mission_type='Primary'
left join home_missionarea hm on hm.id = CommMission.mission_area_id
left join partners_campuspartner c on pcam.campus_partner_id = c.id 
where pc.community_type_id::text like %s
 and((p.academic_year_id <= %s) AND 
       (COALESCE(p.end_academic_year_id,(SELECT max(id) from projects_academicyear)) >= %s))
 and  pcam.campus_partner_id::text like %s  
 and COALESCE(p.legislative_district::TEXT,'0') LIKE %s    
 and c.college_name_id::text like %s      

group by commpartners, website
order by commpartners;"""

selected_community_private_report = """
select pc.name commpartners
  ,array_agg(distinct hm.mission_name) mission
  ,COALESCE (count(distinct p.project_name),0) Projects
  ,COALESCE (sum(p.total_uno_students),0) numberofunostudents
  ,COALESCE (sum(p.total_uno_hours),0) unostudentshours
  , pc.website_url website
from partners_communitypartner pc 
left join projects_projectcommunitypartner pcp on pc.id = pcp.community_partner_id
left join projects_project p on p.id = pcp.project_name_id
left join projects_projectcampuspartner pcam on pcam.project_name_id = p.id
left join partners_communitypartnermission CommMission on CommMission.community_partner_id = pc.id and  CommMission.mission_type='Primary'
left join home_missionarea hm on hm.id = CommMission.mission_area_id
left join partners_campuspartner c on pcam.campus_partner_id = c.id 
where pc.community_type_id::text like %s
 and((p.academic_year_id <= %s) AND 
       (COALESCE(p.end_academic_year_id,(SELECT max(id) from projects_academicyear)) >= %s))
 and  pcam.campus_partner_id::text like %s  
 and COALESCE(p.legislative_district::TEXT,'0') LIKE %s    
 and c.college_name_id::text like %s  
 and pc.id in %s  

group by commpartners, website
order by commpartners;
"""

selected_One_community_private_report = """
select pc.name commpartners
  ,array_agg(distinct hm.mission_name) mission
  ,COALESCE (count(distinct p.project_name),0) Projects
  ,COALESCE (sum(p.total_uno_students),0) numberofunostudents
  ,COALESCE (sum(p.total_uno_hours),0) unostudentshours
  , pc.website_url website
from partners_communitypartner pc 
left join projects_projectcommunitypartner pcp on pc.id = pcp.community_partner_id
left join projects_project p on p.id = pcp.project_name_id
left join projects_projectcampuspartner pcam on pcam.project_name_id = p.id
left join partners_communitypartnermission CommMission on CommMission.community_partner_id = pc.id and  CommMission.mission_type='Primary'
left join home_missionarea hm on hm.id = CommMission.mission_area_id
left join partners_campuspartner c on pcam.campus_partner_id = c.id 
where pc.community_type_id::text like %s
 and((p.academic_year_id <= %s) AND 
       (COALESCE(p.end_academic_year_id,(SELECT max(id) from projects_academicyear)) >= %s))
 and  pcam.campus_partner_id::text like %s  
 and COALESCE(p.legislative_district::TEXT,'0') LIKE %s    
 and c.college_name_id::text like %s  
 and pc.id = %s  

group by commpartners, website
order by commpartners;
"""

community_public_report = """
select pc.name commpartners
  ,array_agg(distinct hm.mission_name) mission
  ,COALESCE (count(distinct p.project_name),0) Projects
  , pc.website_url website
from partners_communitypartner pc 
left join projects_projectcommunitypartner pcp on pc.id = pcp.community_partner_id
left join projects_project p on p.id = pcp.project_name_id
left join projects_projectcampuspartner pcam on pcam.project_name_id = p.id
left join partners_communitypartnermission CommMission on CommMission.community_partner_id = pc.id and  CommMission.mission_type='Primary'
left join home_missionarea hm on hm.id = CommMission.mission_area_id
left join partners_campuspartner c on pcam.campus_partner_id = c.id 
where pc.community_type_id::text like %s
 and((p.academic_year_id <= %s) AND 
       (COALESCE(p.end_academic_year_id,(SELECT max(id) from projects_academicyear)) >= %s))
 and  pcam.campus_partner_id::text like %s  
 and COALESCE(p.legislative_district::TEXT,'0') LIKE %s    
 and c.college_name_id::text like %s      

group by commpartners, website
order by commpartners;
"""
