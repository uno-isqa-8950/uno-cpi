/*beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })
})

describe("Logging in to the CEPI Website", () => {
    it("Can login", () => {
        cy.visit(Cypress.env('admin'))
        cy.get("input[name='username']").type(Cypress.env('username')).should("have.value", Cypress.env('username'))
        cy.get("input[name='password']").type(Cypress.env('password')).should("have.value", Cypress.env('password'))
        cy.get("form").submit().should('be.visible')
    })
})
*/


beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })

    cy.visit(Cypress.env('baseUrl'))
})


describe("Admin login", () => {
    const adminHref = 'a[href="/account/login-Page/"]',
        emailInput = "input[name='email']",
        passwordInput = "input[name='password']"

    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
        })
    })

    it("Successful login", () => {
        cy.visit(Cypress.env('baseUrl'))
        cy.get(adminHref).click()
        cy.get(emailInput)
            .type(Cypress.env('admin_email'))
            .should("have.value", Cypress.env('admin_email'))
        cy.get(passwordInput)
            .type(Cypress.env('admin_password'), { force: true })
            .should("have.value", Cypress.env('admin_password'))
        cy.get("form").submit().should('be.visible')
        cy.visit(Cypress.env('baseUrl'))
    })

})
