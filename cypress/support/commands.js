import * as data from '../fixtures/datareports.json'
import * as users from '../fixtures/users.json'


Cypress.Commands.add("loginCampusUser", (user) => {
  //adding a new command named login
  const username = users.campusUser.username
  const password = users.campusUser.password
  cy.visit(Cypress.env('baseUrl'))
  cy.get('#login').click()
  cy.get("#email_input").type(username).type('{enter}')
  cy.get("#password_input").type(password);
  cy.get("#btnLogin").click();
});

Cypress.Commands.add("loginAdminUser", (user) => {
  //adding a new command named login
  const username = users.adminUser.username
  const password = users.adminUser.password
  cy.visit(Cypress.env('baseUrl'))
  cy.get('#login').click()
  cy.get("#email_input").type(username).type('{enter}')
  cy.get("#password_input").type(password);
  cy.get("#btnLogin").click();
});

Cypress.Commands.add("checkProjectName", () => {
  cy.get('#projectsnav').contains('Projects').click()
  cy.contains('Create Project').click()
  cy.get('.heading').should('contain.text', 'Create Project')
  cy.get('#select2-academicYear-container > .select2-selection__placeholder').contains(data.All_Academic_Years)
  cy.get('#select2-academicYear-container').click()
  cy.get('#select2-academicYear-results').then(($li)=> {
    cy.wrap($li).contains(data.academic_year4).click();
  })
  cy.get('#select2-communityPartner-container').click()
  cy.get('#select2-communityPartner-results').then(($li)=>{
    cy.wrap($li).contains(data.community_partner1).click();
  })
  cy.get('#select2-campuspartner-container').click()
  cy.get('#select2-campuspartner-results').then(($li)=> {
    cy.wrap($li).contains(data.campus_partner3).click();
  })
});

Cypress.Commands.add("projectInformation", () => {
  cy.get('#select2-id_engagement_type-container').click()
  cy.get('#select2-id_engagement_type-results').then(($li)=> {
    cy.wrap($li).contains(data.engagement_type3).click();
  })
  cy.get('#id_description').type(data._comment7)
  cy.get('#projectdurationnav').click()
  cy.get('#select2-id_semester-container').click()
  cy.get('#select2-id_semester-results').then(($li)=> {
    cy.wrap($li).contains(data.semester1).click();
  })
  cy.get('#select2-id_academic_year-container').click()
  cy.get('#select2-id_academic_year-results').then(($li)=> {
    cy.wrap($li).contains(data.academic_year1).click();
  })
});

Cypress.Commands.add("partnersInformation", () => {
  cy.get('#campuspartnerinfonav').click()
  cy.get('#id_campus-0-campus_partner').select(data.campus_partner3)
  cy.get('.add-campus-row').click()
  cy.get('.sw-btn-next').click()
});

