beforeEach(() => {
  cy.on('uncaught:exception', (err, runnable) => {
    if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
    {
      return false
    }
  })
  cy.visit(Cypress.env('baseUrl'))
})

describe('community partner types maps test', () => {
  beforeEach(function() {
    cy.fixture("datareports").then(function(data) {
      this.data = data
    })
  })
  // This test is expected to pass visiting community partner types under maps as a public user.
  // Test is asserted on url, visibility of filters button, map canvas existence in the page loaded and existence of footer.
  it('Community partner types page visit ', function() {
    const communityPartnerTypesHref = `a[href="/community-Partner-Type"]`,
      filtersButton = '#sidebarCollapse',
      footerId = '#footer',
      mapsDivId = '#map_canvas',
      mapsLink = `a[class="nav-link dropdown-toggle"]`,
      noOfCommPartID ='#totalnumber'
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnerTypesHref).click()
      .url().should('be.equal', Cypress.env('baseUrl')+'community-Partner-Type')
    // Asserting to check the page title
      .get('div').contains('label', 'Community Partner Types Map')
    // Checking the number of community partners value is visible
      .get('div').contains('label', 'Number of Community Partners:')
    // Total numbers value  existence assertion
      .get(noOfCommPartID).should('be.visible')
      .get(filtersButton).should('be.visible')
      .get(mapsDivId).should('exist')
      .get(footerId).should('exist')
  })

  it('Testing map canvas button clickability ', function() {
    const communityPartnerTypesHref = `a[href="/community-Partner-Type"]`,
      filtersButton = '#sidebarCollapse',
      footerId = '#footer',
      mapsDivId = '#map_canvas',
      mapsLink = `a[class="nav-link dropdown-toggle"]`
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnerTypesHref).click()
      .url().should('be.equal', Cypress.env('baseUrl')+'community-Partner-Type')
      .get(filtersButton).should('be.visible')
      .get(mapsDivId).should('exist')
      .get(footerId).should('exist')
    cy.get('#map_canvas').then($canvas => {
      // South Carolina
      // Wrap the canvas with the Cypress API, scroll it into view, and click in the location!
      cy.wrap($canvas)
        .scrollIntoView()
        .click(655, 340).wait(3000)
    });
  })

  it('Test filter dropdown are clickable', function() {
    const allFocusAreasDropdown = '#selectMission',
      allDistrictsDropdown = '#selectDistrict',
      allCollegesMainUnitsDropdown = '#selectCollege',
      allCampusPartnersDropdown = '#selectCampus',
      allAcademicYearsDropdown = '#selectYear',
      communityPartnerTypesHref = `a[href="/community-Partner-Type"]`,
      filtersButton = '#sidebarCollapse',
      footerId = '#footer',
      mapsDivId = '#map_canvas',
      mapsLink = `a[class="nav-link dropdown-toggle"]`
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnerTypesHref).click().wait(3000)
      .url().should('be.equal', Cypress.env('baseUrl')+'community-Partner-Type')
    // filter button clicking and asserting to check the button is not disabled
      .get(filtersButton).click().should('not.be.disabled')
    // select dropdown triggering click action to check it is clickable and asserting to check its not disabled
      .get(allFocusAreasDropdown).trigger('click').should('not.be.disabled')
      .get(allFocusAreasDropdown).select(this.data.focus_area2).should('exist')
    // select dropdown triggering click action to check it is clickable and asserting to check its not disabled
      .get(allCollegesMainUnitsDropdown).trigger('click').should('not.be.disabled')
      .get(allCollegesMainUnitsDropdown).select(this.data.college_name1).should('exist')

      .get(allCampusPartnersDropdown).trigger('click').should('not.be.disabled')
      .get(allCampusPartnersDropdown).should('exist')

      .get(allAcademicYearsDropdown).trigger('click').should('not.be.disabled')
      .get(allAcademicYearsDropdown).select(this.data.academic_year2).should('exist')

      .get(allDistrictsDropdown).trigger('click').should('not.be.disabled')
      .get(allDistrictsDropdown).select(this.data.legislative_dist2).should('exist')

      .get(mapsDivId).should('exist')
      .get(footerId).should('exist')
  })

  it('Test search and reset are not disabled for community partner under filters', function() {
    const communityPartnerTypesHref = `a[href="/community-Partner-Type"]`,
      filtersButton = '#sidebarCollapse',
      footerId = '#footer',
      mapsDivId = '#map_canvas',
      mapsLink = `a[class="nav-link dropdown-toggle"]`,
      searchInputId = '#valueFilter',
      resetFilters = `#reset`
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnerTypesHref).click()
      .url().should('be.equal', Cypress.env('baseUrl')+'community-Partner-Type')
    // filter button clicking and asserting to check the button is not disabled
      .get(filtersButton).click().should('not.be.disabled')
      .get(searchInputId).click().type('Arts').should('not.be.disabled')
      .get(resetFilters).click().should('not.be.disabled')
      .get(mapsDivId).should('exist')
      .get(footerId).should('exist')
  })

  it('Test community partner type filter links ', function() {
    const communityPartnerTypesHref = `a[href="/community-Partner-Type"]`,
      filtersButton = '#sidebarCollapse',
      footerId = '#footer',
      mapsDivId = '#map_canvas',
      mapsLink = `a[class="nav-link dropdown-toggle"]`,
      allCommunityPartnerTypesFIlterLink = `a[id="All Community Partner Types"]`,
      businessFIlterLink = `a[id="Business"]`,
      governmentAgencyFilterLink = `a[id="Government Agency"]`,
      higherEducationInstitutionFilterLink = `a[id="Higher Education Institution"]`,
      schoolsFilterLink = `a[id="K-12 Schools"]`,
      nonprofitFilterLink = `a[id="Nonprofit"]`
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnerTypesHref).click()
      .url().should('be.equal', Cypress.env('baseUrl')+'community-Partner-Type')
    // filter button clicking and asserting to check the button is not disabled
      .get(filtersButton).click().should('not.be.disabled')
      .get(allCommunityPartnerTypesFIlterLink).click()
      .get(businessFIlterLink).click()
      .get(governmentAgencyFilterLink).click()
      .get(higherEducationInstitutionFilterLink).click()
      .get(schoolsFilterLink).click()
      .get(nonprofitFilterLink).click()
      .get(mapsDivId).should('exist')
      .get(footerId).should('exist')
  })

  it('should interact with the map by zoom in and zoom', () => {
    const communityPartnerTypesHref = `a[href="/community-Partner-Type"]`,
      mapsLink = `a[class="nav-link dropdown-toggle"]`
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnerTypesHref).click()
      .get('#map_canvas').click(50, 50) // Click on the map at coordinates (50, 50)
      .get('[tabindex="0"] > img').click({force: true}); cy.wait(1000)
      .get('[tabindex="0"] > img').rightclick(); cy.wait(1000) //has context menu
      .get('.gm-style button[title="Zoom in"]').click() // Click the zoom in button
      .get('.gm-style button[title="Zoom out"]').click() // Click the zoom out button
  })

  it('Card should be displayed when right clicked on a map marker', () => {
    const communityPartnerTypesHref = `a[href="/community-Partner-Type"]`,
      mapsLink = `a[class="nav-link dropdown-toggle"]`
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnerTypesHref).click()
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
    const communityPartnerTypesHref = `a[href="/community-Partner-Type"]`,
      mapsLink = `a[class="nav-link dropdown-toggle"]`
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnerTypesHref).click()
      .get('#map_canvas').click(50, 50) // Click on the map at coordinates (50, 50)
      .get('[tabindex="0"] > img').click({force: true}); cy.wait(1000)
      .get('span').contains('span', 'Community Partner:').should('be.visible') // Asserting on pop card fields
      .get('span').contains('span', 'Total Number of Projects:').should('be.visible')
      .get('span').contains('span', 'City:').should('be.visible')
      .get('span').contains('span', 'Focus Areas:').should('be.visible')
      .get('span').contains('span', 'Community Partner Types:').should('be.visible')
      .get('span').contains('span', 'Campus Partner:').should('be.visible')
      .get('span').contains('span', 'Academic Year: ').should('be.visible')
      .get('span').contains('span', 'Website Link:').should('be.visible')
  })

  it('All map markers should be visible on the map canvas', () => {
    const communityPartnerTypesHref = `a[href="/community-Partner-Type"]`,
      mapsLink = `a[class="nav-link dropdown-toggle"]`,
      markerImages = `img[src="https://maps.gstatic.com/mapfiles/transparent.png"]`
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnerTypesHref).click()
      .get('#map_canvas').should('exist')
      .get(markerImages).should('be.visible') // Testing marker images are visible in the map canvas
  })
})
