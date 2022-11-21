function random_Text_Alpha_Numeric() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (var i = 0; i < 10; i++)
      text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}

beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })
})

describe('Projects', () => {
    var randomPartnerName = random_Text_Alpha_Numeric();
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

    it('Project All Projects', () => {
        cy.get('#loginForm').submit()
        cy.get("#projectsnav").click()
        cy.contains('My Drafts').click()
        cy.contains('td', 'KD test').click()
        cy.contains('td', 'Action')
            .contains('a', 'Edit')
            .click()

        cy.get('#select2-id_engagement_type-container').click()
        cy.get('#select2-id_engagement_type-results').then(($li) => {
            cy.wrap($li).contains("Access to Higher Education").click()
            cy.get('#id_description').type(randomPartnerName)
        })

        cy.get("#projectdurationnav").click()
        cy.get('#select2-id_semester-container').click()
        cy.get('#select2-id_semester-results').then(($li) => {
            cy.wrap($li).contains("Fall").click();
        })

        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li) => {
            cy.wrap($li).contains("2019-20").click();
        })

        cy.get("#participantinfonav").click()
        cy.get('#id_total_uno_students').type('1')
        cy.get('#id_total_uno_hours').type('1')
        cy.get('#id_total_other_community_members').type('1')
        cy.contains('Save as Draft').click()

        /*cy.get('#id_community_edit-1-community_partner').select('AIM Institute')
        cy.get(".add-community-row").click()

        cy.get("#campuspartnerinfonav").click()
        cy.get('#campus_edit-1-campus_partner').select('Biology')
        cy.wait(1000)
        cy.get(".add-campus-row").click()
        cy.contains('Next').click()

        cy.get('#id_mission_area').select('Social Justice')
        cy.contains('Next').click()

        cy.get('#id_address_line1').type('123 S 70th Plz')
        cy.get('#id_city').type('Omaha')
        cy.get('#id_state').type('NE')
        cy.get('#id_country').type('USA')
        cy.get('#terms').click()*/
    })
})