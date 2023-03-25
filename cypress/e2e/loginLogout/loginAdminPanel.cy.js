beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
      {
        return false
      }
    })
    cy.visit(Cypress.env('baseUrl'))
  })
  
  describe('login admin panel test', () => {
    beforeEach(function() {
      cy.fixture("users").then(function(data) {
        this.data = data
      })
      cy.fixture("datareports").then(function(datas) {
        this.datas = datas
      })
    })
    it('can submit a valid form', function(){
        const emailInput = 'input[id="id_username"]',
          passwordInput = 'input[id="id_password"]',
          loginButton = 'input[value="Log in"]'
        cy.visit(this.datas.baseUrl+'admin/')
          .get(emailInput).type(this.data.adminUser.username).type('{enter}')
          .get(passwordInput).type(this.data.adminUser.password)
          .get(loginButton).click()
          .url().should('be.equal', this.datas.baseUrl+'admin/')
    })
});