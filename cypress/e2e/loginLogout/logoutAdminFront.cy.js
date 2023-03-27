beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
      {
        return false
      }
    })
    cy.visit(Cypress.env('baseUrl'))
  })
  
  describe('login admin front test', () => {
    beforeEach(function() {
      cy.fixture("users").then(function(data) {
        this.data = data
      })
      cy.fixture("datareports").then(function(datas) {
        this.datas = datas
      })
    })
    it('can submit a valid form', function(){
        const emailInput = 'input[id="email_input"]',
            loginHref = `a[href="/account/login-Page/"]`,
            loginButtonId = '#btnLogin',
            accountInfoId = '#accountinfo',
            logoutButtonId = `a[id="logout"]`
        cy.get(loginHref).click().get(emailInput).type(this.data.adminUser.username).type('{enter}')
          .get("#password_input").type(this.data.adminUser.password)
          .get(loginButtonId).click()
          .url().should('be.equal', this.datas.baseUrl)
          .get(accountInfoId).should('exist').click()
          .get(logoutButtonId).should('exist').click()
          .url().should('be.equal', Cypress.env('baseUrl')+'logout/')
          .get('h3').contains('Logged Out')
    })
})