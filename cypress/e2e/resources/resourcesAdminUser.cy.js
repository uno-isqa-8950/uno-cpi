import user from "../../support/commands.js";

beforeEach(() => {
    cy.on('uncaught:exception', (err) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
      {
        return false
      }
    })
    cy.visit(Cypress.env('baseUrl'))

  })
  
  describe('Testing Resource URLs ', () => {
    beforeEach(function() {
      cy.fixture("datareports").then(function(data) {
        this.data = data
    cy.get('#login').click()
      .loginAdminUser(user)  // this is to login as admin user in each iteration
      })
    })
     
    it('Handling-office-of-engagement', () => {
        cy
        .get('#resourcesnav')
        .click()
        //invoke function is called to force the URL to open in same window
        cy.get(".dropdown-item[href='https://www.unomaha.edu/office-of-engagement/index.php']")
        .invoke("removeAttr", "target")
        .click()
        
        //Cy.origin is used to allow cross domain page handling in cypress
        cy.origin('https://www.unomaha.edu', () => {
            
        //HTML text validation is used to confirm if the external url is correct
            cy.get("h4").should("contain","Office of Engagement");

            })

        
    })

    it('Handling-community-compass', () => {
        cy.get('#resourcesnav')
        .click()
        //exist feature is used if the external URL locator is present in the get function 
        cy.get(".dropdown-item[href='http://www.communityplatform.us/communityplatform/nam']")
        .should('exist')

    })

    it('Handling-About-CEPI', () => {
        cy.get('#resourcesnav')
        .click()
        //exist feature is used if the external URL locator is present in the get function 
        cy.get(".dropdown-item[href='https://unocepi.s3.amazonaws.com/documents/CEPI_Definitions_V1.pdf']")
        .should('exist')
        
        
        
    })

    it('Handling-share-omaha', () => {
        cy.get('#resourcesnav').click()
        cy.get(".dropdown-item[href='https://shareomaha.org/']").invoke("removeAttr","target").click()
        //Cy.origin is used to allow cross domain page handling in cypress
    
        cy.origin('https://shareomaha.org', () => {
            
        cy.url().should("include","shareomaha.org");

        })
    })

    it('Handling-Community-Engagement', () => {
        cy.get('#resourcesnav').click()
        //invoke function is called to force the URL to open in same window
        cy.get(".dropdown-item[href='https://www.unomaha.edu/engagement/roadmap.php']").invoke("removeAttr","target").click()
    
        //Cy.origin is used to allow cross domain page handling in cypress

        cy.origin('https://www.unomaha.edu', () => {
            
        cy.get("h1")
        .should("contain","Community Engagement Roadmap");

        })
    })



  })