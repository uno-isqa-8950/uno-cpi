import user from "../../support/commands.js";

beforeEach(() => {
  cy.on('uncaught:exception', (err, runnable) => {
    if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
    {
      return false
    }
  })
  cy.visit(Cypress.env('baseUrl'))
})


describe ('Register campus partner', () => {
  beforeEach(function () {
    cy.fixture("datareports").then(function (data) {
      this.data = data
    })
  })
  // Register the campus partner
  it('visit partners page and register campus partner', function () {
    cy.get('[data-cy="partners"]').should ("be.visible").click()
    cy.get('[data-cy="campus partners"]').contains("Campus Partners")
    cy.get('[data-cy="btn_reg_campus_partner"]').click()
    cy.get('[data-cy="heading"]').contains("Campus Partner Registration")
    const campus_partnerName = 'input[id="id_name"]'
    cy.get(campus_partnerName).type(this.data.campus_partner7)
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li)=> {
      cy.wrap($li).contains(this.data.college_name1).click();
    })
    cy.get('.sw-btn-next').click()
    cy.get('#id_form-0-first_name').type(this.data.campuspartner1_firstname,{force:true})
    cy.get('#id_form-0-last_name').type(this.data.campuspartner1_lastname,{force:true})
    cy.get('#id_form-0-email_id').type(this.data.campuspartner1_emailID,{force:true})
    cy.get('[data-cy="add-form-row"]').click();
    cy.get('[data-cy="termsdiv"]').click();
    cy.get('[data-cy="submit"]').click();
    cy.get('[data-cy="heading"]').should('have.text', "Thank You")
    cy.get('[data-cy="text"]').contains("Your organization is successfully registered as a campus partner.")
  })
  //verify added campus partner is available in admin panel
  it('visit admin and verify added campus partner', function () {
    cy.get('#login').click()
      .loginAdminUser(user)
    cy.visit(Cypress.env('baseUrl')+'admin/')
    cy.get('.model-campuspartner > th').click()
    cy.visit(Cypress.env('baseUrl')+'admin/partners/campuspartner/')
    cy.get('#searchbar').click().type(this.data.campus_partner7)
    cy.get('#changelist-search > div > [type="submit"]').click()
    cy.get('.field-name > a').contains(this.data.campus_partner7)
  })

  //check cancel in campus partner details.
  it('visit campus partner details and cancel typed data', function() {
    cy.get('[data-cy="partners"]').should("be.visible").click()
    cy.get('[data-cy="btn_reg_campus_partner"]').click()
    const campus_partnerName = 'input[id="id_name"]'
    cy.get(campus_partnerName).type(this.data.campus_partner8)
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li) => {
      cy.wrap($li).contains(this.data.college_name1).click();
    })
    cy.get('[data-cy="cancel"]').click()
    cy.url().should('be.equal',Cypress.env('baseUrl')+'partners/')
  })

  //Check cancel in contact information page
  it('visit contact information and cancel typed data', function() {
    cy.get('[data-cy="partners"]').should("be.visible").click()
    cy.get('[data-cy="btn_reg_campus_partner"]').click()
    const campus_partnerName = 'input[id="id_name"]'
    cy.get(campus_partnerName).type(this.data.campus_partner8,{force:true})
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li) => {
      cy.wrap($li).contains(this.data.college_name1).click()
    })
    cy.get('.sw-btn-next').click()
    cy.get('#id_form-0-first_name').type(this.data.campuspartner2_firstname)
    cy.get('#id_form-0-last_name').type(this.data.campuspartner2_lastname)
    cy.get('#id_form-0-email_id').type(this.data.campuspartner2_emailID)
    cy.get('.add-form-row').click();
    cy.get('[data-cy="cancel"]').click()
    cy.url().should('be.equal',Cypress.env('baseUrl')+'partners/')
  })

  //Check previous button in Contact Information page
  it('visit contact information page and return to campus partner page', function() {
    cy.get('[data-cy="partners"]').should("be.visible").click()
    cy.get('[data-cy="btn_reg_campus_partner"]').click()
    const campus_partnerName = 'input[id="id_name"]'
    cy.get(campus_partnerName).type(this.data.campus_partner8)
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li) => {
      cy.wrap($li).contains(this.data.college_name1).click()
    })
    cy.get('.sw-btn-next').click()
    cy.get('#id_form-0-first_name').type(this.data.campuspartner2_firstname)
    cy.get('#id_form-0-last_name').type(this.data.campuspartner2_lastname)
    cy.get('.sw-btn-prev').click()
    cy.url().should('be.equal',Cypress.env('baseUrl')+'partners/register-Campus-Partner/?')
    cy.get('.sw-btn-next').click().wait(3000)
    cy.get('#id_form-0-first_name').should('have.value', this.data.campuspartner2_firstname)
    cy.get('#id_form-0-last_name').should('have.value', this.data.campuspartner2_lastname)

  })

  //Check submit button is not exist in campus partner details page
  it('verify submit button is not exist in campus partner details page', function() {
    cy.get('[data-cy="partners"]').should("be.visible").click()
    cy.get('[data-cy="btn_reg_campus_partner"]').click()
    const campus_partnerName = 'input[id="id_name"]'
    cy.get(campus_partnerName).type(this.data.campus_partner8)
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li) => {
      cy.wrap($li).contains(this.data.college_name1).click()
    })
    cy.get('[data-cy="submit"]').should('not.visible')
  })

  //Check unchecked terms & conditions
  it('verify unchecked terms & conditions in contact information page', function () {
    cy.get('[data-cy="partners"]').should("be.visible").click()
    cy.get('[data-cy="btn_reg_campus_partner"]').click()
    const campus_partnerName = 'input[id="id_name"]'
    cy.get(campus_partnerName).type(this.data.campus_partner8)
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li)=> {
      cy.wrap($li).contains(this.data.college_name1).click();
    })
    cy.get('.sw-btn-next').click()
    cy.get('#id_form-0-first_name').type(this.data.campuspartner2_firstname)
    cy.get('#id_form-0-last_name').type(this.data.campuspartner2_lastname)
    cy.get('#id_form-0-email_id').type(this.data.campuspartner2_emailID)
    cy.get('[data-cy="add-form-row"]').click()
    //cy.get('#terms').click();
    cy.get('[data-cy="submit"]').click()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('Please Accept the terms and conditions before submitting');
    })
  })
  //Check delete symbol in contact information page
  it('verify delete symbol in contact information page', function () {
    cy.get('[data-cy="partners"]').should("be.visible").click()
    cy.get('[data-cy="btn_reg_campus_partner"]').click()
    const campus_partnerName = 'input[id="id_name"]'
    cy.get(campus_partnerName).type(this.data.campus_partner8)
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li) => {
      cy.wrap($li).contains(this.data.college_name1).click();
    })
    cy.get('.sw-btn-next').click()
    cy.get('#id_form-0-first_name').type(this.data.campuspartner2_firstname)
    cy.get('#id_form-0-last_name').type(this.data.campuspartner2_lastname)
    cy.get('#id_form-0-email_id').type(this.data.campuspartner2_emailID)
    cy.get('[data-cy="add-form-row"]').click()
    cy.get("i[data-id=1]").click()
    cy.get('[data-cy="form-body"]').should('not.visible')

  })
  //Check alert message is displaying while submitting without adding contact information
  it('verify alert message when no contact information is added', function () {
    cy.get('[data-cy="partners"]').should("be.visible").click()
    cy.get('[data-cy="btn_reg_campus_partner"]').click()
    const campus_partnerName = 'input[id="id_name"]'
    cy.get(campus_partnerName).type(this.data.campus_partner8)
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li) => {
      cy.wrap($li).contains(this.data.college_name1).click();
    })
    cy.get('.sw-btn-next').click()
    cy.get('#id_form-0-first_name').type(this.data.campuspartner2_firstname)
    cy.get('#id_form-0-last_name').type(this.data.campuspartner2_lastname)
    cy.get('#id_form-0-email_id').type(this.data.campuspartner2_emailID)
    cy.get('[data-cy="add-form-row"]').click()
    cy.get('[align="center"]').click()
    cy.get('[data-cy="termsdiv"]').click()
    cy.get('[data-cy="submit"]').click()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('You need to add at least one contact');
    })
  })
  //Check only .edu email address can be added
  it('verify only .edu email address can be added', function () {
    cy.get('[data-cy="partners"]').should("be.visible").click()
    cy.get('[data-cy="btn_reg_campus_partner"]').click()
    const campus_partnerName = 'input[id="id_name"]'
    cy.get(campus_partnerName).type(this.data.campus_partner8)
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li) => {
      cy.wrap($li).contains(this.data.college_name1).click();
    })
    cy.get('.sw-btn-next').click()
    cy.get('#id_form-0-first_name').type(this.data.campuspartner2_firstname)
    cy.get('#id_form-0-last_name').type(this.data.campuspartner2_lastname)
    cy.get('#id_form-0-email_id').type(this.data.campuspartner_gmail)
    cy.get('[data-cy="add-form-row"]').click()
    cy.on('window:alert', (txt) => {
      expect(txt).to.contains('Please use your campus email (.edu) for the registration of a Campus Partner');
    })
  })
  //Check first name is a mandatory field
  it('Check firstname is a mandatory field', function () {
    cy.get('[data-cy="partners"]').should("be.visible").click()
    cy.get('[data-cy="btn_reg_campus_partner"]').click()
    const campus_partnerName = 'input[id="id_name"]'
    cy.get(campus_partnerName).type(this.data.campus_partner8)
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li) => {
      cy.wrap($li).contains(this.data.college_name1).click();
    })
    cy.get('.sw-btn-next').click()
    cy.get('[data-cy="add-form-row"]').click()
    cy.on('window:alert', (txt) => {
      expect(txt).to.contains('Provide First Name');
    })
  })
  //Check last name is a mandatory field
  it('Check lastname is a mandatory field', function () {
    cy.get('#partners').should("be.visible").click()
    cy.get('#btn_reg_campus_partner').click()
    const campus_partnerName = 'input[id="id_name"]'
    cy.get(campus_partnerName).type(this.data.campus_partner8)
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li) => {
      cy.wrap($li).contains(this.data.college_name1).click();
    })
    cy.get('.sw-btn-next').click()
    cy.get('#id_form-0-first_name').type(this.data.campuspartner2_firstname)
    cy.get('[data-cy="add-form-row"]').click()
    cy.on('window:alert', (txt) => {
      expect(txt).to.contains('Provide Last Name');
    })
  })
  //Check email id is a mandatory field
  it('Check email id is a mandatory field', function () {
    cy.get('#partners').should("be.visible").click()
    cy.get('#btn_reg_campus_partner').click()
    const campus_partnerName = 'input[id="id_name"]'
    cy.get(campus_partnerName).type(this.data.campus_partner8)
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li) => {
      cy.wrap($li).contains(this.data.college_name1).click();
    })
    cy.get('.sw-btn-next').click()
    cy.get('#id_form-0-first_name').type(this.data.campuspartner2_firstname)
    cy.get('#id_form-0-last_name').type(this.data.campuspartner2_lastname)
    cy.get('[data-cy="add-form-row"]').click()
    cy.on('window:alert', (txt) => {
      expect(txt).to.contains('Provide Email Address');
    })
  })
  //Check existing contact information can be provided
  it('verify existing contact information can be provided', function () {
    cy.get('#partners').should("be.visible").click()
    cy.get('#btn_reg_campus_partner').click()
    const campus_partnerName = 'input[id="id_name"]'
    cy.get(campus_partnerName).type(this.data.campus_partner8)
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li)=> {
      cy.wrap($li).contains(this.data.college_name1).click();
    })
    cy.get('.sw-btn-next').click()
    cy.get('#id_form-0-first_name').type(this.data.campuspartner1_firstname,{force:true})
    cy.get('#id_form-0-last_name').type(this.data.campuspartner1_lastname,{force:true})
    cy.get('#id_form-0-email_id').type(this.data.campuspartner1_emailID,{force:true})
    cy.get('[data-cy="add-form-row"]').click();
    cy.get('[data-cy="termsdiv"]').click();
    cy.get('[data-cy="submit"]').click();
  })
  //Check existing campus partner cannot be added
  it('verify existing campus partner cannot be added', function () {
    cy.get('#partners').should("be.visible").click()
    cy.get('#btn_reg_campus_partner').click()
    const campus_partnerName = 'input[id="id_name"]'
    cy.get(campus_partnerName).type(this.data.campus_partner8)
    cy.get('#select2-id_college_name-container').click()
    cy.on('window:alert', (txt) => {
      expect(txt).to.contains('A Campus Partner with this name already exists');
    })
  })
  //Check duplicate contact information cannot be added
  it('verify duplicate contact information cannot be added', function () {
    cy.get('#partners').should("be.visible").click()
    cy.get('#btn_reg_campus_partner').click()
    const campus_partnerName = 'input[id="id_name"]'
    cy.get(campus_partnerName).type(this.data.campus_partner9)
    cy.get('#select2-id_college_name-container').click()
    cy.get('#select2-id_college_name-results').then(($li)=> {
      cy.wrap($li).contains(this.data.college_name1).click();
    })
    cy.get('.sw-btn-next').click()
    cy.get('#id_form-0-first_name').type(this.data.campuspartner1_firstname,{force:true})
    cy.get('#id_form-0-last_name').type(this.data.campuspartner1_lastname,{force:true})
    cy.get('#id_form-0-email_id').type(this.data.campuspartner1_emailID,{force:true})
    cy.get('.add-form-row').click()
    cy.get('#id_form-1-first_name').type(this.data.campuspartner1_firstname,{force:true})
    cy.get('#id_form-1-last_name').type(this.data.campuspartner1_lastname,{force:true})
    cy.get('#id_form-1-email_id').type(this.data.campuspartner1_emailID,{force:true})
    cy.get('.add-form-row').click()
    cy.get('[data-cy="termsdiv"]').click();
    cy.get('[data-cy="submit"]').click();
    cy.on('window:alert', (txt) => {
      expect(txt).to.contains('Duplicate contacts cannot be added');
    })
  })

  // Data clean up script
  
  it ('data cleanup', function() {
    cy.get('#login').click()
      .loginAdminUser(user)
    cy.visit(Cypress.env('baseUrl')+'admin/')
    cy.get('.model-campuspartner > th').click()
    cy.visit(Cypress.env('baseUrl')+'admin/partners/campuspartner/')
    cy.get('#searchbar').click().type(this.data.campus_partner7)
    cy.get('#changelist-search > div > [type="submit"]').click()
    cy.get('.field-name > a').contains(this.data.campus_partner7).click()
    cy.get('.deletelink-box > a').click()
    cy.get('input[type=submit]').click()
    cy.get('#changelist-search > div > [type="submit"]').click()
    cy.get('#searchbar').clear()
    cy.get('#searchbar').click().type(this.data.campus_partner8)
    cy.get('#changelist-search > div > [type="submit"]').click()
    cy.get('.field-name > a').contains(this.data.campus_partner8).click()
    cy.get('.deletelink-box > a').click()
    cy.get('input[type=submit]').click()
    cy.get('#changelist-search > div > [type="submit"]').click()
    cy.get('#searchbar').clear()
    cy.get('#searchbar').click().type(this.data.campus_partner9)
    cy.get('#changelist-search > div > [type="submit"]').click()
    cy.get('.field-name > a').contains(this.data.campus_partner9).click()
    cy.get('.deletelink-box > a').click()
    cy.get('input[type=submit]').click()
    cy.get('#changelist-search > div > [type="submit"]').click()
    //cy.get('.breadcrumbs > [href="/admin/"]').click()
    //cy.get('.model-contact > th > a').click()
    //cy.get('#searchbar').type(this.data.campuspartner1_emailID)
    //cy.get('#changelist-search > div > [type="submit"]')
    //cy.get('.field-email_id').contains(this.data.campuspartner1_emailID)
    //cy.get('.field-first_name > a').click()
    //cy.get('.deletelink').click()
    //cy.get('div > [type="submit"]').click()
    //cy.get('#searchbar').click().type(this.data.campuspartner1_emailID)
    //cy.get('#changelist-search > div > [type="submit"]').click()
    //cy.get('.paginator').contains('0 contacts')
  })
})
