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

describe('Home Page Public user', () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
        this.data = data
        })
    })
    //Check base url is loading the Home Page of CEPI application
    it('visits the form', function() {
        cy.visit({
            url: this.data.CEPI_site,
            method: 'GET',
          })
    })
    //check link in NAV bar - uno logo
    it('check navbar link', function() {
        cy.contains('Analytics').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get('.himg').click()
        cy.url().should('be.equal', this.data.CEPI_site)
        cy.contains('Analytics').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Types').click()
        })
        cy.get('#cpi').click()
        cy.url().should('be.equal', this.data.CEPI_site)
        cy.contains('Analytics').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Projects').click()
        })
        cy.get('#uno').click()
        cy.url().should('be.equal', this.data.CEPI_site)
        })
    //check link in footer - uno logo
    it ('check footer uno logo', function() {
        cy.contains('Analytics').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get('.fimg').click()
        cy.url().should('be.equal', this.data.CEPI_site)
    })
    //Verify menus in Navigation bar
    it('Navigation bar options', function() {
        cy.get('.navbar').should('contain.text', 'Maps')
            .and('contain.text', 'Analytics')
            .and('contain.text', 'Partners')
            .and('contain.text', 'Resources')
            .and('contain.text', 'Login')
    })
     it('Navigation bar options for Maps', function() {
        cy.get(':nth-child(1) > .nav-link').click()
        cy.contains('Community Partners')
        cy.contains('Legislative Districts')
        cy.contains('City Districts')
        cy.contains('Community Partner Types')
        cy.contains('Projects')
        })
    it('Navigation bar options for Analytics', function() {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area')
            cy.wrap($el).contains('Engagement Types')
            cy.wrap($el).contains('Community Partners')
            cy.wrap($el).contains('Projects')
        })
        cy.contains('Charts').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area')
            cy.wrap($el).contains('Engagement Types')
        })

    })
    it('Navigation bar options for Partners, Login', function() {
        cy.get('#partners').click()
        cy.url().should('be.equal', this.data.CEPI_site+'partners/')
        cy.get('#uno').click()
        cy.get('#login').click()
        cy.url().should('be.equal', this.data.CEPI_site+'account/login-Page/')
    })
    it('Navigation bar options for Resources', function() {
        cy.get('#resourcesnav').click()
        cy.contains('Office of Engagement')
        cy.contains('Community Compass')
        cy.contains('About CEPI')
        cy.contains('Share Omaha')
        cy.contains('Community Engagement Roadmap')
        })
    //Verify links in homepage section
    it ('Verify links in homepage section', function() {
        cy.get('.initialcontent').should('contain', 'REGISTER A NEW CAMPUS PARTNER')
        .and('contain', 'VIEW THE COMMUNITY PARTNER LEGISLATIVE MAP')
        .and('contain', 'VIEW PARTNER AND PROJECT ANALYTICS BY FOCUS AREA')
        cy.get('a[href="https://www.unomaha.edu/engagement/index.php"]').should ('contain', 'COMMUNITY ENGAGEMENT').click().wait(3000)
            cy.visit('https://www.unomaha.edu/engagement/index.php')
            cy.origin('https://www.unomaha.edu/engagement/index.php', () => {
                cy.get('h1').should('have.text','Engagement')
            })
        cy.visit(Cypress.env('baseUrl'))
        cy.get('a[href="https://www.unomaha.edu/academic-affairs/academic-community-engagement/impact/cepi.php"]').should('contain', 'CEPI INFORMATION AND GUIDELINES')
       // cy.url().should('be.equal', 'https://www.unomaha.edu/office-of-engagement/_files/campus-user-guidelines.pdf')
//        cy.origin('.col > :nth-child(1) > p > a').contains('REGISTER A NEW CAMPUS PARTNER').click()
//        cy.url().should('be.equal','https://cepi.unomaha.edu/partners/register-Campus-Partner/')
//        cy.url().should('be.equal', this.data.CEPI_site+'partners/register-Campus-Partner/')
        })

    //Verify homepage footer
    it ('Verify homepage footer', function() {
        cy.get('.fleft').invoke('removeAttr','target').should('contain','Terms and Conditions')
        cy.get('a[href="mailto:partnerships@unomaha.edu"]').should('contain','Contact Us')

    })
})


