beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
      {
        return false
      }
    })
    cy.visit(Cypress.env('baseUrl'))
  })
  
  describe('legislative district maps test', () => {

    beforeEach(function() {         
      cy.fixture("datareports").then(function(data) {       
      this.data = data
      cy.get('#login').click()
      cy.loginCampusUser()
      }) 
      
  }) 
  
    // This test is expected to pass visiting community partners under maps as a public user.
    // Test is asserted on url, visibility of filters button, map canvas existence in the page loaded and existence of footer.
    it('legislative district page visit ', function() {
      const legislativedistrictHref = '[data-cy="legislative-District"]', 
        filtersButton = '[data-cy="sidebarCollapse"]',
        footerId = '[data-cy="footer"]',
        mapsDivId = '[data-cy="map_canvas"]',
        mapsLink = '[data-cy="maps"]',
        noOfCommPartID ='[data-cy="totalnumber"]',
        navbar ='[data-cy="navbar"]'
      cy.get(mapsLink).contains('Maps').click()
        .get(legislativedistrictHref).click()
        .url().should('be.equal', Cypress.env('baseUrl')+'legislative-District')
      // Asserting to check the page title
        cy.get(navbar).should('exist')
      // Checking the number of community partners value is visible
        .get('div').contains('label', 'Number of Community Partners:')
      // Total numbers value  existence assertion
        .get(noOfCommPartID).should('be.visible')
        .get(filtersButton).should('be.visible')
        .get(mapsDivId).should('exist')
        .get(footerId).should('exist')
    }) 


    it('Test filter dropdown are clickable', function()  {

      const legislativedistrictHref = '[data-cy="legislative-District"]', 
        filtersButton = '[data-cy="sidebarCollapse"]',
        footerId = '[data-cy="footer"]',
        mapsDivId = '[data-cy="map_canvas"]',
        mapsLink = '[data-cy="maps"]',     
        districtsDropdown = '[data-cy="selectDistrict"]',
        communityPartnerDropdown = '[data-cy="selectCommtype"]',
      
        selectCollegeDropdown = '[data-cy="selectCollege"]',
      
        selectCampusPartnerDropdown = '[data-cy="selectCampus"]',
      
      selectYearDropdown = '[data-cy="selectYear"]',
            
            reset = '[data-cy="reset"]'

              cy.get(mapsLink).contains('Maps').click()
      
            .get(legislativedistrictHref).click()
      
                  .url().should('be.equal', Cypress.env('baseUrl')+'legislative-District')
      
      //     // filter button clicking and asserting to check the button is not disabled
      
            .get(filtersButton).click().should('not.be.disabled')
      
      // // select dropdown triggering click action to check it is clickable and asserting to check its not disabled

            .get(districtsDropdown).trigger('click').should('not.be.disabled').select(this.data.All_Legislative_Districts)

            cy.get(communityPartnerDropdown).trigger('click').should('not.be.disabled')
            .get(communityPartnerDropdown).select(this.data.community_type2)
      
            .get(selectCollegeDropdown).trigger('click').should('not.be.disabled')
            .get(selectCollegeDropdown).select(this.data.All_Colleges_And_main_Units)
      
            .get(selectCampusPartnerDropdown).trigger('click').should('not.be.disabled')
            .get(selectCampusPartnerDropdown).select(this.data.All_Campus_Partners)
      
            .get(selectYearDropdown).trigger('click').should('not.be.disabled')
            .get(selectYearDropdown).select(this.data.All_Academic_Years)
      
            .get(mapsDivId).should('exist')
      
            .get(footerId).should('exist')

            .get(reset).should('exist')
      
        })
})
