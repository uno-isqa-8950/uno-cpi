
beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined'))
        {
            return false
        }
    })
})

describe('Logout of the app', () => {
    it('visits the form', () => {
        cy.visit(Cypress.env('baseUrl'))
    })

    it('visits the login form', () => {
        cy.get('#login').click()
    })

    it('requires email', () => {
        cy.get('#email_input').type('campususer123@gmail.com{enter}')
    })

    it('requires password name', () => {
        cy.get('#password_input').type('CEPITesting123')
    })

    it('can submit a valid form', () => {
        cy.get('#loginForm').submit()
    })

    it('visits the logout form', () => {
        cy.get('#accountinfo').click()
        cy.get("#logout").click()
    })
})