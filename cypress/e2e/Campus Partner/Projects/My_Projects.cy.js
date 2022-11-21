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
        cy.get('#email_input').type('campususer123@gmail.com{enter}')
    })

    it('requires password name', () => {
        cy.get('#password_input').type('CEPITesting123')
    })

    it('Project My Projects', () => {
        cy.get('#loginForm').submit()
        cy.get("#projectsnav").click()
        cy.contains('My Project').click()
        /*cy.contains('td', 'Ancient Mediterranean Studies Fall Lecture').click()
        cy.contains('td', 'Action')
            .contains('a', 'Edit')
            .click()

        cy.get('#select2-id_engagement_type-container').click()
        cy.get('#select2-id_engagement_type-results').then(($li) => {
            cy.wrap($li).contains("Access to Higher Education").click();
        })

        cy.contains('Next').click()
        cy.get('#id_community_edit-1-community_partner').select('AIM Institute')
        cy.get(".addCommunityPartner").click()
        cy.contains('Next').click()

        cy.get('#id_mission_area').select('Social Justice')
        cy.contains('Next').click()

        cy.get("#terms").click()
        cy.contains('Update').click()*/
    })
})
