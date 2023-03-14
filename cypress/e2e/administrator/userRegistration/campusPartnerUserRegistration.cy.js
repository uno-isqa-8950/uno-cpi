/*beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })
})

describe('Admin User Registration', () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
            })
        }
    )

    it("Can login", () => {
        cy.visit(Cypress.env('admin'))
        cy.get("input[name='username']").type(Cypress.env('username')).should("have.value", Cypress.env('username'))
        cy.get("input[name='password']").type(Cypress.env('password')).should("have.value", Cypress.env('password'))
        cy.get("form").submit().should('be.visible')
        cy.visit(Cypress.env('userVisitUrl'))
        cy.wait(700)
    })

    it("Can add user email and password", () => {
        cy.get("input[name='email']").type(Cypress.env('user_email')).should("have.value", Cypress.env('email'))
        cy.get("input[name='password']").type(Cypress.env('user_password')).should("have.value", Cypress.env('password'))
        cy.wait(700)
    })

    it("Can add personal info", () => {
        cy.get("input[name='first_name']").type(Cypress.env('user_first_name')).should("have.value", Cypress.env('user_first_name'))
        cy.get("input[name='last_name']").type(Cypress.env('user_last_name')).should("have.value", Cypress.env('user_last_name'))
        cy.wait(700)
    })

    it("Can add permissions", () => {
        cy.get('#id_university').click()
        cy.contains('University').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show');
            cy.wrap($el).contains(this.data.university).click();
        })
        cy.get('#id_is_campuspartner').click().should('be.visible')
        cy.wait(700)
    })

    it("Can add date and time", () => {
        cy.get('input[id_last_login_0]').type(Cypress.env('date')).should("have.value", Cypress.env('date'))
        cy.get('input[id_last_login_1]').type(Cypress.env('time')).should("have.value", Cypress.env('time'))
        cy.wait(700)
    })

    it("Can successfully create campus partner public user", () => {
        cy.get("form").submit().should('be.visible')
    })
})
*/


import user from "../../../support/commands";

beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })

    cy.visit(Cypress.env('baseUrl'))
    cy.get('#login').click().loginAdminUser(user)
})


describe("List and sort campus partner organizations", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
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
