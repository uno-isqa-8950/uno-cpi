import * as users from '/cypress.env.json'
describe('login admin panel test', () => {
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
      const username = users.adminUser.username,
        password = users.adminUser.password,
        emailInput = 'input[id="id_username"]',
        passwordInput = 'input[id="id_password"]',
        loginButton = 'input[value="Log in"]'
      cy.visit(Cypress.env('baseUrl')+'admin/')
          .get(emailInput).type(username).type('{enter}')
          .get(passwordInput).type(password)
          .get(loginButton).click()
          .url().should('be.equal', Cypress.env('baseUrl')+'admin/')
    })
  })
