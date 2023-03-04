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
            cy.wrap($el).contains('Focus Area').click()
        })
    })
    it('Check if it is Focus Area Report', function() {
        cy.contains('Analytics').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get('.heading').should('contain.text', 'Focus Areas Report')
    })
    // Hide Filters and Reset Filters
    it('Hide Filters', function() {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get('#hidefilterbtn').should('have.class', 'btn btn-primary')
        cy.get('#hidefilterbtn').click()
        cy.get('.select2-selection__placeholder').should('not.be.visible')
        // check the filers are they visible
        cy.get('#hidefilterbtn').click()
        cy.get('#hidefilterbtn').should('have.class', 'btn btn-primary')
        cy.get('.select2-selection__placeholder').should('be.visible')
        })
    it('Reset Filters', function() {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li) => {
            cy.wrap($li).contains(this.data.academic_year3).click();
        })
        cy.get('#select2-id_engagement_type-container').click()
        cy.get('#select2-id_engagement_type-results').then(($li) => {
            cy.wrap($li).contains(this.data.engagement_type3).click();
        })
        cy.get('#select2-id_academic_year-container').should('contain.text', this.data.academic_year3)
        cy.get('#resetfilterbtn').click()
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
        })
    // Filter Options    
    it('filter options', function() {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li) => {
            cy.wrap($li).contains(this.data.academic_year1).click();
        })
        cy.get('#select2-id_engagement_type-container').click()
        cy.get('#select2-id_engagement_type-results').then(($li) => {
            cy.wrap($li).contains(this.data.engagement_type1).click();
        })
        cy.get('#select2-id_community_type-container').click()
        cy.get('#select2-id_community_type-results').then(($li) => {
            cy.wrap($li).contains(this.data.community_type1).click();
        })
        cy.get('#select2-id_college_name-container').click()
        cy.get('#select2-id_college_name-results').then(($li) => {
            cy.wrap($li).contains(this.data.select_all).click();
        })
        cy.get('#select2-id_campus_partner-container').click()
        cy.get('#select2-id_campus_partner-results').then(($li) => {
            cy.wrap($li).contains(this.data.select_all).click();
        })
        cy.get('#select2-id_weitz_cec_part-container').click()
        cy.get('#select2-id_weitz_cec_part-results').then(($li) => {
            cy.wrap($li).contains(this.data.cec_part1).click();
        })
        cy.get('.buttons-csv').click()
        cy.get('.buttons-pdf').click()
    })
    // Check 7 focus area is listed
    it('Check if report contains all Focus Area Report', function () {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get(':nth-child(1) > .sorting_1').contains(this.data.focus_area1)
        cy.get(':nth-child(2) > .sorting_1').contains(this.data.focus_area2)
        cy.get(':nth-child(3) > .sorting_1').contains(this.data.focus_area3)
        cy.get(':nth-child(4) > .sorting_1').contains(this.data.focus_area4)
        cy.get(':nth-child(5) > .sorting_1').contains(this.data.focus_area5)
        cy.get(':nth-child(6) > .sorting_1').contains(this.data.focus_area6)
        cy.get(':nth-child(7) > .sorting_1').contains(this.data.focus_area7)
    })
    it("Check conectivity to Community Partners report", function() {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get(':nth-child(1) > :nth-child(2) > .class1').invoke('attr', 'target', '_self').click()
        cy.get('.heading').should('contain.text', 'Community Partners Report')
        cy.url().should('contain', 'https://uno-cpi-dev.herokuapp.com/community-public-report')
    })
    it("Check conectivity to Projects report", function() {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get(':nth-child(1) > :nth-child(3) > .class1').invoke('attr', 'target', '_self').click()
        cy.get('.heading').should('contain.text', 'Projects Report')
        cy.url().should('contain', 'https://uno-cpi-dev.herokuapp.com/projectspublicreport/')
    })
    it("Check tooltip text for 7 focus areas", function() {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        //focus area 1
        cy.get(':nth-child(1) > .sorting_1 > span > .fa').trigger('mouseover').invoke('show')
        cy.contains('Projects and organizations that support the need for the improvement through Arts, Culture and Humanities.')
        //focus area 2
        cy.get(':nth-child(2) > .sorting_1 > span > .fa').trigger('mouseover').invoke('show')
        cy.contains('Projects and organizations who address the causes, consequences, and solutions to poverty, with a special focus on meeting the economic needs of those affected by poverty.')
        //focus area 3
        cy.get(':nth-child(3) > .sorting_1 > span > .fa').trigger('mouseover').invoke('show')
        cy.contains('Projects and organizations who support educational and learning needs, as well as inequalities within the community.')
        //focus area 4
        cy.get(':nth-child(4) > .sorting_1 > span > .fa').trigger('mouseover').invoke('show')
        cy.contains('Projects and organizations that support the need for the improvement of our environment through sustainability and awareness.')
        //focus area 5
        cy.get(':nth-child(5) > .sorting_1 > span > .fa').trigger('mouseover').invoke('show')
        cy.contains('Projects and organizations that support and bring awareness to the health and wellness needs of everyone, including specific health concerns of the ill, the aged, those with disabilities, and others in need while advocating for healthy lifestyles.')
        //focus area 6
        cy.get(':nth-child(6) > .sorting_1 > span > .fa').trigger('mouseover').invoke('show')
        cy.contains('Projects and organizations that support international needs and concerns while devoting efforts to both local populations (refugees, immigrants, exchange students, etc.) and those engaged in international travel.')
        //focus area 7
        cy.get(':nth-child(7) > .sorting_1 > span > .fa').trigger('mouseover').invoke('show')
        cy.contains('Projects and organizations that support inequality and corrupt social structures while devoting special efforts to meet the social needs of underprivileged populations.')  
    })
})