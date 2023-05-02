import user from "../../../support/commands.js";
beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') ||err.message.includes('Cannot read properties of null') ||err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('reading \'style\''))
        {
            return false
        }
    })
    cy.visit(Cypress.env('baseUrl'))

})
describe('Verify Profile option in user Tab', () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
           this.data = data
        cy.get('[data-cy="login"]').click()
        cy.loginCampusUser_nosession(user)
        })
    })
  it('Check login form', function() {
        cy.url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
    })
    it('Can navigate to user details', () => {
        const userDetailsLink = '[data-cy="user"]',
        profileLink = '[data-cy="accountinfo"] > .nav-link',
        update = '[data-cy="edit"]',
        name = ':nth-child(3) > [data-cy="name"]',
        alert = '[class="alert alert-danger"]',
        form = '[data-cy="update"]'
        cy.get(profileLink).click()
            .get(userDetailsLink).click()
            .url().should('include', '/partners/profile/userprofile/')
    })

    it('Non .edu users cannot edit user profile', function() {
        const userDetailsLink = '[data-cy="user"]',
        profileLink = '[data-cy="accountinfo"] > .nav-link',
        update = '[data-cy="edit"]',
        name = ':nth-child(3) > [data-cy="name"]',
        alert = '[class="alert alert-danger"]',
        form = '[data-cy="update"]'
        cy.get(profileLink).click()
            .get(userDetailsLink).click()
            .url().should('include', '/partners/profile/userprofile/')

        cy.get(update).click()
                .url().should('include', '/partners/profile/userprofileupdate/')

        cy.get(name).clear()
        cy.get(name).type(this.data.campus_partner_profile_name).should('be.visible')
        cy.get(form).submit().should('be.visible')

        cy.get(alert).contains('Please use your campus email (.edu) inorder to update your profile.').should('be.visible')
    })

})

