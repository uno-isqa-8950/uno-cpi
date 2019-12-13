from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class CreateprojectPageUi:
    ## URL
    URL = 'https://uno-cpi-dev.herokuapp.com/'

    # Locators for createproject
    Projects_link = (By.XPATH, '//*[@id="target"]/ul/li[3]/a')
    Projects_createprojectlink = (By.XPATH, '//*[@id="target"]/ul/li[3]/div/a[3]')
    Projects_checkprojectname = (By.XPATH, '//*[@id="projectName"]')
    Projects_checkprojectsearchbutton = (By.XPATH, '//*[@id="filters-form"]/div[5]/button')
    Projects_createprojectbutton = (By.XPATH, '//*[@id="lnk-create_project"]')
    Projects_engagementtype = (By.XPATH, '//*[@id="select2-id_engagement_type-container"]')
    Projects_activitytype_other = (By.XPATH, '//*[@id="select2-id_populate_activity-container"]')
    Projects_otheractivitytypetext = (By.XPATH, '//*[@id="otheracttype"]')
    Projects_addotheractivity_button = (By.XPATH, '//*[@id="addotheract"]')
    Projects_description = (By.XPATH, '//*[@id="id_description"]')
    Projects_projectsduration_collapsiblebar = (By.XPATH, '//*[@id="form-step-0"]/button[1]')
    Projects_startsemester = (By.XPATH, '//*[@id="select2-id_semester-container"]')
    Projects_participantcollapsiblebar = (By.XPATH, '//*[@id="form-step-0"]/button[2]')
    Projects_projecttotalunostudents = (By.XPATH, '//*[@id="id_total_uno_students"]')
    Projects_unostudenthours = (By.XPATH, '//*[@id="id_total_uno_hours"]')
    Projects_unofacultyhours = (By.XPATH, '//*[@id="id_total_uno_faculty"]')
    Projects_totalotherparticipants = (By.XPATH, '//*[@id="id_total_other_community_members"]')
    Projects_K12studentsflag = (By.XPATH, '//*[@id="id_k12_flag"]')
    Projects_totalnoofk12students = (By.XPATH, '//*[@id="id_total_k12_students"]')
    Projects_totalk12studenthours = (By.XPATH, '//*[@id="id_total_k12_hours"]')
    Projects_Saveasdraft = (By.XPATH, '//*[@id="draft"]')
    Projects_Cancel = (By.XPATH, '//*[@id="cancel"]')
    Projects_next1 = (By.XPATH, '//*[@id="smartwizard"]/div[2]/div/button[2]')
    Projects_communitypartner1 = (By.XPATH, '//*[@id="id_community-0-community_partner"]/option[2]')
    Projects_communitypartner2 = (By.XPATH, '//*[@id="id_community-0-community_partner"]/option[3]')
    Projects_addcommunitypartner = (By.XPATH, '//*[@id="communityinfo"]/div/div[2]/div[3]/i')
    Projects_campuspartnertab = (By.XPATH, '//*[@id="step-2"]/button[1]/span')
    Projects_campuspartner1 = (By.XPATH, '//*[@id="id_campus-0-campus_partner"]/option[2]')
    Projects_campuspartner2 = (By.XPATH, '//*[@id="id_campus-0-campus_partner"]/option[3]')
    Projects_addcampuspartner = (By.XPATH, '//*[@id="campusinfo"]/div[2]/div[2]/div[3]/div/span/i')
    Projects_campusleadstafftab = (By.XPATH, '//*[@id="step-2"]/button[2]')
    Projects_campusleadfirstname = (By.XPATH, '//*[@id="firstname"]')
    Projects_campusleadlastname = (By.XPATH, '//*[@id="lastname"]')
    Projects_addcampuslead = (By.XPATH, '//*[@id="submitname"]')
    Project_previous1 = (By.XPATH, '//*[@id="smartwizard"]/div[2]/div/button[1]')
    Project_next2 = (By.XPATH, '//*[@id="smartwizard"]/div[2]/div/button[2]')
    Project_focusarea = (By.XPATH, '//*[@id="id_mission-0-mission"]/option[2]')
    Project_topics = (By.XPATH, '//*[@id="id_sub_category-0-sub_category"]/option[2]')
    Project_addsubcategory = (By.XPATH, '//*[@id="step-3"]/div[4]/div[4]/div/i')
    Project_next3 = (By.XPATH, '//*[@id="smartwizard"]/div[2]/div/button[2]')
    Project_addressline1 = (By.XPATH, '//*[@id="id_address_line1"]')
    Project_city = (By.XPATH, '//*[@id="id_city"]')
    Project_country = (By.XPATH, '//*[@id="id_country"]')
    Project_state = (By.XPATH, '//*[@id="id_state"]')
    Project_zip = (By.XPATH, '//*[@id="id_zip"]')
    Project_terms = (By.XPATH, '//*[@id="terms"]')
    Project_submit = (By.XPATH, '//*[@id="submit"]')
    ### Initializer

    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods

    def load(self):
        self.browser.get(self.URL)


    def projects_link(self):
        projects_Link = self.browser.find_element(*self.Projects_link)
        projects_Link.click()

    def projects_createprojectlink(self):
        projects_Createprojectlink = self.browser.find_element(*self.Projects_createprojectlink)
        projects_Createprojectlink.click()

    def projects_checkprojectname(self):
        projects_Checkprojectname = self.browser.find_element(*self.Projects_checkprojectname)
        projects_Checkprojectname.send_keys("Testcreate" + Keys.RETURN)

    def projects_checkprojectsearchbutton(self):
        projects_Checkprojectsearchbutton = self.browser.find_element(*self.Projects_checkprojectsearchbutton)
        projects_Checkprojectsearchbutton.click()

    def projects_createprojectbutton(self):
        projects_Createprojectbutton = self.browser.find_element(*self.Projects_createprojectbutton)
        projects_Createprojectbutton.click()

    def projects_engagementtype(self):
        projects_Engagementtype = self.browser.find_element(*self.Projects_engagementtype)
        projects_Engagementtype.click()

    def projects_activitytype_other(self):
        projects_Activitytype_other = self.browser.find_element(*self.Projects_activitytype_other)
        projects_Activitytype_other.click()

    def projects_otheractivitytypetext(self):
        projects_otheractivitytypetext = self.browser.find_element(*self.Projects_otheractivitytypetext)
        projects_otheractivitytypetext.send_keys("Classroom teaching" + Keys.RETURN)

    def projects_addotheractivity_button(self):
        projects_Addotheractivity_button = self.browser.find_element(*self.Projects_addotheractivity_button)
        projects_Addotheractivity_button.click()

    def projects_description(self):
        projects_description = self.browser.find_element(*self.Projects_description)
        projects_description.send_keys("proj desc" + Keys.RETURN)

    def projects_projectsduration_collapsiblebar(self):
        projects_Projectsduration_collapsiblebar = self.browser.find_element(*self.Projects_projectsduration_collapsiblebar)
        projects_Projectsduration_collapsiblebar.click()

    def projects_projecttotalunostudents(self):
        Projects_projecttotalunostudents = self.browser.find_element(*self.Projects_projecttotalunostudents)
        Projects_projecttotalunostudents.send_keys("10" + Keys.RETURN)

    def projects_unostudenthours(self):
        projects_unostudenthours = self.browser.find_element(*self.Projects_unostudenthours)
        projects_unostudenthours.send_keys("5" + Keys.RETURN)

    def projects_totalotherparticipants(self):
        Projects_totalotherparticipants = self.browser.find_element(*self.Projects_totalotherparticipants)
        Projects_totalotherparticipants.send_keys("20" + Keys.RETURN)

    def projects_K12studentsflag(self):
        Projects_K12studentsflag = self.browser.find_element(*self.Projects_K12studentsflag)
        Projects_K12studentsflag.click()

    def projects_totalnoofk12students(self):
        Projects_totalnoofk12students = self.browser.find_element(*self.Projects_totalnoofk12students)
        Projects_totalnoofk12students.send_keys("5" + Keys.RETURN)

    def projects_totalk12studenthours(self):
        Projects_totalk12studenthours = self.browser.find_element(*self.Projects_totalk12studenthours)
        Projects_totalk12studenthours.send_keys("100" + Keys.RETURN)

    def projects_Saveasdraft(self):
        Projects_Saveasdraft = self.browser.find_element(*self.Projects_Saveasdraft)
        Projects_Saveasdraft.click()

    def projects_Cancel(self):
        Projects_Cancel = self.browser.find_element(*self.Projects_Cancel)
        Projects_Cancel.click()

    def projects_next1(self):
        Projects_next1 = self.browser.find_element(*self.Projects_next1)
        Projects_next1.click()

    def projects_communitypartner1(self):
        Projects_communitypartner1 = self.browser.find_element(*self.Projects_communitypartner1)
        Projects_communitypartner1.click()

    def projects_addcommunitypartner(self):
        Projects_addcommunitypartner = self.browser.find_element(*self.Projects_addcommunitypartner)
        Projects_addcommunitypartner.click()

    def projects_communitypartner2(self):
        Projects_communitypartner2 = self.browser.find_element(*self.Projects_communitypartner2)
        Projects_communitypartner2.click()

    def projects_campuspartnertab(self):
        Projects_campuspartnertab = self.browser.find_element(*self.Projects_campuspartnertab)
        Projects_campuspartnertab.click()

    def projects_campuspartner1(self):
        Projects_campuspartner1 = self.browser.find_element(*self.Projects_campuspartner1)
        Projects_campuspartner1.click()

    def projects_campuspartner2(self):
        Projects_campuspartner2 = self.browser.find_element(*self.Projects_campuspartner2)
        Projects_campuspartner2.click()

    def projects_participantcollapsiblebar(self):
        Projects_participantcollapsiblebar = self.browser.find_element(*self.Projects_participantcollapsiblebar)
        Projects_participantcollapsiblebar.click()

    def projects_startsemester(self):
        Projects_startsemester = self.browser.find_element(*self.Projects_startsemester)
        Projects_startsemester.click()

    def projects_addcampuspartner(self):
        Projects_addcampuspartner = self.browser.find_element(*self.Projects_addcampuspartner)
        Projects_addcampuspartner.click()

    def projects_campusleadstafftab(self):
        Projects_campusleadstafftab = self.browser.find_element(*self.Projects_campusleadstafftab)
        Projects_campusleadstafftab.click()

    def projects_campusleadfirstname(self):
        Projects_campusleadfirstname = self.browser.find_element(*self.Projects_campusleadfirstname)
        Projects_campusleadfirstname.send_keys("Dave" + Keys.RETURN)


    def projects_campusleadlastname(self):
        Projects_campusleadlastname = self.browser.find_element(*self.Projects_campusleadlastname)
        Projects_campusleadlastname.send_keys("Williams" + Keys.RETURN)

    def projects_addcampuslead(self):
        Projects_addcampuslead = self.browser.find_element(*self.Projects_addcampuslead)
        Projects_addcampuslead.click()

    def project_previous1(self):
        Project_previous1 = self.browser.find_element(*self.Project_previous1)
        Project_previous1.click()

    def project_next2(self):
        Project_next2 = self.browser.find_element(*self.Project_next2)
        Project_next2.click()

    def project_topics(self):
        Project_topics = self.browser.find_element(*self.Project_topics)
        Project_topics.click()


    def project_addsubcategory(self):
        Project_addsubcategory = self.browser.find_element(*self.Project_addsubcategory)
        Project_addsubcategory.click()


    def project_next3(self):
        Project_next3 = self.browser.find_element(*self.Project_next3)
        Project_next3.click()

    def project_addressline1(self):
        Project_addressline1 = self.browser.find_element(*self.Project_addressline1)
        Project_addressline1.send_keys("7525 Howard Street" + Keys.RETURN)

    def project_city(self):
        Project_city = self.browser.find_element(*self.Project_city)
        Project_city.send_keys("Omaha" + Keys.RETURN)

    def project_country(self):
        Project_country = self.browser.find_element(*self.Project_country)
        Project_country.send_keys("US" + Keys.RETURN)

    def project_state(self):
        Project_state = self.browser.find_element(*self.Project_state)
        Project_state.send_keys("Nebraska" + Keys.RETURN)

    def project_zip(self):
        Project_zip = self.browser.find_element(*self.Project_zip)
        Project_zip.send_keys("68114" + Keys.RETURN)

    def project_terms(self):
        Project_terms = self.browser.find_element(*self.Project_terms)
        Project_terms.click()

    def project_submit(self):
        Project_submit = self.browser.find_element(*self.Project_submit)
        Project_submit.click()


