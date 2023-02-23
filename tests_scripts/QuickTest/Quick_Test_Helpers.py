from tests_scripts import QuickTest
from tests_scripts import *

# creating object of the class
login = QuickTest.QuickTest()

# Pass the appropriate user name and password from __init__.py file
# login.test_Quick_Login(admin_user,admin_pwd)
# login.test_Quick_Logout(campus_partner_user,campus_partner_pwd)
# login.test_Quick_Logout(admin_user,admin_pwd)
# login.test_Quick_Community_Partner_Registration("Viz26")
# login.test_Quick_Campus_Partner_Registration("Vix203")
login.test_Quick_Campus_Partner_User_Sign_Up(campus_partner_user, campus_partner_pwd)





