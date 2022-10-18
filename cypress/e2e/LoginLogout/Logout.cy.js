
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
        cy.visit('http://127.0.0.1:8000/')
    })

    it('visits the login form', () => {
        cy.get('#login').click()
    })

    it('requires email', () => {
        cy.get('#email_input').type('shwetap1002@gmail.com{enter}')
    })

    it('requires password name', () => {
        cy.get('#password_input').type('CEPITesting123')
    })

    it('can submit a valid form', () => {
        cy.get('#loginForm').submit()
    })

    it('visits the logout form', () => {
        cy.wait(200)
        cy.get('#accountinfo').click()
        cy.wait(200)
        cy.get("#logout").click()
    })
})