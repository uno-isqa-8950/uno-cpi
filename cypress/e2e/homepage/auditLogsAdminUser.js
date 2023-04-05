/// <reference types="cypress"/>
import user from "../../support/commands";
import * as data from "../../fixtures/datareports.json";

beforeEach(() => {
  cy.on('uncaught:exception', (err, runnable) => {
    if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('reading \'style\''))
    {
      return false
    }
  })
  cy.visit(Cypress.env('baseUrl'))
})

describe('Audit Logs for admin user', () => {
    beforeEach(function () {
        cy.fixture("datareports").then(function (data) {
            this.data = data
        cy.get('#login').click()
        cy.loginCampusUser(user)
        })
    })
    //Check navigation to Engagement types charts
    it('validate audit logs exist', function () {
        cy.get('[data-cy="administrator"]').should('exist').click()
        cy.get('[data-cy="auditlogs"]').next('[data-cy="dropdown-administrator"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Audit Logs').click()
        })
    })
})
