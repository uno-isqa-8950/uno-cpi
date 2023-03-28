beforeEach(() => {
  cy.on('uncaught:exception', (err, runnable) => {
    if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
    {
      return false
    }
  })
  cy.visit(Cypress.env('baseUrl'))
})

describe('community partners maps test', () => {
  beforeEach(function() {
    cy.fixture("datareports").then(function(data) {
      this.data = data
      cy.get('#login').click()
      cy.loginCampusUser()
  })
})
  // This test is expected to pass visiting community partners under maps as a public user.
  // Test is asserted on url, visibility of filters button, map canvas existence in the page loaded and existence of footer.
  it('Community partners page visit with campus partner login ', function() {
    const communityPartnersHref = `a[href="/community-Partner"]`,
      filtersButton = '#sidebarCollapse',
      footerId = '#footer',
      mapsDivId = '#map_canvas',
      mapsLink = `a[class="nav-link dropdown-toggle"]`,
      noOfCommPartID ='#totalnumber'
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnersHref).click()
      .url().should('be.equal', this.data.baseUrl+'community-Partner')            
    // Asserting to check the page title
      .get('div').contains('label', 'Community Partners Map')
    // Checking the number of community partners value is visible
      .get('div').contains('label', 'Number of Community Partners:')
    // Total numbers value  existence assertion
      .get(noOfCommPartID).should('be.visible')
      .get(filtersButton).should('be.visible')
      .get(mapsDivId).should('exist')
      .get(footerId).should('exist')
  })

  it('Testing map canvas button clickability ', function() {
    const communityPartnersHref = `a[href="/community-Partner"]`,
      filtersButton = '#sidebarCollapse',
      footerId = '#footer',
      mapsDivId = '#map_canvas',
      mapsLink = `a[class="nav-link dropdown-toggle"]`
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnersHref).click()
      .url().should('be.equal', this.data.baseUrl+'community-Partner')
      .get(filtersButton).should('be.visible')
      .get(mapsDivId).should('exist')
      .get(footerId).should('exist')
    cy.get('#map_canvas').then($canvas => {
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
    
    const communityPartnersHref = `a[href="/community-Partner"]`,
      filtersButton = '#sidebarCollapse',
      footerId = '#footer',
      districtsDropdown = '#selectDistrict',
      mapsDivId = '#map_canvas',
      mapsLink = `a[class="nav-link dropdown-toggle"]`,
      communityPartnerDropdown = '#selectCommtype',
      selectCollegeDropdown = '#selectCollege',
      selectCampusPartnerDropdown = '#selectCampus',
      selectYearDropdown = '#selectYear'
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnersHref).click()
      .url().should('be.equal', this.data.baseUrl+'community-Partner')
    // filter button clicking and asserting to check the button is not disabled
      .get(filtersButton).click().should('not.be.disabled')
    // select dropdown triggering click action to check it is clickable and asserting to check its not disabled
      .get(districtsDropdown).trigger('click').should('not.be.disabled')
    // Selecting some value from dropdown. Here selecting legislative district 1 option from districts dropdown list
      .get(districtsDropdown).select(this.data.legislative_dist1).should('exist')

      .get(communityPartnerDropdown).trigger('click').should('not.be.disabled')
    // Selecting some value from dropdown. Here selecting business option from community partners dropdown list
      .get(communityPartnerDropdown).select(this.data.community_type1).should('exist')

      .get(selectCollegeDropdown).trigger('click').should('not.be.disabled')
    // Selecting some value from dropdown. Here selecting "Academic Affairs" option from select college dropdown list
      .get(selectCollegeDropdown).select(this.data.college_name1).should('exist')

      .get(selectCampusPartnerDropdown).trigger('click').should('not.be.disabled')

      .get(selectYearDropdown).trigger('click').should('not.be.disabled')
    // Selecting some value from dropdown. Here selecting "Academic year" option from select year dropdown list
      .get(selectYearDropdown).select(this.data.academic_year1).should('exist')

      .get(mapsDivId).should('exist')
      .get(footerId).should('exist')
  })

  it('Mission area filters links are clickable', function(){
    const communityPartnersHref = `a[href="/community-Partner"]`,
      filtersButton = '#sidebarCollapse',
      footerId = '#footer',
      mapsDivId = '#map_canvas',
      mapsLink = `a[class="nav-link dropdown-toggle"]`,
      allFocusAreasFilterLink = `a[id="All Focus Areas"]`,
      artsCultureHumanitiesLink = `a[id="Arts, Culture and Humanities"]`,
      economicImpactLink = `a[id="Economic Impact"]`,
      educationalSupportLink = `a[id="Educational Support"]`,
      environmentalStewardshipLink = `a[id="Environmental Stewardship"]`,
      healthAndWellnessLink = `a[id="Health and Wellness"]`,
      internationalServiceLink = `a[id="International Service"]`,
      socialJusticeLink = `a[id="Social Justice"]`  
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnersHref).click()
      .url().should('be.equal', this.data.baseUrl+'community-Partner')
    // filter button clicking and asserting to check the button is not disabled
      .get(filtersButton).click().should('not.be.disabled')
    // Testing filters links function
      .get(allFocusAreasFilterLink).click()
      .get(artsCultureHumanitiesLink).click()
      .get(economicImpactLink).click()
      .get(educationalSupportLink).click()
      .get(environmentalStewardshipLink).click()
      .get(healthAndWellnessLink).click()
      .get(internationalServiceLink).click()
      .get(socialJusticeLink).click()
      .get(mapsDivId).should('exist')
      .get(footerId).should('exist')
  })

  it('Test search and reset are not disabled for community partner under filters', function() {
    const communityPartnersHref = `a[href="/community-Partner"]`,
      filtersButton = '#sidebarCollapse',
      footerId = '#footer',
      mapsDivId = '#map_canvas',
      mapsLink = `a[class="nav-link dropdown-toggle"]`,
      searchInputId = '#valueFilter',
      resetFilters = `#reset`
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnersHref).click()
      .url().should('be.equal', this.data.baseUrl+'community-Partner')
    // filter button clicking and asserting to check the button is not disabled
      .get(filtersButton).click().should('not.be.disabled')
      .get(searchInputId).click().type('Arts').should('not.be.disabled')
    // reset button clicking and asserting to check the button is not disabled
      .get(resetFilters).click().should('not.be.disabled')
      .get(mapsDivId).should('exist')
      .get(footerId).should('exist')
  })

  it('should interact with the map by zoom in and zoom', () => {
    const communityPartnersHref = `a[href="/community-Partner"]`,
      mapsLink = `a[class="nav-link dropdown-toggle"]`
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnersHref).click()
      .get('#map_canvas').click(50, 50) // Click on the map at coordinates (50, 50)
      .get('[tabindex="0"] > img').click({force: true}); cy.wait(1000)
      .get('[tabindex="0"] > img').rightclick(); cy.wait(1000) //has context menu
      .get('.gm-style button[title="Zoom in"]').click() // Click the zoom in button
      .get('.gm-style button[title="Zoom out"]').click() // Click the zoom out button
  })

  it('Card should be displayed when right clicked on a map marker', () => {
    const communityPartnersHref = `a[href="/community-Partner"]`,
      mapsLink = `a[class="nav-link dropdown-toggle"]`
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnersHref).click()
      .get('#map_canvas').click(50, 50) // Click on the map at coordinates (50, 50)
      .get('[tabindex="0"] > img').click({force: true}); cy.wait(1000)
      .get('[tabindex="0"] > img').rightclick()
      .get('span').contains('span', 'Community Partner:').should('be.visible') // Asserting on pop card fields
      .get('span').contains('span', 'Projects:').should('be.visible')
      .get('td').contains('td', 'Academic Year').should('be.visible')
      .get('td').contains('td', 'Name').should('be.visible') // Asserting on table field name
      .get('td').contains('td', 'Engagement Type').should('be.visible')
  })

  it('Card should be displayed when clicked on a map marker', () => {
    const communityPartnersHref = `a[href="/community-Partner"]`,
      mapsLink = `a[class="nav-link dropdown-toggle"]`
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnersHref).click()
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
    const communityPartnersHref = `a[href="/community-Partner"]`,
      mapsLink = `a[class="nav-link dropdown-toggle"]`,
      markerImages = `img[src="https://maps.gstatic.com/mapfiles/transparent.png"]`
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnersHref).click()
      .get('#map_canvas').should('exist')
      .get(markerImages).should('be.visible')
  })
});
