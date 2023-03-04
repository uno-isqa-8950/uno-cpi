beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })
    cy.visit(Cypress.env('baseUrl'))
})

describe('Charts Focus Area', () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
        })
    })

    it('visits the site', function() {
        cy.visit(Cypress.env('baseUrl'))
    })

    it('Analytic Charts Focus Area User', function() {
        cy.get('#analyticnav').click().should('be.visible')
        cy.contains('Charts').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show').should('be.visible')
            cy.wrap($el).contains('Focus Areas').click()
        })

        cy.get("input[value='Hide Filters']").should('not.be.disabled')
        cy.get("input[value='Reset Filters']").should('not.be.disabled')

        cy.get('#select2-id_academicyear-container').click()
        cy.get('#select2-id_academicyear-results').then(($li) => {
            cy.wrap($li).contains(this.data.academic_year2).should('have.text', this.data.academic_year2).click()
        })

        cy.get('#select2-id_engagement_type-container').click()
        cy.get('#select2-id_engagement_type-results').then(($li) => {
            cy.wrap($li).contains(this.data.engagement_type3).should('have.text', this.data.engagement_type3).click()
        })

        cy.get('#select2-id_community_type-container').click()
        cy.get('#select2-id_community_type-results').then(($li) => {
            cy.wrap($li).contains(this.data.community_type1).should('have.text', this.data.community_type1).click()
        })

        cy.get('#select2-id_college_name-container').click()
        cy.get('#select2-id_college_name-results').then(($li) => {
            cy.wrap($li).contains(this.data.college_name3).should('have.text', this.data.college_name3).click()
        })

        cy.get('#select2-id_campus_partner-container').click()
        cy.get('#select2-id_campus_partner-results').then(($li) => {
            cy.wrap($li).contains(this.data.community_type6).should('have.text', this.data.community_type6).click()
        })

        cy.get('#select2-id_weitz_cec_part-container').click()
        cy.get('#select2-id_weitz_cec_part-results').then(($li) => {
            cy.wrap($li).contains(this.data.cec_part1).should('have.text', this.data.cec_part1).click()
        })

        cy.get('.highcharts-root').should('be.visible').and(chart => {
            expect(chart.height()).to.be.greaterThan(200)
        })

        cy.get('.highcharts-xaxis').contains('Focus Areas')
        cy.get('.highcharts-yaxis').contains('Projects/Community Partners')
        cy.get('.highcharts-xaxis-labels').filter(':contains("Arts, Culture and Humanities")').should('exist')
        cy.get('.highcharts-xaxis-labels').filter(':contains("Economic Impact")').should('exist')
        cy.get('.highcharts-xaxis-labels').filter(':contains("Educational Support")').should('exist')
        cy.get('.highcharts-xaxis-labels').filter(':contains("Environmental Stewardship")').should('exist')
        cy.get('.highcharts-xaxis-labels').filter(':contains("Health and Wellness")').should('exist')
        cy.get('.highcharts-xaxis-labels').filter(':contains("International Service")').should('exist')
        cy.get('.highcharts-xaxis-labels').filter(':contains("Social Justice")').should('exist')
    })

    it('Chart legends', function () {
        cy.get('#analyticnav').click()
        cy.contains('Charts').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Areas').click()
        })
        cy.get('.highcharts-series-0 > text').contains("Projects").should("be.visible")
        cy.get('.highcharts-series-0 > rect').should('have.attr', 'fill', 'turquoise')
        cy.get('.highcharts-series-1 > text').contains("Community Partners").should("be.visible")
        cy.get('.highcharts-series-1 > rect').should('have.attr', 'fill', 'teal')
    })


})
