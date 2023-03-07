beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })
})

describe('Login to the app', () => {
    it('visits the form', () => {
        cy.visit(Cypress.env('http://127.0.0.1:8000/'))
    })

    it('visits the login form', () => {
        cy.get('#login').click()
    })

    it('requires email', () => {
        cy.get('#email_input').type('unotest.super@gmail.com{enter}')
    })

    it('requires password name', () => {
        cy.get('#password_input').type('superman02')
    })

    it('can submit a valid form', () => {
        cy.get('#loginForm').submit()
    })
    it('Register Community Partner', () => {
        cy.get('#btn_reg_community_partner').click()
    })
})