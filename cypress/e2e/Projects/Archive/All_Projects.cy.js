beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })
})

describe('Projects', () => {
    it('visits the form', () => {
        cy.visit(Cypress.env('baseUrl'))
    })

    it('visits the login form', () => {
        cy.get('#login').click()
    })

    it('requires email', () => {
        cy.get('#email_input').type('shwetap1002@gmail.com{enter}')
    })

    it('requires password name', () => {
        cy.get('#password_input').type('CEPITesting123')
    })

    it('Project All Projects', () => {
        cy.get('#loginForm').submit()
        cy.get("#projectsnav").click()
        cy.contains('All Projects').click()

        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li) => {
            cy.wrap($li).contains("2016-17").click();
        })

        cy.get('#select2-id_mission-container').click()
        cy.get('#select2-id_mission-results').then(($li) => {
            cy.wrap($li).contains("Educational Support").click();
        })

        cy.get('#select2-id_community_type-container').click()
        cy.get('#select2-id_community_type-results').then(($li) => {
            cy.wrap($li).contains("Business").click();
        })

        cy.get('#select2-id_college_name-container').click()
        cy.get('#select2-id_college_name-results').then(($li) => {
            cy.wrap($li).contains("Academic Affairs").click();
        })

        cy.get('#select2-id_campus_partner-container').click()
        cy.get('#select2-id_campus_partner-results').then(($li) => {
            cy.wrap($li).contains("All").click();
        })

        cy.get('#select2-id_weitz_cec_part-container').click()
        cy.get('#select2-id_weitz_cec_part-results').then(($li) => {
            cy.wrap($li).contains("Current Community Building Partners").click();

            cy.get('#select2-id_engagement_type-container').click()
        cy.get('#select2-id_engagement_type-results').then(($li) => {
            cy.wrap($li).contains("Access to Higher Education").click();
        })
        })

        cy.get('#select2-id_k12_flag-container').click()
        cy.get('#select2-id_k12_flag-results').then(($li) => {
            cy.wrap($li).contains("Yes").click();
        })
    })
})