  describe('Maps for Project maps campus partner user test', () => {
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
      cy.loginCampusUser()  // Campus User is logged in before the test begins
      cy.visit(Cypress.env('baseUrl'))
    })
  
    // This test is expected to pass visiting community partners under maps as a public user.
    // Test is asserted on url, visibility of filters button, map canvas existence in the page loaded and existence of footer.
    it('projects maps visit ', function() {
      const projectsHref = '[data-cy="projects"]',
      filtersButton = '[data-cy="filters"]',
      footerId = '[data-cy="footer"]',
      mapsDivId = '[data-cy="mapcanvas"]',
      mapsLink = '[data-cy="maps"]',
      noOfCommPartID ='[data-cy="totalnumber"]',
      navbar ='[data-cy="navbar"]'
      cy.get(mapsLink).contains('Maps').click()
        .get(projectsHref).click()
         .url().should('be.equal', Cypress.env('baseUrl')+'project-Map')
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

    it('Testing map canvas button clickability ', function() {
      const projectsHref = '[data-cy="projects"]',
        filtersButton = '[data-cy="filters"]',
        footerId = '[data-cy="footer"]',
        mapsDivId = '[data-cy="mapcanvas"]',
        mapsLink = '[data-cy="maps"]'
      cy.get(mapsLink).contains('Maps').click()
        .get(projectsHref).click()
        .url().should('be.equal', Cypress.env('baseUrl')+'project-Map')
        .get(filtersButton).should('be.visible')
        .get(mapsDivId).should('exist')
        .get(footerId).should('exist')
      cy.get('#map_canvas').then($canvas => {
        // South Carolina
        // Wrap the canvas with the Cypress API, scroll it into view, and click in the location!
        const Map_point = '[tabindex="0"] > img',
        Map_point_details = '.gm-style-iw-d > div > :nth-child(1)',
        Map_point_details1 = '.gm-style-iw-d > div > :nth-child(3)',
       Map_point_details4 = '.gm-style-iw-d > div > :nth-child(9)',
       Map_Zoom = '[aria-label="Zoom in"]'
       cy.wrap($canvas)
       cy.get(Map_Zoom).click()
      cy.get(Map_point).click(); cy.wait(1000)
       cy.get(Map_point_details).contains(this.data.Project_Name).should('be.visible')
       cy.get(Map_point_details1).contains(this.data.Focus_Areas).should('be.visible')
       cy.get(Map_point_details4).contains(this.data._comment7).should('be.visible')                   
   });
    })


    it('Test filter dropdown are clickable', function()  {

          const projectsHref = '[data-cy="projects"]',
        filtersButton = '[data-cy="filters"]',
        footerId = '[data-cy="footer"]',
        mapsDivId = '[data-cy="mapcanvas"]',
        mapsLink = '[data-cy="maps"]',
        districtsDropdown = '[data-cy="selectdistrict"]',
        communityPartnerDropdown = '[data-cy="selectcommunitytype"]',
      
        selectCollegeDropdown = '[data-cy="selectcollege"]',
      
        selectCampusPartnerDropdown = '[data-cy="selectcampus"]',
      
      selectYearDropdown = '[data-cy="selectyear"]',
            
            reset = '[data-cy="reset"]'
      
          cy.get(mapsLink).contains('Maps').click()
      
            .get(projectsHref).click()
      
            .url().should('be.equal', Cypress.env('baseUrl')+'project-Map')
      
          // filter button clicking and asserting to check the button is not disabled
      
            .get(filtersButton).click().should('not.be.disabled')
      
          // select dropdown triggering click action to check it is clickable and asserting to check its not disabled
      
            .get(districtsDropdown).trigger('click', {force: true}).should('not.be.disabled').select(this.data.All_Legislative_Districts, {force: true})

      cy.get(communityPartnerDropdown).trigger('click', {force: true}).should('not.be.disabled')
      .get(communityPartnerDropdown).select(this.data.community_type2, {force: true})

      .get(selectCollegeDropdown).trigger('click', {force: true}).should('not.be.disabled')
      .get(selectCollegeDropdown).select(this.data.All_Colleges_And_main_Units, {force: true})

      .get(selectCampusPartnerDropdown).trigger('click', {force: true}).should('not.be.disabled')
      .get(selectCampusPartnerDropdown).select(this.data.All_Campus_Partners, {force: true})

      .get(selectYearDropdown).trigger('click', {force: true}).should('not.be.disabled')
      .get(selectYearDropdown).select(this.data.All_Academic_Years, {force: true})
      
            .get(mapsDivId).should('exist')
      
            .get(footerId).should('exist')

            .get(reset).should('exist')
      
    })
})
