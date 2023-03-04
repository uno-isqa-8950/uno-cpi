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
      .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/community-Partner-Type')
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
      .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/community-Partner-Type')
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
      .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/community-Partner-Type')
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
      .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/community-Partner-Type')
    // filter button clicking and asserting to check the button is not disabled
      .get(filtersButton).click().should('not.be.disabled')
      .get(searchInputId).click().type('Arts').should('not.be.disabled')
      .get(resetFilters).click().should('not.be.disabled')
      .get(mapsDivId).should('exist')
      .get(footerId).should('exist')
  })
})
