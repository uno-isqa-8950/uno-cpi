import user from "../../support/commands.js";
describe ('Register campus partner as admin', () => {
  beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
      {
        return false
      }
    })
    cy.fixture("datareports").then(function(data) {
      this.data = data
    })
    cy.loginAdminUser(user) // Admin User is logged in before the test begins
    cy.visit(Cypress.env('baseUrl'))
  })

  // Register the campus partner as admin
  it ('visit partners page, log in as admin, and register campus partner', function () {
    cy.get('[data-cy="partners"]').should ("be.visible").click()
    cy.get('#btn_reg_campus_partner').click()
    cy.get('[data-cy="heading"]').should('contain', 'Campus Partner Registration')
    cy.get('#id_name').type(this.data.campus_partner4)
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li)=> {
      cy.wrap($li).contains(this.data.college_name1).click();
    })
    cy.get('.sw-btn-next').click()
    cy.get('#id_form-0-first_name').type(this.data.campuspartner1_firstname,{force:true})
    cy.get('#id_form-0-last_name').type(this.data.campuspartner1_lastname,{force:true})
    cy.get('#id_form-0-email_id').type(this.data.campuspartner1_emailID,{force:true})
    cy.get('.add-form-row').click({force:true});
    cy.get('[data-cy="form-body"] > tr > :nth-child(1)').should('contain',this.data.campuspartner1_firstname)
      .and('contain', this.data.campuspartner1_lastname)
    cy.get('[data-cy="form-body"] > tr > :nth-child(2)').should('contain',this.data.campuspartner1_emailID)
    cy.get('[data-cy="termsdiv"]').click({force: true});
    cy.get('[data-cy="submit"]').click();
    cy.visit(Cypress.env('baseUrl')+'admin/')
    cy.get('.model-campuspartner > th').click()
    cy.visit(Cypress.env('baseUrl')+'admin/partners/campuspartner/')
    cy.get('#searchbar').click().type(this.data.campus_partner4)
    cy.get('#changelist-search > div > [type="submit"]').click()
    cy.get('.field-name > a').should('contain',this.data.campus_partner4)
    //data clean up steps
    cy.get('.action-select').click()
    cy.get('select').select('Delete selected campus partners')
    cy.get('.button').click()
    cy.get('div > [type="submit"]').click()
    cy.get('.alert-success').should('contain', 'Successfully deleted 1 campus partner.')
    cy.get('#changelist-search > div > [type="submit"]').click()
    cy.get('.paginator').should('contain', '0 campus partners')
  })

  //Check only .edu email address can be added
  it('Check if a contact with non .edu email id is not possible', function() {
    //cy.url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
    cy.get('[data-cy="partners"]').click()
    cy.get('[data-cy="btn_reg_campus_partner"]').should('be.enabled').click()
    cy.get('[data-cy="heading"]').should('contain', 'Campus Partner Registration')
    const campus_partnerName = 'input[id="id_name"]'
    cy.get(campus_partnerName).type(this.data.campus_partner_test1+'new')
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li) => {
      cy.wrap($li).contains(this.data.college_name1).click();
    })
    cy.get('.sw-btn-next').click()
    cy.get('#id_form-0-first_name').type(this.data.campus_contact_firstname)
    cy.get('#id_form-0-last_name').type(this.data.campus_contact_lastname)
    cy.get('#id_form-0-email_id').type(this.data.campus_contact_email,{force:true})
    cy.get('.add-form-row').click()
    cy.on('window:alert', (txt) => {
      expect(txt).to.contains('Please use your campus email (.edu) for the registration of a Campus Partner.');
    })
  })

})