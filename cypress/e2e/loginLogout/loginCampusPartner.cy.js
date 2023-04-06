import * as users from '/cypress.env.json'
describe('login campus user test', () => {
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
    const username = users.campusUser.username,
       password = users.campusUser.password,
       emailInput = '[data-cy="email"]',
       loginHref = '[data-cy="login"]',
       loginButtonId ='[data-cy="login"]',
       passwordInput = '[data-cy="password"]'
      cy.get(loginHref).click().get(emailInput).type(username).type('{enter}')
      cy.get(passwordInput).then(($input)=>{
        $input.val(password);
    })
      cy.get(loginButtonId).eq(1).click({force: true})
      cy.url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
  })

  it('cannnot submit an invalid form with wrong password', function(){
    const username = users.campusUser.username,
       password = users.campusUser.incorrectPassword,
       emailInput = '[data-cy="email"]',
       loginLink = '[data-cy="login"]',
       loginButtonId = '[data-cy="login"]',
       passwordInput = '[data-cy="password"]'
      cy.get(loginLink).click().get(emailInput).type(username).type('{enter}')
      cy.get(passwordInput).then(($input)=>{
        $input.val(password);
    })
      cy.get(loginButtonId).eq(1).click({force: true})
      cy.url().should('be.equal', Cypress.env('baseUrl')+'account/login-Page/')
      cy.get('.alert').contains('Email or Password is incorrect or contact system administration.').should('be.visible')
  })

  it('cannot login with non existing email id', function(){
    const username = users.campusUser.incorrectUsername,
      password = users.campusUser.password,
      emailInput = '[data-cy="email"]',
      loginHref = '[data-cy="login"]',
      loginButtonId ='[data-cy="login"]',
      passwordInput = '[data-cy="password"]'
      cy.get(loginHref).click().get(emailInput).type(username).type('{enter}')
      cy.get(passwordInput).then(($input)=>{
        $input.val(password);
    })
      cy.get(loginButtonId).eq(1).click()
      cy.url().should('be.equal', Cypress.env('baseUrl')+'account/login-Page/')
      cy.get('.alert').contains('Email or Password is incorrect or contact system administration.').should('be.visible')
  })
})