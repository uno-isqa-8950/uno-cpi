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

describe('Analytic Charts Public user', () => {
    beforeEach(function () {
        cy.fixture("datareports").then(function (data) {
            this.data = data
        })
    })
    it('visits the form', function () {
        cy.visit(Cypress.env('baseUrl'))
    })
    //Check navigation to Engagement types charts
    it('Check navigation', function () {
        cy.contains('Analytics').click()
        cy.contains('Charts').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Types').click()
        })
    })
    it('Check if it is Engagement Types charts', function () {
        cy.contains('Analytics').click()
        cy.contains('Charts').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Types').click()
        })
        cy.get('.heading').should('contain.text', 'Engagement Types')
    })
    // Hide Filters
    it('Hide Filters', function () {
        cy.get('#analyticnav').click()
        cy.contains('Charts').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Types').click()
        })
        cy.get('#btn').should('have.class', 'btn btn-primary')
        cy.get('#btn').click()
        cy.get('.select2-selection__placeholder').should('not.be.visible')
        // check the filers are they visible
        cy.get('#btn').click()
        cy.get('#btn').should('have.class', 'btn btn-primary')
        cy.get('.select2-selection__placeholder').should('be.visible')
    })

    //Reset Filters
    it('Reset Filters', function () {
        cy.get('#analyticnav').click()
        cy.contains('Charts').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Types').click()
        })
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li) => {
            cy.wrap($li).contains(this.data.academic_year3).click();
        })
        cy.get('#select2-id_mission-container').click()
        cy.get('#select2-id_mission-results').then(($li) => {
            cy.wrap($li).contains(this.data.focus_area3).click();
        })
        cy.get('#select2-id_academic_year-container').should('contain.text', this.data.academic_year3)
        cy.get('input[value = "Reset Filters"]').click()
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
    })
    // Filter Options
    it ('filter options', function () {
        cy.get('#analyticnav').click()
        cy.contains('Charts').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Types').click()
        })
        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li) => {
            cy.wrap($li).contains(this.data.academic_year1).click();
        })
        cy.get('#select2-id_mission-container').click()
        cy.get('#select2-id_mission-results').then(($li) => {
            cy.wrap($li).contains(this.data.focus_area2).click();
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
    })

    //Verify charts x-axis, y-axis and x-axis labels
    it ('Charts x-axis, y-axis and x-axis labels', function () {
        cy.get('#analyticnav').click()
        cy.contains('Charts').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Types').click()
        })
        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li) => {
            cy.wrap($li).contains(this.data.academic_year1).click();
        })
        cy.get('#select2-id_mission-container').click()
        cy.get('#select2-id_mission-results').then(($li) => {
            cy.wrap($li).contains(this.data.focus_area2).click();
        })
        cy.get('#select2-id_community_type-container').click()
        cy.get('#select2-id_community_type-results').then(($li) => {
            cy.wrap($li).contains(this.data.select_all).click();
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
        cy.get('g[class="highcharts-axis highcharts-xaxis"]').contains('Engagement Types')
        cy.get('g[class="highcharts-axis highcharts-yaxis"]').contains('Projects/Partners')
        cy.get('div[class="highcharts-axis-labels highcharts-xaxis-labels"]').filter(':contains("Engaged Research")').should('exist')
        cy.get('div[class="highcharts-axis-labels highcharts-xaxis-labels"]').filter(':contains("Board Memberships")').should('exist')
        cy.get('div[class="highcharts-axis-labels highcharts-xaxis-labels"]').filter(':contains("Community-Based Learning")').should('exist')
        cy.get('div[class="highcharts-axis-labels highcharts-xaxis-labels"]').filter(':contains(" Knowledge and Resource Sharing")').should('exist')
        cy.get('div[class="highcharts-axis-labels highcharts-xaxis-labels"]').filter(':contains(" Service Learning")').should('exist')
        cy.get('div[class="highcharts-axis-labels highcharts-xaxis-labels"]').filter(':contains("Volunteering")').should('exist')
    })

    //verify legends in the chart
    it ('Chart legends', function () {
        cy.get('#analyticnav').click()
        cy.contains('Charts').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Types').click()
        })
        cy.get('.highcharts-series-0 > text').contains("Projects").should("be.visible")
        cy.get('.highcharts-series-0 > rect').should('have.attr', 'fill', 'teal')
        cy.get('.highcharts-series-1 > text').contains("Community Partners").should("be.visible")
        cy.get('.highcharts-series-1 > rect').should('have.attr', 'fill', 'turquoise')
        cy.get('.highcharts-series-2 > text').contains("Campus Partners").should("be.visible")
        cy.get('.highcharts-series-2 > rect').should('have.attr', 'fill', 'blue')
    })
})