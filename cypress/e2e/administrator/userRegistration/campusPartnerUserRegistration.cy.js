import user from "../../../support/commands";

beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })

    cy.visit(Cypress.env('baseUrl'))
})


describe("List and sort campus partner organizations", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
            cy.get('#login').click().loginAdminUser(user)
        })
    })

    const administratorLink = `a[class="nav-link dropdown-toggle"]`,
        campusPartnerUserHref = `a[href="/register-Campus-Partner-User/"]`,
        campusPartnerLabel = '.control-label',
        campusPartnerDropdown = 'select[name="campus_partner"]',
        firstName = 'input[name="first_name"]',
        lastName = 'input[name="last_name"]',
        email = 'input[name="email"]',
        terms = '#terms'


    it('Verifies user with .edu email can be registered', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(campusPartnerUserHref).click()
            .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/register-Campus-Partner-User/')

        cy.get(campusPartnerLabel).contains('Campus Partner')
        cy.get(campusPartnerDropdown).should('be.visible').select('Accounting', {force: true})

        cy.get(campusPartnerLabel).contains('First Name')
        cy.get(firstName).type('John').should("have.value", 'John')

        cy.get(campusPartnerLabel).contains('Last Name')
        cy.get(lastName).type('Doe').should("have.value", 'Doe')

        cy.get(campusPartnerLabel).contains('Email')
        cy.get(email).type('usercampustest@unomaha.edu').should("have.value", 'usercampustest@unomaha.edu')

        cy.get(terms).check().should('exist')
        //cy.url().should('eq', 'https://unocpi.s3.amazonaws.com/documents/Terms_and_Conditions.pdf')

        cy.get("form").submit().should('be.visible')

    })

    it('Verifies user with non .edu email cannot be registered', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(campusPartnerUserHref).click()
            .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/register-Campus-Partner-User/')

        cy.get(campusPartnerLabel).contains('Campus Partner')
        cy.get(campusPartnerDropdown).should('be.visible').select('Accounting', {force: true})

        cy.get(campusPartnerLabel).contains('First Name')
        cy.get(firstName).type('John').should("have.value", 'John')

        cy.get(campusPartnerLabel).contains('Last Name')
        cy.get(lastName).type('Doe').should("have.value", 'Doe')

        cy.get(campusPartnerLabel).contains('Email')
        cy.get(email).type('usercampustest@unomaha.edu').should("have.value", 'usercampustest@unomaha.edu')

        cy.get(terms).check().should('exist')
        //cy.url().should('eq', 'https://unocpi.s3.amazonaws.com/documents/Terms_and_Conditions.pdf')

        cy.get("form").submit().should('be.visible')

        cy.get([".alert-danger strong"])
            .contains('Please use your campus email (.edu) for the registration of a Campus Partner User.')

    })


})
