beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })
    cy.visit(Cypress.env('baseUrl'))
})

describe('Admin Partner Registration Page', () => {
    it('visits the form', () => {
        cy.visit(Cypress.env('baseUrl'))
        })

    it('visits the site', function() {
        cy.visit(Cypress.env('baseUrl'))
    })

    it('Visit the login form', function() {
        cy.get('#login').click()
        cy.get('#email_input').type('unotest.super@gmail.com{enter}')
        cy.get('#password_input').type('superman02')
        cy.get('#loginForm').submit()
        cy.get('#partners').click()
    })
})