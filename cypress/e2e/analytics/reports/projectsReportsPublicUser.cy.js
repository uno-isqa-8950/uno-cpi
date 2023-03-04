/// <reference types="cypress"/>
beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('reading \'style\''))
        {
            return false
        }
    })
    cy.visit(Cypress.env('baseUrl'))
})
describe('Analytic Reports Public user', () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
        this.data = data
        })
    })
    it('visits the form', function() {
        cy.visit(Cypress.env('baseUrl'))
    })
   //Check navigation
   it('Check navigation', function() {
    cy.contains('Analytics').click()
    cy.contains('Reports').next('.dropdown-menu').then($el => {
        cy.wrap($el).invoke('show')
        cy.wrap($el).contains('Projects').click()
    })
    })
    it('Check if it is Projects Report', function() {
        cy.contains('Analytics').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Projects').click()
        })
        cy.get('.heading').should('contain.text', 'Projects Report')
    })
    it('Hide Filters', function() {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Projects').click()
        })
        cy.get('#btn').should('have.class', 'btn btn-secondary')
        cy.get('#btn').click()
        cy.get('.select2-selection__placeholder').should('not.be.visible')
        // check the filers are they visible
        cy.get('#btn').click()
        cy.get('#btn').should('have.class', 'btn btn-secondary')
        cy.get('.select2-selection__placeholder').should('be.visible')
        })
    it.skip('Reset Filters', function() {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Projects').click()
        })
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li) => {
            cy.wrap($li).contains(this.data.academic_year1).click();
        })
        cy.get('#select2-id_community_type-container').click()
        cy.get('#select2-id_community_type-results').then(($li) => {
            cy.wrap($li).contains(this.data.community_type3).click();
        })
        cy.get('#select2-id_academic_year-container').should('contain.text', this.data.academic_year1)
        cy.get('#btn-reset').click()
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
        })
    // Filter Options
    it('filter options', function() {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Projects').click()
        })
        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li) => {
            cy.wrap($li).contains(this.data.academic_year4).click();
        })
        cy.get('#select2-id_mission-container').click()
        cy.get('#select2-id_mission-results').then(($li) => {
            cy.wrap($li).contains(this.data.focus_area4).click();
        })
        cy.get('#select2-id_engagement_type-container').click()
        cy.get('#select2-id_engagement_type-results').then(($li) => {
            cy.wrap($li).contains(this.data.engagement_type1).click();
        })
        cy.get('#select2-id_community_type-container').click()
        cy.get('#select2-id_community_type-results').then(($li) => {
            cy.wrap($li).contains(this.data.community_type5).click();
        })
        cy.get('#select2-id_college_name-container').click()
        cy.get('#select2-id_college_name-results').then(($li) => {
            cy.wrap($li).contains(this.data.college_name1).click();
        })
        cy.get('#select2-id_campus_partner-container').click()
        cy.get('#select2-id_campus_partner-results').then(($li) => {
            cy.wrap($li).contains(this.data.select_all).click();
        })
        cy.get('#select2-id_weitz_cec_part-container').click()
        cy.get('#select2-id_weitz_cec_part-results').then(($li) => {
            cy.wrap($li).contains(this.data.cec_part4).click();
        })
    })

    it("Check Card View", function() 
    {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Projects').click()
        })
        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li) => {
            cy.wrap($li).contains(this.data.academic_year1).click();
        })
        cy.get('#select2-id_mission-container').click()
        cy.get('#select2-id_mission-results').then(($li) => {
        cy.wrap($li).contains(this.data.focus_area4).click();
        })
        cy.get('#select2-id_engagement_type-container').click()
        cy.get('#select2-id_engagement_type-results').then(($li) => {
            cy.wrap($li).contains(this.data.select_all).click();
        })
        cy.get('#select2-id_campus_partner-container').click()
        cy.get('#select2-id_campus_partner-results').then(($li) => {
            cy.wrap($li).contains(this.data.campus_partner3).click();
        })
        //verify if theye are present in card structure
        cy.get('div[class="card-toptext"]').contains(this.data.focus_area4).should("be.visible")
        cy.get('span[id="academic_year"]').contains(this.data.academic_year1).should("be.visible")
        cy.get('div[class="col-md-6 col-lg-6 col-sm-12"]').contains("Community Partners:").should("be.visible")
        cy.get('div[class="col-md-6 col-lg-6 col-sm-12"]').contains("Campus Partners:").should("be.visible")
        //cy.get('div [class="col-md-6 col-lg-6 col-sm-12"] > .ul').children().contains(this.data.campus_partner3).should("be.visible")
        //cy.get('div[class="col-sm-12 col-lg-6"]').contains("Engagement Types:").should("be.visible")
    })
    it("Check Table view", function()
    {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Projects').click()
        })
        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li) => {
            cy.wrap($li).contains(this.data.academic_year1).click();
        })
        cy.get('#select2-id_mission-container').click()
        cy.get('#select2-id_mission-results').then(($li) => {
        cy.wrap($li).contains(this.data.focus_area4).click();
        })

        cy.get('#btn-table').click()
        cy.get('.buttons-csv').should("be.visible").click()
        cy.get('.buttons-pdf').should("be.visible").click()
        cy.get(':nth-child(1) > .sorting_1').click()
        cy.get('[data-dtr-index="8"] > .dtr-data').contains(this.data.academic_year1)
        cy.get('tbody > :nth-child(1) > :nth-child(2)').contains(this.data.focus_area4)
        cy.get('tbody > :nth-child(4) > :nth-child(2)').contains(this.data.focus_area4)
        cy.get('#btn-table').click()
        //check button visble for import and export
        cy.get(':nth-child(1) > .card-header > .media > .media-body > .card-toptext > .media-subheading > :nth-child(1)').contains((this.data.focus_area4))
    })
})