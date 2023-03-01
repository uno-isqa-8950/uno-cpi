beforeEach(() => {
  cy.on('uncaught:exception', (err, runnable) => {
    if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
    {
      return false
    }
  })
  cy.visit(Cypress.env('baseUrl'))
})

describe('Login to the app', () => {
  beforeEach(function () {
    cy.fixture("user").then(function (data) {
      this.data = data
    })
    it('can submit a valid form', () => {
      const emailInput = 'input[id="email_input"]',
          loginHref = `a[href="/account/login-Page/"]`
      cy.get(loginHref).click().get(emailInput).type(this.data.email)
      cy.get('#password_input').type(this.data.password)
      cy.get('#loginForm').submit()
      cy.url().should('be.equal', 'http://127.0.0.1:8000/')
    })

    it('cannnot submit an invalid form with wrong password', () => {
      const emailInput = 'input[id="email_input"]',
          loginId = `a[href="/account/login-Page/"]`
      cy.get(loginId).click().get(emailInput).type('shireen54@gmail.com{enter}')
      cy.get('#password_input').type('Testme123#')
      cy.get('#loginForm').submit()
      cy.url().should('be.equal', 'http://127.0.0.1:8000/account/login-Page/')
    })

   it('cannnot submit an invalid form with unregisterd email id', () => {
      const emailInput = 'input[id="email_input"]',
          loginId = `a[href="/account/login-Page/"]`
      cy.get(loginId).click().get(emailInput).type('shireen541@gmail.com{enter}')
      cy.get('#password_input').type('Testme123#')
      cy.get('#loginForm').submit()
      cy.url().should('be.equal', 'http://127.0.0.1:8000/account/login-Page/')
    })
  })
})