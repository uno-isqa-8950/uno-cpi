from .campuspartnerpageui import CampusPartnersPageUi

def test_campus_register(browser):
    partners = CampusPartnersPageUi(browser)
    partners.partners_homepage()
    partners.partners_campuspartnerregister()
    partners.partners_Campuspartnername()
    partners.partners_College()
    partners.partners_next()
    partners.partners_campusfirstname()
    partners.partners_campuslastname()
    partners.partners_campusemail()
    partners.partners_addcampuscontact()
    partners.partners_campusterms()
    partners.partners_campussubmit()