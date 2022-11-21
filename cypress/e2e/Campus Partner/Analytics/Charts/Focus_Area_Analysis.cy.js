beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })
})

describe('Charts Focus Area Analysis', () => {
    it('visits the form', () => {
        cy.visit(Cypress.env('baseUrl'))
    })

    it('visits the login form', () => {
        cy.get('#login').click()
    })

    it('requires email', () => {
        cy.get('#email_input').type('campususer123@gmail.com{enter}')
    })

    it('requires password name', () => {
        cy.get('#password_input').type('CEPITesting123')
    })

    it('Analytic Charts Focus Area Analysis', () => {
        cy.get('#loginForm').submit()
        cy.get('#analyticnav').click()
        cy.contains('Charts').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area Analysis').click()
        })

        cy.get('#select2-id_academicyear-container').click()
        cy.get('#select2-id_academicyear-results').then(($li) => {
            cy.wrap($li).contains("2016-17").click();
        })

        cy.get('#select2-id_endacademicyear-container').click()
        cy.get('#select2-id_endacademicyear-results').then(($li) => {
            cy.wrap($li).contains("2016-17").click();
        })

        cy.get('#select2-id_engagement_type-container').click()
        cy.get('#select2-id_engagement_type-results').then(($li) => {
            cy.wrap($li).contains("All").click();
        })

        cy.get('#select2-id_college_name-container').click()
        cy.get('#select2-id_college_name-results').then(($li) => {
            cy.wrap($li).contains("All").click();
        })

        cy.get('#select2-id_campus_partner-container').click()
        cy.get('#select2-id_campus_partner-results').then(($li) => {
            cy.wrap($li).contains("All").click();
        })

        cy.get('#select2-id_weitz_cec_part-container').click()
        cy.get('#select2-id_weitz_cec_part-results').then(($li) => {
            cy.wrap($li).contains("All").click();
        })

        cy.get('#select2-id_community_type-container').click()
        cy.get('#select2-id_community_type-results').then(($li) => {
            cy.wrap($li).contains("All").click();
        })

        cy.get('#select2-id_legislative_value-container').click()
        cy.get('#select2-id_legislative_value-results').then(($li) => {
            cy.wrap($li).contains("All").click();
        })
    })
})