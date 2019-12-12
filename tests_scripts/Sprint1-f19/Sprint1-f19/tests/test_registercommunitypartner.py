from .communitypartnerpageelementsui import PartnersPageUi

def test_community_register(browser):
    partners = PartnersPageUi(browser)
    partners.Partners_Homepagelink()
    partners.partners_homepage()
    partners.partners_communitypartnerregister()
    partners.partners_checkcommunitypartnertext()
    partners.partners_checkcommunitysearchbutton()
    partners.partners_createcommunitybutton()
    partners.partners_communityacronym()
    partners.partners_communitypartnertype()
    partners.partners_communitywebsite()
    partners.partners_communityaddresschoice()
    partners.partners_communitynextpage()
    partners.partners_communityfocusarea()
    partners.partners_communityotherfocusarea()
    partners.partners_addcommunityfocus()
    partners.partners_communityterms()
    partners.partners_communitysubmit()

