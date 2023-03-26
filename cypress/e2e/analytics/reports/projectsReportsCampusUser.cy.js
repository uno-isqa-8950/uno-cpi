/// <reference types="cypress"/>
beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('reading \'style\''))
        {
            return false
        }
    })
    cy.visit(Cypress.env('baseUrl'))
    cy.loginCampusUser()
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
    cy.get('[data-cy="analytics"]').click()
    cy.get('[data-cy="reports"]').next('[data-cy="reportsdropdown"]').then($el => {
        cy.wrap($el).invoke('show')
        cy.wrap($el).get('[data-cy="projectsreport"]').click()
    })
    })
    it('Check if it is Projects Report', function() {
        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="reports"]').next('[data-cy="reportsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).get('[data-cy="projectsreport"]').click()
        })
        cy.get('[data-cy="heading"]').should('contain.text', 'Projects Report')
    })
    it('Hide Filters', function() {
        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="reports"]').next('[data-cy="reportsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).get('[data-cy="projectsreport"]').click()
        })
        cy.get('[data-cy="Hide Filters"]').should('have.class', 'btn btn-secondary')
        cy.get('[data-cy="Hide Filters"]').click() 
        cy.get('[data-cy="collapse show"]').should('not.be.visible')
        // check the filers are they visible
        cy.get('[data-cy="Hide Filters"]').click() 
        cy.get('[data-cy="Hide Filters"]').click() .should('have.class', 'btn btn-secondary')
        cy.get('[data-cy="collapse show"]').should('be.visible')
        })
    it('Reset Filters', function() {
        const academic_year_selector = '#select2-id_academic_year-container',
        academic_year_results =  '#select2-id_academic_year-results',
        community_containter = '#select2-id_community_type-container',
        community_results = '#select2-id_community_type-results'
        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="reports"]').next('[data-cy="reportsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).get('[data-cy="projectsreport"]').click()
        })
        cy.get('[data-cy="academic_year"]').contains('Previous Academic Year')
        cy.get(academic_year_selector).click()
        cy.get(academic_year_results).then(($li) => {
            cy.wrap($li).contains(this.data.academic_year1).click();
        })

        cy.get(community_containter).click()
        cy.get(community_results).then(($li) => {
            cy.wrap($li).contains(this.data.community_type3).click();
        })
        cy.get('[data-cy="academic_year"]').should('contain.text', this.data.academic_year1)
        cy.get('[data-cy="Reset Filters"]').click()
        cy.get('[data-cy="academic_year"]').contains('Previous Academic Year')
        })
    // Filter Options
    it('filter options', function() {
        const academic_year_selector = '#select2-id_academic_year-container',
        academic_year_results =  '#select2-id_academic_year-results',
        mission_container='#select2-id_mission-container',
        mission_results ='#select2-id_mission-results',
        community_containter = '#select2-id_community_type-container',
        community_results = '#select2-id_community_type-results',
        engagement_container = '#select2-id_engagement_type-container',
        engagement_results = '#select2-id_engagement_type-results',
        college_name_container ='#select2-id_college_name-container',
        college_name_results = '#select2-id_college_name-results',
        campus_partner_container = '#select2-id_campus_partner-container',
        campus_partner_results ='#select2-id_campus_partner-results',
        weitz_cec_part_container = '#select2-id_weitz_cec_part-container',
        weitz_cec_part_results ='#select2-id_weitz_cec_part-results'

        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="reports"]').next('[data-cy="reportsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).get('[data-cy="projectsreport"]').click()
        })
        cy.get('[data-cy="academic_year"]').contains('Previous Academic Year')
        cy.get(academic_year_selector).click()
        cy.get(academic_year_results).then(($li) => {
            cy.wrap($li).contains(this.data.academic_year4).click();
        })
        cy.get(mission_container).click()
        cy.get(mission_results).then(($li) => {
        cy.wrap($li).contains(this.data.focus_area4).click();
        })
        cy.get(engagement_container).click()
        cy.get(engagement_results).then(($li) => {
            cy.wrap($li).contains(this.data.engagement_type2).click()
        })
        cy.get(community_containter).click()
        cy.get(community_results).then(($li) => {
            cy.wrap($li).contains(this.data.community_type5).click();
        })
        cy.get(college_name_container).click()
        cy.get(college_name_results).then(($li) => {
            cy.wrap($li).contains(this.data.college_name1).click();
        })
        cy.get(campus_partner_container).click()
        cy.get(campus_partner_results).then(($li) => {
            cy.wrap($li).contains(this.data.select_all).click();
        })
        cy.get(weitz_cec_part_container).click()
        cy.get(weitz_cec_part_results).then(($li) => {
            cy.wrap($li).contains(this.data.cec_part4).click();
        })
    })

    it.only("Check Card View", function() 
    {
        const academic_year_selector = '#select2-id_academic_year-container',
        academic_year_results =  '#select2-id_academic_year-results',
        mission_container ='#select2-id_mission-container',
        mission_results ='#select2-id_mission-results',
        engagement_container = '#select2-id_engagement_type-container',
        engagement_results = '#select2-id_engagement_type-results',
        campus_partner_container = '#select2-id_campus_partner-container',
        campus_partner_results ='#select2-id_campus_partner-results'

        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="reports"]').next('[data-cy="reportsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).get('[data-cy="projectsreport"]').click()
        })
        cy.get(academic_year_selector).click()
        cy.get(academic_year_results).then(($li) => {
            cy.wrap($li).contains(this.data.academic_year1).click();
        })
        cy.get(mission_container).click()
        cy.get(mission_results).then(($li) => {
        cy.wrap($li).contains(this.data.focus_area4).click();
        })
        cy.get(engagement_container).click()
        cy.get(engagement_results).then(($li) => {
            cy.wrap($li).contains(this.data.select_all).click();
        })
        cy.get(campus_partner_container).click()
        cy.get(campus_partner_results).then(($li) => {
            cy.wrap($li).contains(this.data.campus_partner3).click();
        })
        //verify if theye are present in card structure
        cy.get('[data-cy="mission"]').contains(this.data.focus_area4).should("be.visible")
        cy.get('[data-cy="academic_year"]').contains(this.data.academic_year1).should("be.visible")
        cy.get('[data-cy="id_community_type"]').contains(this.data.select_all).should("be.visible")
        cy.get('[data-cy="id_campus_partner"]').contains(this.data.campus_partner3).should("be.visible")
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