import user from "../../support/commands.js";
/// <reference types="cypress"/>
beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') ||err.message.includes('Cannot read properties of null') ||err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('reading \'style\''))
        {
            return false
        }
    })
    cy.visit(Cypress.env('baseUrl'))

})
describe('My Drafts - campus partner user', () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
           this.data = data
        cy.get('#login').click()
        cy.loginCampusUser(user)
        })
    })
    it('Check login form', function() {
        cy.url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
    })
    it ('Create test data for checking "My Drafts"', function() {
    cy.url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
    cy.get('#uno').click()
    cy.get('#projectsnav').click()
    cy.contains('Create Project').click()
    cy.get('#select2-academicYear-container').click()
    cy.get('#select2-academicYear-results').then(($li) => {
        cy.wrap($li).contains(this.data.select_all).click();
    })
    cy.get('#projectName').type(this.data.project_name1)
    cy.get('.save').click()
    cy.get('#button-id > :nth-child(2) > div > label').should('contain','The project that you are searching for does not exist, to proceed with the creation of a new project, click on the above button.')
    cy.get('#lnk-create_project').should('be.visible').click()
    cy.get('#select2-id_engagement_type-container').click()
    cy.get('#select2-id_engagement_type-results').then(($li) => {
        cy.wrap($li).contains(this.data.engagement_type5).click();
    })
    cy.get('#id_description').type("Project description for Capstone project")
    cy.get('#projectdurationnav > .fa').click()
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
    cy.get('#draft').click()
    // test data 2 
    cy.get('#projectsnav').click()
    cy.contains('Create Project').click()
    cy.get('#select2-academicYear-container').click()
    cy.get('#select2-academicYear-results').then(($li) => {
        cy.wrap($li).contains(this.data.select_all).click();
    })
    cy.get('#projectName').type(this.data.project_name2)
    cy.get('.save').click()
    cy.get('#button-id > :nth-child(2) > div > label').should('contain', 'The project that you are searching for does not exist, to proceed with the creation of a new project, click on the above button.')
    cy.get('#lnk-create_project').should('be.visible').click()
    cy.get('#select2-id_engagement_type-container').click()
    cy.get('#select2-id_engagement_type-results').then(($li) => {
        cy.wrap($li).contains(this.data.engagement_type2).click();
    })
    cy.get('#id_description').type("Project description for Capstone project data 2")
    cy.get('#projectdurationnav > .fa').click()
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
    cy.get('#draft').click()
    })

    it('My Draft - Edit option', function() {
    cy.url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
    cy.get('#uno').click()
    cy.get('#projectsnav').click()
    cy.contains('My Drafts').click()
    cy.get('#example_filter > label > .form-control').type(this.data.project_name1+'{enter}').click()
    cy.get(':nth-child(1) > .sorting_1').click()
    cy.get('.dtr-data > .btn-secondary').should('contain', 'Edit').click()
    cy.get('#id_description').type(".Project submitted & created")
    cy.get('#projectdurationnav > .fa').click()
    cy.get('#select2-id_project_type-container').click()
    cy.get('#select2-id_project_type-results').then(($li) => {
        cy.wrap($li).contains('Project').click();
    })
    cy.get('#participantinfonav > .fa').click()
    cy.get('#id_total_uno_students').type("6")
    cy.get('#id_total_uno_hours').type("300")
    cy.get('.sw-btn-next').click()
    cy.get('#campuspartnerinfonav').click()
    cy.get('#id_campus_edit-0-campus_partner').select(this.data.campus_partner3)
    cy.get('.input-group-append > .centered').click()
    cy.get('.sw-btn-next').click()
    cy.get('#id_mission_area').select(this.data.focus_area4)
    cy.get('.sw-btn-next').click()
    cy.get('#id_address_line1').type('address1')
    cy.get('#id_city').type('Omaha')
    cy.get('#id_country').type('US')
    cy.get('#id_state').type('NE')
    cy.get('#id_zip').type('68111')
    cy.get('#termsdiv > p').should('contain', "I agree to the Terms")
    cy.get('#terms').click()
    cy.get('#submit').click()
    cy.url().should('be.equal', Cypress.env('baseUrl')+'submit-project-done/')
    cy.get('.box > p').should('contain', 'My Projects')
    cy.get('[style=" color: #d71920;"]').click()
    cy.url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
    cy.get('#example_filter > label > .form-control').type(this.data.project_name1+'{enter}')
    cy.get('.sorting_1').should('contain',this.data.project_name1).click()
    cy.get('.sorting_1').should('contain',this.data.project_name1)
    //cy.get('.odd > :nth-child(2)').should('contain', this.data.focus_area4 )
    //cy.get('.odd > :nth-child(4)').should('contain', this.data.campus_partner3)
    //verify project creation in Admin panel
    cy.get('#accountinfo > .nav-link').click()
    cy.get('#logout').click()
    // login as admin
    cy.get('#login').click()
    cy.loginAdminUser(user)
    cy.visit(Cypress.env('baseUrl')+'admin/')
    //check Projects database
    cy.get('.model-project > th > a').click()
    cy.get('#searchbar').type(this.data.project_name1)
    cy.get('#changelist-search > div > [type="submit"]').click()
    cy.get('.field-project_name > a').should('contain', this.data.project_name1).click()
    cy.get('#content > h2').should('contain', this.data.project_name1)
    cy.get('#id_engagement_type').should('contain', this.data.engagement_type5)

    cy.get('#id_description').should('contain', 'Project description for Capstone project.Project submitted & created')
    cy.get('#id_status').should('contain', 'Active')
    cy.get('#id_project_type').should('contain', 'Project')
    })

    it('My Draft - Delete option', function() {
    cy.url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
    cy.get('#uno').click()
    cy.get('#projectsnav').click()
    cy.contains('My Drafts').click()
    cy.get('#example_filter > label > .form-control').type(this.data.project_name2+'{enter}').click()
    cy.get('.sorting_1').click()
    cy.get('.dtr-data > .btn-cancel').should('contain', 'Delete').click()
    cy.get('#example_filter > label > .form-control').type(this.data.project_name2+'{enter}').click()
    cy.get('#example_info').should('contain','Showing 0 to 0 of 0 entries')
    //verify project creation in Admin panel
    cy.get('#accountinfo > .nav-link').click()
    cy.get('#logout').click()
    // login as admin
    cy.get('#login').click()
    cy.loginAdminUser(user)
    cy.visit(Cypress.env('baseUrl')+'admin/')
    //check Projects database
    cy.get('.model-project > th > a').click()
    cy.get('#searchbar').type(this.data.project_name2)
    cy.get('#changelist-search > div > [type="submit"]').click()
    cy.get('.paginator').should('contain', '0 projects')
    })

    it('data cleanup', function() {
    cy.url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
    cy.get('#uno').click()
    cy.get('#projectsnav').click()
    cy.contains('My Projects').click()
    cy.get('#example_filter > label > .form-control').type(this.data.project_name1+'{enter}')
    cy.get('.sorting_1').should('contain',this.data.project_name1).click()
    cy.get('.dtr-data > .btn-cancel').click()
    cy.get('#example_filter > label > .form-control').type(this.data.project_name1+'{enter}')
    cy.get('#example_info').should('contain','Showing 0 to 0 of 0 entries')
    })
})