// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })
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
