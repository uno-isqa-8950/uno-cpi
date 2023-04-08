import user from "../../support/commands.js";
describe('My Drafts Administrator', () => {
beforeEach(() => {
    cy.on('uncaught:exception', (err) => {
      if(err.message.includes('is not a function') || err.message.includes('Cannot read properties of null') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
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
    it('Check login form', function() {
        cy.url().should('be.equal', Cypress.env('baseUrl'))
    })
    it('Create test data for checking "My Drafts"', function() {
    cy.url().should('be.equal', Cypress.env('baseUrl'))
    cy.get('[data-cy="cpi"]').click()
    cy.get('[data-cy="projectsnav"]').click()
    cy.get('[data-cy="createproject"]').click()
    cy.get('#select2-academicYear-container').click()
    cy.get('[data-cy="academicyear"]').select(this.data.select_all,{force:true})
    cy.get('[data-cy="projectnameinput"]').clear().type(this.data.project_name3)
    cy.get('[data-cy="search"]').click()
    cy.get('[data-cy="button-id"]').should('contain','The project that you are searching for does not exist, to proceed with the creation of a new project, click on the above button.')
    cy.get('[data-cy="createprojectbutton"]').should('be.visible').click()
    cy.get('#select2-id_engagement_type-container').click()
    cy.get('#select2-id_engagement_type-results').then(($li) => {
        cy.wrap($li).contains(this.data.engagement_type5).click();
    })
    cy.get('[data-cy="descriptioninput"]').type("Project description for Capstone project")
    cy.get('[data-cy="projectduration"] > .fa').click()
    cy.get('#select2-id_project_type-container').click()
    cy.get('#select2-id_project_type-results').then(($li) => {
        cy.wrap($li).contains('Project').click();
    })
    cy.get('#select2-id_semester-container').click()
    cy.get('#select2-id_semester-results').then(($li) => {
        cy.wrap($li).contains('Spring').click();
    })
    cy.get('#select2-id_academic_year-container').click()
    cy.get('#select2-id_academic_year-results').then(($li) => {
        cy.wrap($li).contains(this.data.academic_year1).click();
    })
    cy.get('[data-cy="saveasdraft"]').click()
    // test data 2 
    cy.get('[data-cy="projectsnav"]').click()
    cy.get('[data-cy="createproject"]').click()
    cy.get('#select2-academicYear-container').click()
    cy.get('[data-cy="academicyear"]').select(this.data.select_all,{force:true})
    cy.get('[data-cy="projectnameinput"]').clear().type(this.data.project_name4)
    cy.get('[data-cy="search"]').click()
    cy.get('[data-cy="button-id"]').should('contain','The project that you are searching for does not exist, to proceed with the creation of a new project, click on the above button.')
    cy.get('[data-cy="createprojectbutton"]').should('be.visible').click()
    cy.get('#select2-id_engagement_type-container').click()
    cy.get('#select2-id_engagement_type-results').then(($li) => {
        cy.wrap($li).contains(this.data.engagement_type2).click();
    })
    cy.get('[data-cy="descriptioninput"]').type("Project description for Capstone project")
    cy.get('[data-cy="projectduration"] > .fa').click()
    cy.get('#select2-id_project_type-container').click()
    cy.get('#select2-id_project_type-results').then(($li) => {
        cy.wrap($li).contains('Project').click();
    })
    cy.get('#select2-id_semester-container').click()
    cy.get('#select2-id_semester-results').then(($li) => {
        cy.wrap($li).contains('Fall').click();
    })
    cy.get('#select2-id_academic_year-container').click()
    cy.get('#select2-id_academic_year-results').then(($li) => {
        cy.wrap($li).contains(this.data.academic_year4).click();
    })
    cy.get('[data-cy="saveasdraft"]').click()
    })

    it('My Draft - Edit option', function() {
    cy.url().should('be.equal', Cypress.env('baseUrl'))
    cy.get('[data-cy="cpi"]').click()
    cy.get('[data-cy="projectsnav"]').click()
    cy.get('[data-cy="mydrafts"]').click()
    cy.get('[data-cy="mydrafts-heading"]').should('contain', 'My Drafts')
    cy.get('#example_filter > label > .form-control').type(this.data.project_name3+'{enter}').click()
    cy.get(':nth-child(1) > .sorting_1').click()
    cy.get('table').contains('td',this.data.project_name3)
          .parent()
          .find('a[data-cy="draft-edit"]').click({force:true})
    cy.get('#id_description').type(".Project submitted & created")
    cy.get('[data-cy="projectdurationnav"] > .fa').click()
    cy.get('#select2-id_project_type-container').click()
    cy.get('#select2-id_project_type-results').then(($li) => {
        cy.wrap($li).contains('Project').click();
    })
    cy.get('[data-cy="participantinfonav"] > .fa').click()
    cy.get('#id_total_uno_students').type("6")
    cy.get('#id_total_uno_hours').type("300")
    cy.get('.sw-btn-next').click()
    cy.get('[data-cy="campuspartnerinfonav"]').click()
    cy.get('#id_campus_edit-0-campus_partner').select(this.data.campus_partner3)
    cy.get('[data-cy="input-group-append"] > .centered').click()
    cy.get('.sw-btn-next').click()
    cy.get('[data-cy="id_mission_area"]').select(this.data.focus_area4)
    cy.get('.sw-btn-next').click()
    cy.get('#id_address_line1').type('address1')
    cy.get('#id_city').type('Omaha')
    cy.get('#id_country').type('US')
    cy.get('#id_state').type('NE')
    cy.get('#id_zip').type('68111')
    cy.get('[data-cy="termsdiv"] > p').should('contain', "I agree to the Terms")
    cy.get('#terms').click()
    cy.get('[data-cy="submit"]').click()
    cy.url().should('be.equal', Cypress.env('baseUrl')+'adminsubmit_project_done/')
    cy.get('[data-cy="allprojects-admin"]').should('contain', 'All Projects').click()
    cy.url().should('be.equal', Cypress.env('baseUrl')+'allProjects/')
    cy.get('#select2-id_academic_year-container').click()
    cy.get('[data-cy="academicyear"]').select(this.data.select_all,{force:true})
    cy.get('[data-cy="applyfilters"]').click()
    cy.get('#example_filter > label > .form-control').type(this.data.project_name3+'{enter}')
    cy.get('.sorting_1').should('contain',this.data.project_name3).click()
    cy.get('.sorting_1').should('contain',this.data.project_name3)
    //cy.get('.odd > :nth-child(2)').should('contain', this.data.focus_area4 )
    //cy.get('.odd > :nth-child(4)').should('contain', this.data.campus_partner3)
    //verify project creation in Admin panel
    cy.visit(Cypress.env('baseUrl')+'admin/')
    //check Projects database
    cy.get('.model-project > th > a').click()
    cy.get('#searchbar').type(this.data.project_name3)
    cy.get('#changelist-search > div > [type="submit"]').click()
    cy.get('.field-project_name > a').should('contain', this.data.project_name3).click()
    cy.get('#content > h2').should('contain', this.data.project_name3)
    cy.get('#id_engagement_type').should('contain', this.data.engagement_type5)
    cy.get('#id_description').should('contain', 'Project description for Capstone project.Project submitted & created')
    cy.get('#id_status').should('contain', 'Active')
    cy.get('#id_project_type').should('contain', 'Project')
    })

    it('My Draft - Delete option', function() {
    cy.url().should('be.equal', Cypress.env('baseUrl'))
    cy.get('[data-cy="cpi"]').click()
    cy.get('[data-cy="projectsnav"]').click()
    cy.get('[data-cy="mydrafts"]').click()
    cy.get('[data-cy="mydrafts-heading"]').should('contain', 'My Drafts')
    cy.get('#example_filter > label > .form-control').type(this.data.project_name4+'{enter}').click()
    cy.get('.sorting_1').click()
    cy.get('table').contains('td',this.data.project_name4)
          .parent()
          .find('a[data-cy="draft-delete"]').click({force:true})
    //cy.get('.dtr-data > .btn-cancel').should('contain', 'Delete').click()
    cy.get('#example_filter > label > .form-control').type(this.data.project_name4+'{enter}').click()
    cy.get('#example_info').should('contain','Showing 0 to 0 of 0 entries')
    //verify project creation in Admin panel
    cy.visit(Cypress.env('baseUrl')+'admin/')
    //check Projects database
    cy.get('.model-project > th > a').click()
    cy.get('#searchbar').type(this.data.project_name4)
    cy.get('#changelist-search > div > [type="submit"]').click()
    cy.get('.paginator').should('contain', '0 projects')
    })

    it('data cleanup', function() {
    cy.url().should('be.equal', Cypress.env('baseUrl'))
    cy.get('[data-cy="cpi"]').click()
    cy.get('[data-cy="projectsnav"]').click()
    cy.get('[data-cy="myprojects"]').click()
    cy.get('#example_filter > label > .form-control').type(this.data.project_name3+'{enter}')
    cy.get('.sorting_1').should('contain',this.data.project_name3).click()
    cy.get('table').contains('td',this.data.project_name3)
          .parent()
          .find('a[data-cy="projects_delete"]').click({force:true})
    cy.get('#example_filter > label > .form-control').type(this.data.project_name3+'{enter}')
    cy.get('#example_info').should('contain','Showing 0 to 0 of 0 entries')
    })
})