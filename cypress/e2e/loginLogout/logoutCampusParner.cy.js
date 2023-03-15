beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
      if(err.message.includes('is not a function') 
      || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
      {
        return false
      }
    })
    cy.visit(Cypress.env('baseUrl'))
  })
  
  describe('logout campus partner test', () => {
    beforeEach(function() {
      cy.fixture("users").then(function(data) {
        this.data = data
      })
    })
    it('can submit a valid form', function(){
        const emailInput = 'input[id="email_input"]',
            loginHref = `a[href="/account/login-Page/"]`,
            loginButtonId = '#btnLogin',
            accountInfoId = '#accountinfo',
            logoutButtonId = `a[id="logout"]`
        cy.get(loginHref).click().get(emailInput).type(this.data.campusUser.username).type('{enter}')
          .get("#password_input").type(this.data.campusUser.password)
          .get(loginButtonId).click()
          .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/myProjects/')
          .get(accountInfoId).should('exist').click()
          .get(logoutButtonId).should('exist').click()
          .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/logout/')
          .get('h3').contains('Logged Out')
    })
})

