from .test_login import test_basic_login
from .projectspageui import *

def test_createproject(browser):
    test_basic_login()
    CreateprojectPageUi.projects_link()
    CreateprojectPageUi.projects_createprojectlink()
    CreateprojectPageUi.projects_checkprojectname()
    CreateprojectPageUi.projects_checkprojectsearchbutton()
    CreateprojectPageUi.projects_engagementtype()
    CreateprojectPageUi.projects_description()
    CreateprojectPageUi.projects_startsemester()
    CreateprojectPageUi.projects_next1()
    CreateprojectPageUi.projects_campuspartnertab()
    CreateprojectPageUi.projects_campuspartner1()
    CreateprojectPageUi.projects_addcampuspartner()
    CreateprojectPageUi.Project_next2()
    CreateprojectPageUi.Project_focusarea()
    CreateprojectPageUi.Project_topics()
    CreateprojectPageUi.Project_addsubcategory()
    CreateprojectPageUi.Project_next3()
    CreateprojectPageUi.Project_terms()
    CreateprojectPageUi.Project_submit()