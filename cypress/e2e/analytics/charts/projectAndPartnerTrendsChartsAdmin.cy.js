import user from "../../../support/commands";

beforeEach(() => {
  cy.on('uncaught:exception', (err, runnable) => {
    if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
    {
      return false
    }
  })
  cy.visit(Cypress.env('baseUrl'))
})

describe('Charts Project and Partner Trend', () => {
  beforeEach(function() {
    cy.fixture("datareports").then(function(data) {
      this.data = data
      cy.get('#login').click()
      cy.loginAdminUser(user)
    })
  })

  it('visits the site', function() {
    cy.visit(Cypress.env('baseUrl'))
  })

  it('Analytic Charts Project and Partner Trends', function() {
    cy.get("[data-cy='analytics']").click().should('be.visible')
    cy.contains('Charts').next("[data-cy='chartsdropdown']").then($el => {
      cy.wrap($el).invoke('show').should('be.visible')
      cy.wrap($el).contains('Project and Partner Trend').click()
    })

    cy.get("[data-cy='Hide Filters']").should('not.be.disabled')
    cy.get("[data-cy='Reset Filters']").should('not.be.disabled')

    cy.get('#select2-id_mission-container').click()
    cy.get('#select2-id_mission-results').then(($li) => {
      cy.wrap($li).contains(this.data.focus_area1).should('have.text', this.data.focus_area1).click()
    })

    cy.get('#select2-id_community_type-container').click()
    cy.get('#select2-id_community_type-results').then(($li) => {
      cy.wrap($li).contains(this.data.community_type6).should('have.text', this.data.community_type6).click()
    })

    cy.get('#select2-id_engagement_type-container').click()
    cy.get('#select2-id_engagement_type-results').then(($li) => {
      cy.wrap($li).contains(this.data.engagement_type3).should('have.text', this.data.engagement_type3).click()
    })

    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li) => {
      cy.wrap($li).contains(this.data.college_name4).should('have.text', this.data.college_name4).click()
    })

    cy.get('#select2-id_campus_partner-container').click()
    cy.get('#select2-id_campus_partner-results').then(($li) => {
      cy.wrap($li).contains(this.data.campus_partner3).should('have.text', this.data.campus_partner3).click()
    })

    cy.get('#select2-id_weitz_cec_part-container').click()
    cy.get('#select2-id_weitz_cec_part-results').then(($li) => {
      cy.wrap($li).contains(this.data.cec_part1).should('have.text', this.data.cec_part1).click()
    })

    cy.get('.highcharts-root').should('be.visible').and(chart => {
      expect(chart.height()).to.be.greaterThan(200)
    })

    cy.get('.highcharts-yaxis').contains('Projects/Partners')
    cy.get('.highcharts-xaxis').contains('Academic Years')
  })

  it('Chart legends', function () {
    cy.get("[data-cy='analytics']").click()
    cy.contains('Charts').next('.dropdown-menu').then($el => {
      cy.wrap($el).invoke('show')
      cy.wrap($el).contains('Project and Partner Trends').click()
    })
    cy.get('.highcharts-series-0 > text').contains("Projects").should("be.visible")
    cy.get('.highcharts-series-1 > text').contains("Community Partners").should("be.visible")
    cy.get('.highcharts-series-2 > text').contains("Campus Partners").should("be.visible")
  })


})