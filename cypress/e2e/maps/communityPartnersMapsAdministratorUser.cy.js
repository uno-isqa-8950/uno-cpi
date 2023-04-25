import user from "../../support/commands.js";
describe('community partners map admin user test', () => {
beforeEach(() => {
    cy.on('uncaught:exception', (err) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'options\'') || err.message.includes('reading \'scrollTop\'') || err.message.includes('reading \'addEventListener\'')|| err.message.includes('null (reading \'style\')'))
      {
        return false
      }
    })
    cy.fixture("datareports").then(function(data) {
      this.data = data
    })
    cy.loginAdminUser(user)  // Admin User is logged in before the test begins
    cy.visit(Cypress.env('baseUrl'))
  })
    // This test is expected to pass visiting community partners under maps as a admin user.
    // Test is asserted on url, visibility of filters button, map canvas existence in the page loaded and existence of footer.
    it('Community partners page visit with admin user login ', function() {
      const communityPartnersLink = '[data-cy="communitypartners"]',
        filtersButton = '[data-cy="filters"]',
        footer = '[data-cy="footer"]',
        mapsDiv = '[data-cy="mapcanvas"]',
        mapsLink = '[data-cy="maps"]',
        noOfCommPart ='[data-cy="totalnumber"]'
      cy.get(mapsLink).contains('Maps').click()
        .get(communityPartnersLink).click()
        .url().should('be.equal', Cypress.env('baseUrl')+'community-Partner')            
      // Asserting to check the page title
        .get('div').contains('label', 'Community Partners Map')
      // Checking the number of community partners value is visible
        .get('div').contains('label', 'Number of Community Partners:')
      // Total numbers value  existence assertion
        .get(noOfCommPart).should('be.visible')
        .get(filtersButton).should('be.visible')
        .get(mapsDiv).should('exist')
        .get(footer).should('exist')
    })
  
    it('Testing map canvas button clickability ', function() {
      const communityPartnersLink = '[data-cy="communitypartners"]',
        filtersButton = '[data-cy="filters"]',
        footer = '[data-cy="footer"]',
        mapsDiv = '[data-cy="mapcanvas"]',
        mapsLink = '[data-cy="maps"]'
      cy.get(mapsLink).contains('Maps').click()
        .get(communityPartnersLink).click()
        .url().should('be.equal', Cypress.env('baseUrl')+'community-Partner')
        .get(filtersButton).should('be.visible')
        .get(mapsDiv).should('exist')
        .get(footer).should('exist')
      cy.get(mapsDiv).then($canvas => {
        // South Carolina
        // Wrap the canvas with the Cypress API, scroll it into view, and click in the location!
        cy.wrap($canvas)
          .scrollIntoView()
        // click on a marker to check marker is not disabled
        cy.get('[style="z-index: 3; position: absolute; height: 100%; width: 100%; padding: 0px; border-width: 0px; margin: 0px; left: 0px; top: 0px; touch-action: pan-x pan-y;"]').click().wait(3000)
          .should('not.be.disabled')
      });
    })
   
    it('Test filter dropdown are clickable', function(){
      
      const communityPartnersLink = '[data-cy="communitypartners"]',
        filtersButton = '[data-cy="filters"]',
        footer = '[data-cy="footer"]',
        districtsDropdown = '[data-cy="selectdistrict"]',
        mapsDiv = '[data-cy="mapcanvas"]',
        mapsLink = '[data-cy="maps"]',
        communityPartnerTypeDropdown = '[data-cy="selectcommunitytype"]',
        selectCollegeDropdown = '[data-cy="selectcollege"]',
        selectCampusPartnerDropdown = '[data-cy="selectcampus"]',
        selectYearDropdown = '[data-cy="selectyear"]'
      cy.get(mapsLink).contains('Maps').click()
        .get(communityPartnersLink).click()
        .url().should('be.equal', Cypress.env('baseUrl')+'community-Partner')
      // filter button clicking and asserting to check the button is not disabled
        .get(filtersButton).click().should('not.be.disabled')
      // select dropdown triggering click action to check it is clickable and asserting to check its not disabled
        .get(districtsDropdown).trigger('click').should('not.be.disabled')
      // Selecting some value from dropdown. Here selecting legislative district 1 option from districts dropdown list
        .get(districtsDropdown).select(this.data.legislative_dist1).should('exist')
  
        .get(communityPartnerTypeDropdown).trigger('click').should('not.be.disabled')
      // Selecting some value from dropdown. Here selecting business option from community partners dropdown list
        .get(communityPartnerTypeDropdown).select(this.data.community_type1).should('exist')
  
        .get(selectCollegeDropdown).trigger('click').should('not.be.disabled')
      // Selecting some value from dropdown. Here selecting "Academic Affairs" option from select college dropdown list
        .get(selectCollegeDropdown).select(this.data.college_name1).should('exist')
  
        .get(selectCampusPartnerDropdown).trigger('click').should('not.be.disabled')
  
        .get(selectYearDropdown).trigger('click').should('not.be.disabled')
      // Selecting some value from dropdown. Here selecting "Academic year" option from select year dropdown list
        .get(selectYearDropdown).select(this.data.academic_year1).should('exist')
  
        .get(mapsDiv).should('exist')
        .get(footer).should('exist')
    })
  
    it('Mission area filters links are clickable', function(){
      const communityPartnersLink = '[data-cy="communitypartners"]',
        filtersButton = '[data-cy="filters"]',
        footer = '[data-cy="footer"]',
        mapsDiv = '[data-cy="mapcanvas"]',
        mapsLink = '[data-cy="maps"]',
        missionAreaFilters = '[data-cy="missionareafilters"]',
        allFocusAreasFilterLink = `a[id="All Focus Areas"]`,
        artsCultureHumanitiesLink = `a[id="Arts, Culture and Humanities"]`,
        economicSufficiencyLink = `a[id="Economic Impact"]`,
        educationalSupportLink = `a[id="Educational Support"]`,
        environmentalStewardshipLink = `a[id="Environmental Stewardship"]`,
        healthAndWellnessLink = `a[id="Health and Wellness"]`,
        internationalServiceLink = `a[id="International Service"]`,
        socialJusticeLink = `a[id="Social Justice"]`  
      cy.get(mapsLink).contains('Maps').click()
        .get(communityPartnersLink).click()
        .url().should('be.equal', Cypress.env('baseUrl')+'community-Partner')
      // filter button clicking and asserting to check the button is not disabled
        .get(filtersButton).click().should('not.be.disabled')
      // Testing filters links function
        .get(missionAreaFilters).should('exist')
        .get(allFocusAreasFilterLink).click({force: true})
        .get(artsCultureHumanitiesLink).click({force: true})
        .get(economicSufficiencyLink).click({force: true})
        .get(educationalSupportLink).click({force: true})
        .get(environmentalStewardshipLink).click({force: true})
        .get(healthAndWellnessLink).click({force: true})
        .get(internationalServiceLink).click({force: true})
        .get(socialJusticeLink).click({force: true})
        .get(mapsDiv).should('exist')
        .get(footer).should('exist')
    })
  
    it('Mission area filters dropdowns are clickable', function(){
      const communityPartnersLink = '[data-cy="communitypartners"]',
        filtersButton = '[data-cy="filters"]',
        footer = '[data-cy="footer"]',
        mapsDiv = '[data-cy="mapcanvas"]',
        mapsLink = '[data-cy="maps"]',
        missionAreaFilters = '[data-cy="missionareafilters"]',
        allCommunityPartnerTypes= '[data-cy="selectcommunitytype"]',
        selectCollege = '[data-cy="selectcollege"]',
        selectCampus = '[data-cy="selectcampus"]',
        selectYear = '[data-cy="selectyear"]',
        selectDistrict = '[data-cy="selectdistrict"]'
      cy.get(mapsLink).contains('Maps').click()
        .get(communityPartnersLink).click()
        .url().should('be.equal', Cypress.env('baseUrl')+'community-Partner')
      // filter button clicking and asserting to check the button is not disabled
        .get(filtersButton).click().should('not.be.disabled')
      // Testing filters links function
      .get(missionAreaFilters).should('exist')
      .get(allCommunityPartnerTypes).select(this.data.community_type1,{force: true})
      .get(selectCollege).should('exist')
      .get(selectCampus).select(this.data.campus_partner1,{force: true})
      .get(selectYear).select(this.data.academic_year1,{force: true})
      .get(selectDistrict).select(this.data.legislative_dist1,{force: true})
      .get(mapsDiv).should('exist')
      .get(footer).should('exist')
  })

    it('Test search and reset are not disabled for community partner under filters', function() {
      const communityPartnersLink = '[data-cy="communitypartners"]',
        filtersButton = '[data-cy="filters"]',
        footer = '[data-cy="footer"]',
        mapsDiv = '[data-cy="mapcanvas"]',
        mapsLink = '[data-cy="maps"]',
        searchInput = '[data-cy="search"]',
        resetFilters = '[data-cy="reset"]'
      cy.get(mapsLink).contains('Maps').click()
        .get(communityPartnersLink).click()
        .url().should('be.equal', Cypress.env('baseUrl')+'community-Partner')
      // filter button clicking and asserting to check the button is not disabled
        .get(filtersButton).click().should('not.be.disabled')
        .get(searchInput).click().type('Arts').should('not.be.disabled')
      // reset button clicking and asserting to check the button is not disabled
        .get(resetFilters).click().should('not.be.disabled')
        .get(mapsDiv).should('exist')
        .get(footer).should('exist')
    })
  
    it('should interact with the map by zoom in and zoom', () => {
      const communityPartnersLink = '[data-cy="communitypartners"]',
      mapsLink = '[data-cy="maps"]',
      mapsDiv = '[data-cy="mapcanvas"]'
      cy.get(mapsLink).contains('Maps').click()
        .get(communityPartnersLink).click()
        .get(mapsDiv).click(50, 50) // Click on the map at coordinates (50, 50)
        .get('[tabindex="0"] > img').click({force: true}); cy.wait(1000)
        .get('[tabindex="0"] > img').rightclick(); cy.wait(1000) //has context menu
        .get('.gm-style button[title="Zoom in"]').click() // Click the zoom in button
        .get('.gm-style button[title="Zoom out"]').click() // Click the zoom out button
    })
  
    it('Card should be displayed when right clicked on a map marker', () => {
      const communityPartnersLink = '[data-cy="communitypartners"]',
        mapsLink = '[data-cy="maps"]',
        mapsDiv = '[data-cy="mapcanvas"]'
      cy.get(mapsLink).contains('Maps').click()
        .get(communityPartnersLink).click()
        .get(mapsDiv).click(50, 50) // Click on the map at coordinates (50, 50)
        .get('[tabindex="0"] > img').click({force: true}); cy.wait(1000)
        .get('[tabindex="0"] > img').rightclick()
        .get('span').contains('Community Partner:').should('be.visible') // Asserting on pop card fields
        .get('span').contains('Projects:').should('be.visible')
        .get('td').contains('td', 'Academic Year').should('be.visible')
        .get('td').contains('td', 'Name').should('be.visible') // Asserting on table field name
        .get('td').contains('td', 'Engagement Type').should('be.visible')
    })
  
    it('Card should be displayed when clicked on a map marker', () => {
      const communityPartnersLink = '[data-cy="communitypartners"]',
        mapsLink = '[data-cy="maps"]',
        mapsDiv = '[data-cy="mapcanvas"]'
      cy.get(mapsLink).contains('Maps').click()
        .get(communityPartnersLink).click()
        .get('#map_canvas').click(50, 50) // Click on the map at coordinates (50, 50)
      .get('[tabindex="0"] > img').click({force: true}); cy.wait(1000)
      .get('span').contains('span', 'Community Partner:').should('be.visible') // Asserting on pop card fields
      .get('span').contains('span', 'Total Number of Projects:').should('be.visible')
      .get('span').contains('span', 'City:').should('be.visible')
      .get('span').contains('span', 'Focus Areas:').should('be.visible')
      .get('span').contains('span', 'Community Partner Type:').should('be.visible')
      .get('span').contains('span', 'Campus Partner:').should('be.visible')
      .get('span').contains('span', 'Academic Year: ').should('be.visible')
      .get('span').contains('span', 'Website Link:').should('be.visible')
    })
  
    it('All map markers should be visible on the map canvas', () => {
      const communityPartnersLink = '[data-cy="communitypartners"]',
        mapsLink = '[data-cy="maps"]',
        markerImages = `img[src="https://maps.gstatic.com/mapfiles/transparent.png"]`,
        mapsDiv = '[data-cy="mapcanvas"]'
      cy.get(mapsLink).contains('Maps').click()
        .get(communityPartnersLink).click()
        .get(mapsDiv).should('exist')
        .get(markerImages).should('be.visible')
    })


    it('Test Reset filter ', function(){
      const communityPartnersLink = '[data-cy="communitypartners"]',
        filtersButton = '[data-cy="filters"]',
        footer = '[data-cy="footer"]',
        mapsDiv = '[data-cy="mapcanvas"]',
        mapsLink = '[data-cy="maps"]',
        missionAreaFilters = '[data-cy="missionareafilters"]',
        allCommunityPartnerTypes= '[data-cy="selectcommunitytype"]',
        selectCollege = '[data-cy="selectcollege"]',
        selectCampus = '[data-cy="selectcampus"]',
        resetLink = '[data-cy="reset"]'
      cy.get(mapsLink).contains('Maps').click()
        .get(communityPartnersLink).click()
        .url().should('be.equal', Cypress.env('baseUrl')+'community-Partner')
      // filter button clicking and asserting to check the button is not disabled
        .get(filtersButton).click().should('not.be.disabled')
      // Testing filters links function
       .get(missionAreaFilters).should('exist')
       .get(allCommunityPartnerTypes).select(this.data.community_type1,{force: true})
       .get(allCommunityPartnerTypes).contains('Business')
       .get(selectCollege).should('exist')
       .get(selectCampus).select(this.data.campus_partner1,{force: true})
       .get(selectCampus).contains('Marketing and Entrepreneurship')
       .get(resetLink).click({force: true})
       .get(allCommunityPartnerTypes).contains('All Community Partner Types')
       .get(selectCampus).contains('All Campus Partners')
       .get(mapsDiv).should('exist')
       .get(footer).should('exist')
  })
  });
  