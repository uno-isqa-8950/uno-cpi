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
        cy.visit('http://127.0.0.1:8000/')
    })

    it('visits the login form', () => {
        cy.get('#resourcesnav').click()
        cy.wait(700)
    })
})
    /*it('Resources', () => {
        //cy.get('#loginForm').submit()
        cy.get('#resourcesnav').click()
        //cy.contains('Community Engagement Roadmap').next('.dropdown-menu').then($el => {
            //cy.wrap($el).invoke('show')
            //cy.wrap($el).contains('Project and Partner Trends').click()
        })*/
