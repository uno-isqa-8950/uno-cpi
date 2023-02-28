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
  // This test is expected to pass visiting community partners under maps as a public user.
  // Test is asserted on url, visibility of filters button, map canvas existence in the page loaded and existence of footer.
  it('Community partners page visit ', () => {
    const communityPartnersHref = `a[href="/community-Partner"]`,
      filtersButton = '#sidebarCollapse',
      footerId = '#footer',
      mapsDivId = '#map_canvas',
      mapsLink = `a[class="nav-link dropdown-toggle"]`,
      noOfCommPartID ='#totalnumber'
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnersHref).click()
      .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/community-Partner')
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

  it('Testing map canvas button clickability ', () => {
    const communityPartnersHref = `a[href="/community-Partner"]`,
      filtersButton = '#sidebarCollapse',
      footerId = '#footer',
      mapsDivId = '#map_canvas',
      mapsLink = `a[class="nav-link dropdown-toggle"]`
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnersHref).click()
      .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/community-Partner')
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
      .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/community-Partner')
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

  it('Test search and reset are not disabled for community partner under filters', () => {
    const communityPartnersHref = `a[href="/community-Partner"]`,
      filtersButton = '#sidebarCollapse',
      footerId = '#footer',
      mapsDivId = '#map_canvas',
      mapsLink = `a[class="nav-link dropdown-toggle"]`,
      searchInputId = '#valueFilter',
      resetFilters = `#reset`
    cy.get(mapsLink).contains('Maps').click()
      .get(communityPartnersHref).click()
      .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/community-Partner')
    // filter button clicking and asserting to check the button is not disabled
      .get(filtersButton).click().should('not.be.disabled')
      .get(searchInputId).click().type('Arts').should('not.be.disabled')
    // reset button clicking and asserting to check the button is not disabled
      .get(resetFilters).click().should('not.be.disabled')
      .get(mapsDivId).should('exist')
      .get(footerId).should('exist')
  })
  });
  