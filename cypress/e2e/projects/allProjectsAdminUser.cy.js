import user from "../../support/commands.js";
describe('all projects admin user test', () => {
beforeEach(() => {
    cy.on('uncaught:exception', (err) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
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
     
    it('Test all projects page navigation bar', function(){
      const unoLogo = '[data-cy="himg"]',
        navigationList = '[data-cy="navbar"]',
        userInfo = '[data-cy="accountinfo"]',
        projectsId = '[data-cy="projectsnav"]',
        allProjectsHref = '[data-cy="allprojects"]'
      cy.get(projectsId).should('exist').click()
        .get(allProjectsHref).should('exist').click()
        .get(unoLogo).should('be.visible')
        .get(navigationList).should('be.visible').contains('Maps')
        .get(navigationList).contains('Analytics')
        .get(navigationList).contains('Projects')
        .get(navigationList).contains('Partners')
        .get(navigationList).contains('Resources')
        .get(userInfo).should('be.visible') 
    })

    it('Test all projects page navigation bar, title and footer', function(){
      const projectsId = '[data-cy="projectsnav"]',
        allProjectsHref = '[data-cy="allprojects"]',
        footerId = '[data-cy="footer"]'
      cy.get(projectsId).should('exist').click()
        .get(allProjectsHref).should('exist').click()
        .url().should('be.equal', Cypress.env('baseUrl')+'allProjects/')
        .get('h4').contains("All Projects").should("be.visible")
        .get(footerId).should('exist')
    })

    it('Test all projects page filter card', function(){
      const projectsId = '[data-cy="projectsnav"]',
        allProjectsHref = '[data-cy="allprojects"]',
        filtersForm = '[data-cy="filtersform"]'
      cy.get(projectsId).should('exist').click()
        .get(allProjectsHref).should('exist').click()
        .get(filtersForm).should('be.visible')
        .get('label').contains('Academic Years')
        .get('label').contains('Project Focus Areas')
        .get('label').contains('Community Organization Types')
        .get('label').contains('College and Main Units')
        .get('label').contains('Campus Partners')
        .get('label').contains('CEC Building Partners')
        .get('label').contains('Engagement Types')
        .get('label').contains('K-12 Involvement')  
    })

    it('Test all projects page excel, pdf, hide filters and reset filters button', function(){
      const projectsId = '[data-cy="projectsnav"]',
        allProjectsHref =  '[data-cy="allprojects"]',
        filtersForm = '[data-cy="filtersform"]',
        hideFiltersButton = '[data-cy="hidefilters"]',
        resetFiltersButton ='[data-cy="resetfilters"]',
        applyFiltersButton = '[data-cy="applyfilters"]'
      cy.get(projectsId).should('exist').click()
        .get(allProjectsHref).should('exist').click()
        .get(filtersForm).should('be.visible')
        .get('button').contains('Excel').should('be.visible').click()
        .get('button').contains('PDF').should('be.visible').click() 
        .get(hideFiltersButton).should('be.visible').click()
        .get(resetFiltersButton).should('be.visible').click()
        .get(applyFiltersButton).should('be.visible').click()
    })

    it('Test projects page filter selections for academic years', function(){
      const projectsId = '[data-cy="projectsnav"]',
        allProjectsHref = '[data-cy="allprojects"]',
        filterOptionSelection = `span[class="select2-selection select2-selection--single"]`,
        tableData = `td[class="sorting_1"]`,
        applyFilters = '[data-cy="applyfilters"]'
      cy.get(projectsId).should('exist').click()
        .get(allProjectsHref).should('exist').click()
       // selecting filter option from  academic years filters 
        .get(filterOptionSelection).contains('Previous Academic Year').click()  
        .get('#select2-id_academic_year-results').then(($li) => {
           cy.wrap($li)
             .contains(this.data.academic_year1)
             .click()
           })
        .get(applyFilters).click()
      cy.get(tableData).contains(this.data.academic_year1)
    })

    it('Test projects page filter selections for project focus areas', function(){
      const projectsId = '[data-cy="projectsnav"]',
        allProjectsHref = '[data-cy="allprojects"]',
        filterOptionSelection = `span[class="select2-selection__placeholder"]`,
        applyFilters = '[data-cy="applyfilters"]' 
      cy.get(projectsId).should('exist').click()
        .get(allProjectsHref).should('exist').click()
       // selecting filter option from all project focus areas filters 
      .get(filterOptionSelection).contains('All Project Focus Areas').click()  
      .get('#select2-id_mission-results').then(($li) => {
           cy.wrap($li)
             .contains(this.data.focus_area2)
             .click()
           })
      .get(applyFilters).click()
    cy.get('td').contains(this.data.focus_area2)
  })

    it('Test projects page filter selections for project community organization types', function(){
      const projectsId = '[data-cy="projectsnav"]',
        allProjectsHref = '[data-cy="allprojects"]',
        filterOptionSelection = `span[class="select2-selection__placeholder"]`,
        applyFilters = '[data-cy="applyfilters"]' 
      cy.get(projectsId).should('exist').click()
        .get(allProjectsHref).should('exist').click()
       // selecting filter option from all community organization types
        .get(filterOptionSelection).contains('All Community Organization Types').click()  
        .get('#select2-id_community_type-results').then(($li) => {
           cy.wrap($li)
             .contains(this.data.community_type1)
             .click()
           })
        .get(applyFilters).click()
    })

    it('Test projects page filter selections for college and main units', function(){
      const projectsId = '[data-cy="projectsnav"]',
        allProjectsHref = '[data-cy="allprojects"]',
        filterOptionSelection = `span[class="select2-selection__placeholder"]`,
        applyFilters = '[data-cy="applyfilters"]'  
      cy.get(projectsId).should('exist').click()
        .get(allProjectsHref).should('exist').click()
       // selecting filter option from college and main units
        .get(filterOptionSelection).contains('All College and Main Units').click()  
        .get('#select2-id_college_name-results').then(($li) => {
           cy.wrap($li)
             .contains(this.data.college_name1)
             .click()
           })
        .get(applyFilters).click() 
    })
    
    it('Test projects page filter selections for campus partners', function(){
      const projectsId = '[data-cy="projectsnav"]',
        allProjectsHref = '[data-cy="allprojects"]',
        filterOptionSelection = `span[class="select2-selection__placeholder"]`,
        applyFilters = '[data-cy="applyfilters"]' 
      cy.get(projectsId).should('exist').click()
        .get(allProjectsHref).should('exist').click()
       // selecting filter option from campus partners
        .get(filterOptionSelection).contains('All Campus Partners').click()  
        .get('#select2-id_campus_partner-results').then(($li) => {
           cy.wrap($li)
             .contains(this.data.campus_partner6)
             .click()
           })
        .get(applyFilters).click()
      cy.get('td').contains(this.data.campus_partner6)
    })

    it('Test projects page filter selections for CEC building partners', function(){
      const projectsId = '[data-cy="projectsnav"]',
        allProjectsHref = '[data-cy="allprojects"]',
        filterOptionSelection = `span[class="select2-selection__placeholder"]`,
        applyFilters = '[data-cy="applyfilters"]'   
      cy.get(projectsId).should('exist').click()
        .get(allProjectsHref).should('exist').click()
       // selecting filter option from CEC building partners
        .get(filterOptionSelection).contains('All (CEC/Non-CEC Partners)').click()  
        .get('#select2-id_weitz_cec_part-results').then(($li) => {
           cy.wrap($li)
             .contains(this.data.cec_part2)
             .click()
           })
        .get(applyFilters).click()
    })

    it('Test projects page filter selections for Engagement types', function(){
      const projectsId ='[data-cy="projectsnav"]',
        allProjectsHref ='[data-cy="allprojects"]',
        filterOptionSelection = `span[class="select2-selection__placeholder"]`,
        applyFilters = '[data-cy="applyfilters"]'  
      cy.get(projectsId).should('exist').click()
        .get(allProjectsHref).should('exist').click()
       // selecting filter option from all engagement types
        .get(filterOptionSelection).contains('All Engagement Types').click()  
        .get('#select2-id_engagement_type-results').then(($li) => {
           cy.wrap($li)
             .contains(this.data.engagement_type2)
             .click()
           })
        .get(applyFilters).click()
      cy.get('td').contains(this.data.engagement_type2)
    })

    it('Test projects page filter selections for K-12 involvement', function(){
      const projectsId = '[data-cy="projectsnav"]',
        allProjectsHref ='[data-cy="allprojects"]',
        filterOptionSelection = `span[class="select2-selection__placeholder"]`,
        applyFilters = '[data-cy="applyfilters"]' 
      cy.get(projectsId).should('exist').click()
        .get(allProjectsHref).should('exist').click()
       // selecting filter option from K-12 involvement
        .get(filterOptionSelection).contains('All K-12 Involvement').click()  
        .get('#select2-id_k12_flag-results').then(($li) => {
           cy.wrap($li)
             .contains(this.data.k12_involve1)
             .click()
           })
        .get(applyFilters).click()
    })
  });