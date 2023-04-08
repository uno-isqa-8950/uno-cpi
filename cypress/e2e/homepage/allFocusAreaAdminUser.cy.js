import user from "../../support/commands.js";
describe('All focus area cards for admin user', () => {
beforeEach(() => {
    cy.on('uncaught:exception', (err) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
      {
        return false
      }
    })
    cy.fixture("datareports").then(function(data) {
      this.data = data
    })
    cy.loginAdminUser(user)  // Admin User is logged in before the test begins
    cy.visit(Cypress.env('baseUrl'))
  })
    //verify all projects listed in this report belong to economic impact focus area.
    it('visits economic impact focus area', () => {
        cy.get('[data-cy="economic impact"]').contains("ECONOMIC IMPACT").should("be.visible").click()
        cy.url().should("include", "/projectsprivatereport/?academic_year=All&mission=3&community_type=&college_name=&campus_partner=&engagement_type=")
        cy.get('[data-cy="toptext"]').contains("Economic Impact").should("be.visible")
    })

    //verify all projects listed in this report belong to educational support focus area.
    it('visits educational support focus area', () => {
        cy.get('[data-cy="educational support"]').contains("EDUCATIONAL SUPPORT").should("be.visible").click()
        cy.url().should("include", "/projectsprivatereport/?academic_year=All&mission=1&community_type=&college_name=&campus_partner=&engagement_type=")
        //cy.get('.btn-secondary').contains("2").click()
        cy.get('[data-cy="toptext"]').contains("Educational Support").should("be.visible")
    })

    //verify all projects listed in this report belong to international service focus area.
    it('visits international service focus area', () => {
        cy.get('[data-cy="international service"]').contains("INTERNATIONAL SERVICE").should("be.visible").click()
        cy.url().should("include", "/projectsprivatereport/?academic_year=All&mission=5&community_type=&college_name=&campus_partner=&engagement_type=")
        //cy.get('.btn-secondary').contains("3").click()
        cy.get('[data-cy="toptext"]').contains("International Service").should("be.visible")
    })

    //verify all projects listed in this report belong to social justice focus area.
    it('visits social justice focus area', () => {
        cy.get('[data-cy="social justice"]').contains("SOCIAL JUSTICE").should("be.visible").click()
        cy.url().should("include", "/projectsprivatereport/?academic_year=All&mission=4&community_type=&college_name=&campus_partner=&engagement_type=")
        //cy.get('.btn-secondary').contains("3").click()
        //cy.get('.btn-secondary').contains("4").click()
        cy.get('[data-cy="toptext"]').contains("Social Justice").should("be.visible")
    })

    //verify all projects listed in this report belong to environmental stewardship focus area.
    it('visits environmental stewardship focus area', () => {
        cy.get('[data-cy="environmental stewardship"]').contains("ENVIRONMENTAL STEWARDSHIP").should("be.visible").click()
        cy.url().should("include", "/projectsprivatereport/?academic_year=All&mission=6&community_type=&college_name=&campus_partner=&engagement_type=")
        //cy.get('.btn-secondary').contains("3").click()
        //cy.get('.btn-secondary').contains("5").click()
        cy.get('[data-cy="toptext"]').contains("Environmental Stewardship").should("be.visible")
    })

    //verify all projects listed in this report belong to health and wellness focus area.
    it('visits health and wellness focus area', () => {
        cy.get('[data-cy="health"]').contains("HEALTH AND WELLNESS").should("be.visible").click()
        cy.url().should("include", "/projectsprivatereport/?academic_year=All&mission=2&community_type=&college_name=&campus_partner=&engagement_type=")
        //cy.get('.btn-secondary').contains("3").click()
        //cy.get('.btn-secondary').contains("5").click()
        cy.get('[data-cy="toptext"]').contains("Health and Wellness").should("be.visible")
    })

    //verify all projects listed in this report belong to arts, culture, and humanities focus area.
    it ('visits arts,culture & humanities focus area', () => {
        cy.get('[data-cy="arts"]').contains("ARTS, CULTURE & HUMANITIES").should("be.visible").click()
        cy.url().should("include", "/projectsprivatereport/?academic_year=All&mission=8&community_type=&college_name=&campus_partner=&engagement_type=")
        //cy.get('.btn-secondary').contains("3").click()
        //cy.get('.btn-secondary').contains("4").click()
        cy.get('[data-cy="toptext"]').contains("Arts, Culture and Humanities").should("be.visible")
    })
})


