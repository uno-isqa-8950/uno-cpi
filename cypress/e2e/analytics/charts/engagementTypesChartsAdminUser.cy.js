/// <reference types="cypress"/>
import user from "../../../support/commands";

beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('reading \'style\''))
        {
            return false
        }
    })
    cy.visit(Cypress.env('baseUrl'))
})

describe('Engagement Types Chart Campus user', () => {
    beforeEach(function () {
        cy.fixture("datareports").then(function (data) {
            this.data = data
        cy.get('#login').click()
        cy.loginAdminUser(user)
        })
    })
    //Check navigation to Engagement types charts
    it('Check navigation', function () {
        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="charts"]').next('[data-cy="chartsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Types').click()
        })
    })
    it('Check if it is Engagement Types charts', function () {
        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="charts"]').next('[data-cy="chartsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Types').click()
        })
        cy.get('[data-cy="engagement types"]').should('contain.text', 'Engagement Types')
    })
    // Hide Filters
    it('Hide Filters', function () {
        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="charts"]').next('[data-cy="chartsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Types').click()
        })
        cy.get('[data-cy="hide filters"]').should('have.value', 'Hide Filters')
        cy.get('[data-cy="hide filters"]').click()
        cy.get('.select2-selection__placeholder').should('not.be.visible')
        // check the filers are they visible
        cy.get('[data-cy="hide filters"]').click()
        cy.get('[data-cy="hide filters"]').should('have.value', 'Hide Filters')
        cy.get('.select2-selection__placeholder').should('be.visible')
    })

    //Reset Filters
    it('Reset Filters', function () {
        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="charts"]').next('[data-cy="chartsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Types').click()
        })
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
        cy.get('[data-cy="academic_year"]').select(this.data.academic_year1,{force:true})
        cy.get('#select2-id_academic_year-container').should('have.text' ,this.data.academic_year1)
        cy.get('[data-cy="mission"]').select(this.data.focus_area3,{force:true})
        cy.get('#select2-id_academic_year-container').should('contain.text', this.data.academic_year1)
        cy.get('[data-cy="Reset filter"]').click()
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
    })
    // Check selected filter options
    it('filter options', function () {
        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="charts"]').next('[data-cy="chartsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Types').click()
        })
        cy.get('[data-cy="academic_year"]').select(this.data.academic_year1,{force:true})
        cy.get('#select2-id_academic_year-container').should('have.text' ,this.data.academic_year1)
        cy.get('[data-cy="mission"]').select(this.data.focus_area3,{force:true})
        cy.get('#select2-id_mission-container').should('have.text' ,this.data.focus_area3)
        cy.get('[data-cy="community_type"]').select(this.data.community_type1,{force:true})
        cy.get('#select2-id_community_type-container').should('have.text' ,this.data.community_type1)
        cy.get('[data-cy="college_name"]').select(this.data.college_name1,{force:true})
        cy.get('#select2-id_college_name-container').should('have.text' ,this.data.college_name1)
        cy.get('[data-cy="campus_partner"]').select(this.data.campus_partner3,{force:true})
        cy.get('#select2-id_campus_partner-container').should('have.text' ,this.data.campus_partner3)
        cy.get('[data-cy="weitz_cec_part"]').select(this.data.cec_part1,{force:true})
        cy.get('#select2-id_weitz_cec_part-container').should('have.text' ,this.data.cec_part1)
    })

    //Verify charts x-axis, y-axis and x-axis labels
    it('Charts x-axis, y-axis and x-axis labels', function () {
        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="charts"]').next('[data-cy="chartsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Types').click()
        })
        cy.get('[data-cy="academic_year"]').select(this.data.academic_year1,{force:true})
        cy.get('[data-cy="mission"]').select(this.data.focus_area3,{force:true})
        cy.get('[data-cy="community_type"]').select(this.data.community_type1,{force:true})
        cy.get('[data-cy="college_name"]').select(this.data.college_name1,{force:true})
        cy.get('[data-cy="campus_partner"]').select(this.data.campus_partner3,{force:true})
        cy.get('[data-cy="weitz_cec_part"]').select(this.data.cec_part1,{force:true})
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
        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="charts"]').next('[data-cy="chartsdropdown"]').then($el => {
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