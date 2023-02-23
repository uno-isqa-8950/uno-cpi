beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })
})

describe('Projects', () => {
    it('visits the form', () => {
        cy.visit(Cypress.env('baseUrl'))
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

    it('Office Of Engagement', () => {
        cy.get('#loginForm').submit()
        cy.get("#resourcesnav").click()
        cy.contains('Community Engagement Roadmap').click()
    })
})
