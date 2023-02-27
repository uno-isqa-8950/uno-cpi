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

describe ('Visits all focus areas in home page', () => {

    //verify all projects listed in this report belong to economic impact focus area.
    it ('visits economic impact focus area', () => {
        cy.get('h3').contains("ECONOMIC IMPACT").should("be.visible").click()
        cy.url().should("include", "/projectspublicreport/?academic_year=All&mission=3&community_type=&college_name=&campus_partner=&engagement_type=")
        cy.get('div[class="card-toptext"]').contains("Economic Impact").should("be.visible")
    })

    //verify all projects listed in this report belong to educational support focus area.
    it ('visits educational support focus area', () => {
        cy.get('h3').contains("EDUCATIONAL SUPPORT").should("be.visible").click()
        cy.url().should("include", "/projectspublicreport/?academic_year=All&mission=1&community_type=&college_name=&campus_partner=&engagement_type=")
        cy.get('.btn-secondary').contains("2").click()
        cy.get('div[class="card-toptext"]').contains("Educational Support").should("be.visible")
    })

    //verify all projects listed in this report belong to international service focus area.
    it ('visits international service focus area', () => {
        cy.get('h3').contains("INTERNATIONAL SERVICE").should("be.visible").click()
        cy.url().should("include", "/projectspublicreport/?academic_year=All&mission=5&community_type=&college_name=&campus_partner=&engagement_type=")
        cy.get('.btn-secondary').contains("3").click()
        cy.get('div[class="card-toptext"]').contains("International Service").should("be.visible")
    })

    //verify all projects listed in this report belong to social justice focus area.
    it ('visits social justice focus area', () => {
        cy.get('h3').contains("SOCIAL JUSTICE").should("be.visible").click()
        cy.url().should("include", "/projectspublicreport/?academic_year=All&mission=4&community_type=&college_name=&campus_partner=&engagement_type=")
        cy.get('.btn-secondary').contains("3").click()
        cy.get('.btn-secondary').contains("4").click()
        cy.get('div[class="card-toptext"]').contains("Social Justice").should("be.visible")
    })

    //verify all projects listed in this report belong to environmental stewardship focus area.
    it ('visits environmental stewardship focus area', () => {
        cy.get('h3').contains("ENVIRONMENTAL STEWARDSHIP").should("be.visible").click()
        cy.url().should("include", "/projectspublicreport/?academic_year=All&mission=6&community_type=&college_name=&campus_partner=&engagement_type=")
        cy.get('.btn-secondary').contains("3").click()
        cy.get('.btn-secondary').contains("5").click()
        cy.get('div[class="card-toptext"]').contains("Environmental Stewardship").should("be.visible")
    })

    //verify all projects listed in this report belong to health and wellness focus area.
    it ('visits health and wellness focus area', () => {
        cy.get('h3').contains("HEALTH AND WELLNESS").should("be.visible").click()
        cy.url().should("include", "/projectspublicreport/?academic_year=All&mission=2&community_type=&college_name=&campus_partner=&engagement_type=")
        cy.get('.btn-secondary').contains("3").click()
        cy.get('.btn-secondary').contains("5").click()
        cy.get('div[class="card-toptext"]').contains("Health and Wellness").should("be.visible")
    })

    //verify all projects listed in this report belong to arts, culture, and humanities focus area.
    it ('visits arts,culture & humanities focus area', () => {
        cy.get('h3').contains("ARTS, CULTURE & HUMANITIES").should("be.visible").click()
        cy.url().should("include", "/projectspublicreport/?academic_year=All&mission=8&community_type=&college_name=&campus_partner=&engagement_type=")
        cy.get('.btn-secondary').contains("3").click()
        cy.get('.btn-secondary').contains("4").click()
        cy.get('div[class="card-toptext"]').contains("Arts, Culture and Humanities").should("be.visible")
    })
})


