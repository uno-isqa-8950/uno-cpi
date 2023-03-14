beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
      {
        return false
      }
    })
    cy.visit(Cypress.env('baseUrl'))
    
  })
  
  describe('City district maps test', () => {
        beforeEach(function() {         
        cy.fixture("datareports").then(function(data) {       
        this.data = data         
        }) 
        
    }) 
  
    // This test is expected to pass visiting community partners under maps as a public user.
    // Test is asserted on url, visibility of filters button, map canvas existence in the page loaded and existence of footer.
    it('projects maps visit ', function() {
      const communityPartnersHref = `a[href="/project-Map"]`,
        filtersButton = '#sidebarCollapse',
        footerId = '#footer',
        mapsDivId = '#map_canvas',
        mapsLink = `a[class="nav-link dropdown-toggle"]`,
        noOfCommPartID ='#totalnumber',
        navbar ='.navbar'
      cy.get(mapsLink).contains('Maps').click()
        .get(communityPartnersHref).click()
         .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/project-Map')
      // Asserting to check the page title
        cy.get(navbar).should('exist')
      // Checking the number of community partners value is visible
        .get('div').contains('label', 'Projects Map')
      // Total numbers value  existence assertion
        .get(noOfCommPartID).should('be.visible')
        .get(filtersButton).should('be.visible')
        .get(mapsDivId).should('exist')
        .get(footerId).should('exist')
       
    }) 

    it.only('Testing map canvas button clickability ', function() {
      const communityPartnerTypesHref = `a[href="/project-Map"]`,
        filtersButton = '#sidebarCollapse',
        footerId = '#footer',
        mapsDivId = '#map_canvas',
        mapsLink = `a[class="nav-link dropdown-toggle"]`
      cy.get(mapsLink).contains('Maps').click()
        .get(communityPartnerTypesHref).click()
        .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/project-Map')
        .get(filtersButton).should('be.visible')
        .get(mapsDivId).should('exist')
        .get(footerId).should('exist')
      cy.get('#map_canvas').then($canvas => {
        // South Carolina
        // Wrap the canvas with the Cypress API, scroll it into view, and click in the location!
           const Map_point = '[tabindex="0"] > img',
           Map_point_details = '.gm-style-iw-d > div > :nth-child(1)',
           Map_point_details1 = '.gm-style-iw-d > div > :nth-child(3)',
          Map_point_details4 = '.gm-style-iw-d > div > :nth-child(9)'
        cy.wrap($canvas)
          cy.get(Map_point).click(); cy.wait(1000)
          cy.get(Map_point_details).contains(this.data.Project_Name).should('be.visible')
          cy.get(Map_point_details1).contains(this.data.Focus_Areas).should('be.visible')
          cy.get(Map_point_details4).contains(this.data._comment7).should('be.visible')                   
      });
    })


    it ('Test filter dropdown are clickable', function()  {

          const communityPartnersHref = `a[href="/project-Map"]`,
      
            filtersButton = '#sidebarCollapse',
      
            footerId = '#footer',
      
            districtsDropdown = '#selectDistrict',
      
            mapsDivId = '#map_canvas',
      
            mapsLink = `a[class="nav-link dropdown-toggle"]`,
      
            communityPartnerDropdown = '#selectCommunityType',
      
            selectCollegeDropdown = '#selectCollege',
      
            selectCampusPartnerDropdown = '#selectCampus',
      
            selectYearDropdown = '#selectYear',
            
            reset = 'u'
      
          cy.get(mapsLink).contains('Maps').click()
      
            .get(communityPartnersHref).click()
      
            .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/project-Map')
      
          // filter button clicking and asserting to check the button is not disabled
      
            .get(filtersButton).click().should('not.be.disabled')
      
          // select dropdown triggering click action to check it is clickable and asserting to check its not disabled
      
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
