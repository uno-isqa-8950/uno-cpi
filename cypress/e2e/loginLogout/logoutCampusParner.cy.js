import * as users from '/cypress.env.json'
describe('logout campus user front test', () => {
beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
      {
        return false
      }
    })
    cy.visit(Cypress.env('baseUrl'))
  })
  
    it('can submit a valid form', function(){
        const username = users.campusUser.username
        const password = users.campusUser.password
        const baseUrl = users.baseUrl
        const emailInput = '[data-cy="email"]',
            loginHref = '[data-cy="login"]',
            loginButtonId = '[data-cy="login"]',
            accountInfoId = '[data-cy="accountinfo"]',
            logoutButtonId = '[data-cy="campus-logout"]'
        cy.get(loginHref).click().get(emailInput).type(username).type('{enter}')
          .get("#password_input").type(password)
          .get(loginButtonId).eq(1).click()
          .url().should('be.equal', baseUrl+'myProjects/')
          .get(accountInfoId).should('exist').click()
          .get(logoutButtonId).should('exist').click()
          .url().should('be.equal', Cypress.env('baseUrl')+'logout/')
          .get('h3').contains('Logged Out')
    })
})

