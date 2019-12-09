from .test_login import test_basic_login
from .projectspageui import *

def test_saveasdraft(browser):
    test_basic_login()
    CreateprojectPageUi.projects_link()
    CreateprojectPageUi.projects_createprojectlink()
    CreateprojectPageUi.projects_checkprojectname()
    CreateprojectPageUi.projects_checkprojectsearchbutton()
    CreateprojectPageUi.projects_engagementtype()
    CreateprojectPageUi.projects_description()
    CreateprojectPageUi.projects_startsemester()
    CreateprojectPageUi.projects_Saveasdraft()

