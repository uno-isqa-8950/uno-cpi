beforeEach(() => {
  cy.on('uncaught:exception', (err, runnable) => {
    if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
    {
      return false
    }
  })
  cy.visit(Cypress.env('baseUrl'))
})

describe('Logout from the app', () => {
  it('can logout from the app', () => {
    const accountInfoId = 'li[id="accountinfo"]',
      emailInput = 'input[id="email_input"]',
      loginHref = `a[href="/account/login-Page/"]`,
      logoutHref = `a[href="/logout/"]`

    cy.get(loginHref).click().get(emailInput).type('shireen54@gmail.com{enter}')
    cy.get('#password_input').type('Testme12#')
    cy.get('#loginForm').submit()
    cy.url().should('be.equal', 'http://127.0.0.1:8000/')
    cy.get(accountInfoId).click().wait(2000).get(logoutHref).click()
    cy.url().should('be.equal', 'http://127.0.0.1:8000/logout/')
  })

})