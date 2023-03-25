import user from "../../support/commands.js";
/// <reference types="cypress"/>
beforeEach(() => {
  cy.on('uncaught:exception', (err, runnable) => {
    if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('reading \'style\''))
    {
      return false
    }
  })
  cy.visit(Cypress.env('baseUrl'))

})

describe('Register campus partner - campus partner user', () => {
  beforeEach(function() {
    cy.fixture("datareports").then(function(data) {
      this.data = data
    cy.get('#login').click()
    cy.loginCampusUser(user)
    })
  })
  it('visits the form', function() {
    cy.url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
  })
  //Check navigation
  it('Check navigation for Partners : campus_partner_user', function() {
    cy.url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
    cy.get('#uno').click()
    cy.get('#partners').click()
  })

  it('Check ability to add Campus Partner', function() {
    cy.url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
    cy.get('#uno').click()
    cy.get('#partners').click()
    cy.get('#btn_reg_campus_partner').should('be.enabled').click()
    cy.get('.heading').should('contain', 'Campus Partner Registration')
    cy.get('#id_name').type(this.data.campus_partner_test1)
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li)=> {
      cy.wrap($li).contains(this.data.college_name1).click();
    })
    cy.get('.sw-btn-next').click()
    //  cy.get('#id_form-0-first_name').should('be.visble')
    cy.get('#id_form-0-first_name').type(this.data.campus_contact_firstname,{force:true})
    cy.get('#id_form-0-last_name').type(this.data.campus_contact_lastname,{force:true})
    cy.get('#id_form-0-email_id').type(this.data.campus_contact_email,{force:true})
    cy.get('.add-form-row').click({force:true})
    cy.get('#form-body > tr > :nth-child(1)').should('contain',this.data.campus_contact_firstname)
      .and('contain', this.data.campus_contact_lastname)
    cy.get('#form-body > tr > :nth-child(2)').should('contain',this.data.campus_contact_email)
    cy.get('#terms').click({force:true})
    cy.get('#submit').click({force:true})
    //  verify the backend
    cy.get('#accountinfo > .nav-link').click()
    cy.get('#logout').click()
    // login as admin
    cy.get('#login').click()
    cy.loginAdminUser(user)
    cy.visit(Cypress.env('baseUrl')+'admin/')
    cy.get('.model-campuspartner > th').click()
    cy.visit(Cypress.env('baseUrl')+'admin/partners/campuspartner/')
    cy.get('#searchbar').click().type(this.data.campus_partner_test1)
    cy.get('#changelist-search > div > [type="submit"]').click()
    cy.get('.field-name > a').should('contain',this.data.campus_partner_test1)
    //data clean up steps
    cy.get('.action-select').click()
    cy.get('select').select('Delete selected campus partners')
    cy.get('.button').click()
    cy.get('div > [type="submit"]').click()
    cy.get('.alert-success').should('contain', 'Successfully deleted 1 campus partner.')
    cy.get('#changelist-search > div > [type="submit"]').click()
    cy.get('.paginator').should('contain', '0 campus partners')
  })

  it('Check if a contact with non .edu email id is not possible', function() {
    cy.url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
    cy.get('#uno').click()
    cy.get('#partners').click()
    cy.get('#btn_reg_campus_partner').should('be.enabled').click()
    cy.get('.heading').should('contain', 'Campus Partner Registration')
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