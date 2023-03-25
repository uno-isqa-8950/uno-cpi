beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
      {
        return false
      }
    })
    cy.visit(Cypress.env('baseUrl'))
  })
  
  describe('login campus partner test', () => {
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
            loginButtonId ='#btnLogin'
        cy.get(loginHref).click().get(emailInput).type(this.data.campusUser.username).type('{enter}')
        cy.get("#password_input").type(this.data.campusUser.password);
        cy.get(loginButtonId).click()
        cy.url().should('be.equal', this.datas.baseUrl+'myProjects/')
    })

    it('cannnot submit an invalid form with wrong password', function(){
        const emailInput = 'input[id="email_input"]',
            loginId = `a[href="/account/login-Page/"]`,
            loginButtonId ='#btnLogin'
        cy.get(loginId).click().get(emailInput).type(this.data.campusUser.username).type('{enter}')
        cy.get('#password_input').type(this.data.campusUser.incorrectPassword)
        cy.get(loginButtonId).click()
        cy.url().should('be.equal', this.datas.baseUrl+'account/login-Page/')
        cy.get('.alert').contains('Email or Password is incorrect or contact system administration.').should('be.visible')
    })

    it('cannot login with non existing email id', function(){
        const emailInput = 'input[id="email_input"]',
            loginHref = `a[href="/account/login-Page/"]`,
            loginButtonId ='#btnLogin'
        cy.get(loginHref).click().get(emailInput).type(this.data.campusUser.incorrectUsername).type('{enter}')
        cy.get("#password_input").type(this.data.campusUser.password);
        cy.get(loginButtonId).click()
        cy.url().should('be.equal', this.datas.baseUrl+'account/login-Page/')
        cy.get('.alert').contains('Email or Password is incorrect or contact system administration.').should('be.visible')
    })
})

