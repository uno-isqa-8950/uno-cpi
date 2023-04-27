import user from "../../../support/commands"

describe('Change user details from profile page', () => {
  beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
      {
        return false
      }
    })
    cy.fixture("datareports").then(function(data) {
      this.data = data
    })
    cy.loginCampusUser(user) // Admin User is logged in before the test begins
    cy.visit(Cypress.env('baseUrl'))
  })

    const userDetailsLink = '[data-cy="user"]',
        profileLink = '[data-cy="accountinfo"]',
        update = '[data-cy="edit"]',
        name = ':nth-child(3) > [data-cy="name"]',
        alert = '[class="alert alert-danger"]',
        form = '[data-cy="update"]'

    it('Can navigate to user details', () => {
        cy.get(profileLink).click()
            .get(userDetailsLink).click()
            .url().should('include', '/partners/profile/userprofile/')
    })

    it('Non .edu users cannot edit user profile', function() {
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

