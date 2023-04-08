beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
      {
        return false
      }
    })
    cy.visit(Cypress.env('baseUrl'))
    });

describe('Navigate to Resources Menu to view external links ', () => {
    it('Handling-community-engagement', () => {
        cy
        .get('#resourcesnav')
        .click()
        //invoke function is called to force the URL to open in same window
        cy.get(".dropdown-item[href='https://www.unomaha.edu/engagement/roadmap.php']").should('exist')

        
    })

    it('Handling-community-compass', () => {
        cy.get("#resourcesnav")
        .click()
        //exist feature is used if the external URL locator is present in the get function 
        cy.get(".dropdown-item[href='http://www.communityplatform.us/communityplatform/nam']")
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

    it('Handling-Service-learning-academy', () => {
        cy.get('#resourcesnav').click()
        //invoke function is called to force the URL to open in same window
        cy.get(".dropdown-item[href='https://www.unomaha.edu/service-learning-academy/']").should('exist')

        })
    })
