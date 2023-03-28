/// <reference types="cypress"/>
import user from "../../support/commands";

beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('reading \'style\''))
        {
            return false
        }
    })
    cy.visit(Cypress.env('baseUrl'))
})
describe('Home Page Administrator', () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
        this.data = data
        cy.get('#login').click()
        cy.loginAdminUser(user)
        })
    })
    //Check base url is loading the Home Page of CEPI application
    it('visits the form', function() {
        cy.visit({
            url: Cypress.env('baseUrl'),
            method: 'GET',
          })
    })
    //check link in NAV bar - uno logo
    it('check navbar link', function() {
        const analytics = '[data-cy=analytics]'
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Areas').click()
        })
        cy.get('[data-cy=himg]').click()
        cy.url().should('be.equal', Cypress.env('baseUrl'))
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.contains('Reports').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Types').click()
        })
        cy.get('[data-cy=cpi]').click()
        cy.url().should('be.equal', Cypress.env('baseUrl'))
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.contains('Reports').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Projects').click()
        })
        cy.get('[data-cy=uno]').click()
        cy.url().should('be.equal', Cypress.env('baseUrl'))
        })
    //check link in footer - uno logo
    it ('check footer uno logo', function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.contains('Reports').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get('[data-cy=fimg]').click()
        cy.url().should('be.equal', Cypress.env('baseUrl'))
    })
    //Verify menus in Navigation bar
    it('Navigation bar options', function() {
        cy.get('[data-cy=navbar]').should('contain.text', 'Maps')
            .and('contain.text', 'Analytics')
            .and('contain.text', 'Partners')
            .and('contain.text', 'Resources')
    //        .and('contain.text', 'Login')
    })
     it('Navigation bar options for Maps', function() {
        cy.get('[data-cy=maps]').click()
        cy.contains('Community Partners')
        cy.contains('Legislative Districts')
        cy.contains('City Districts')
        cy.contains('Community Partner Types')
        cy.contains('Projects')
        })
     it('Navigation bar options for Projects', function() {
        cy.get('[data-cy="projectsnav"]').click()
        cy.contains('All Projects')
        cy.contains('My Projects')
        cy.contains('Create Project')
        cy.contains('My Drafts')
        })
    it('Navigation bar options for Analytics', function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area')
            cy.wrap($el).contains('Engagement Types')
            cy.wrap($el).contains('Community Partners')
            cy.wrap($el).contains('Projects')
        })
        cy.get('[data-cy=charts]').next('[data-cy=chartsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area')
            cy.wrap($el).contains('Engagement Types')
        })
    })
    it('Navigation bar options for Partners, Login', function() {
        cy.get('[data-cy=partners]').click()
        cy.url().should('be.equal', Cypress.env('baseUrl')+'partners/')
        cy.get('[data-cy=uno]').click()
        // User Login link
        cy.get('[data-cy="accountinfo"]').click()
        cy.contains('Logout')
    })
    it('Navigation bar options for Resources', function() {
        cy.get('[data-cy=resources]').click()
        cy.contains('Office of Engagement')
        cy.contains('Community Compass')
        cy.contains('About CEPI')
        cy.contains('Share Omaha')
        cy.contains('Community Engagement Roadmap')
        })
    it('Navigation bar options for Administrator', function() {
        cy.get('[data-cy="administrator"]').click()
        cy.contains('Admin View')
        cy.contains('CMS')
        cy.contains('Organization')
        cy.contains('Audit Logs')
        cy.contains('Campus Partner User Registration')
        })
    //Verify links in homepage section
    it('Verify links in homepage section', function() {
        cy.get('[data-cy=himg]').click()
        cy.get('.initialcontent').should('contain', 'REGISTER A NEW CAMPUS PARTNER')
        .and('contain', 'VIEW THE COMMUNITY PARTNER LEGISLATIVE MAP')
        .and('contain', 'VIEW PARTNER AND PROJECT ANALYTICS BY FOCUS AREA')
        cy.get('a[href="https://www.unomaha.edu/engagement/index.php"]').should ('contain', 'COMMUNITY ENGAGEMENT').click().wait(3000)
            cy.visit('https://www.unomaha.edu/engagement/index.php')
            cy.origin('https://www.unomaha.edu/engagement/index.php', () => {
                cy.get('h1').should('have.text','Engagement')
            })
        cy.visit(Cypress.env('baseUrl'))
        //cy.get('a[href="https://www.unomaha.edu/academic-affairs/academic-community-engagement/impact/cepi.php"]').should('contain', 'CEPI INFORMATION AND GUIDELINES')
       // cy.url().should('be.equal', 'https://www.unomaha.edu/office-of-engagement/_files/campus-user-guidelines.pdf')
//        cy.origin('.col > :nth-child(1) > p > a').contains('REGISTER A NEW CAMPUS PARTNER').click()
//        cy.url().should('be.equal','https://cepi.unomaha.edu/partners/register-Campus-Partner/')
//        cy.url().should('be.equal', Cypress.env('baseUrl')+'partners/register-Campus-Partner/')
        })
    //Verify homepage footer
    it('Verify homepage footer', function() {
        cy.get('[data-cy=terms]').invoke('removeAttr','target').should('contain','Terms and Conditions')
        cy.get('[data-cy=contactus]').should('contain','Contact Us')
    })
})

