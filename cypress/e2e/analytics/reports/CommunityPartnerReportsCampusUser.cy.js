import user from "../../../support/commands";
beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('reading \'style\''))
        {
            return false
        }
    })
    cy.visit(Cypress.env('baseUrl'))
})


describe('Navigate to Resources Menu to view external links ', () => {
    beforeEach(function() {
      cy.fixture("datareports").then(function(data) {
      this.data = data
      cy.get('#login').click()
      cy.loginCampusUser(user)
      })
    })

    it('Open-Community-partner-reports-Filters', () => {
        cy.get('[data-cy=analytics]').click()
        cy.get('[data-cy=communitypublicreport]').click()
        cy.get("select2-id_academic_year-container")
        .click()
        cy.get(".select2-search__field")
        .type("All")
        .type('{enter}')
        cy.get("select2-id_academic_year-container")
        .should('have.text','All')

        cy.get("#select2-id_community_type-container")
        .click()
        cy.get(".select2-search__field")
        .type("All")
        .type('{enter}')
        cy.get("#select2-id_community_type-container")
        .should('have.text','All')

        cy.get("#select2-id_weitz_cec_part-container")
        .click()
        cy.get(".select2-search__field")
        .type("All")
        .type('{enter}')
        cy.get("#select2-id_weitz_cec_part-container")
        .should('have.text','All')

        cy.get("#select2-id_college_name-container")
        .click()
        cy.get(".select2-search__field")
        .type("All")
        .type('{enter}')
        cy.get("#select2-id_college_name-container")
        .should('have.text','All')

        cy.get("a[href='/projectspublicreport/?proj_id_list=1535']")
        .invoke("removeAttr", "target")
        .click()
        cy.get("a[href='/projectspublicreport/?proj_id_list=1535']").should('always.returned')
        
    })
    


  })