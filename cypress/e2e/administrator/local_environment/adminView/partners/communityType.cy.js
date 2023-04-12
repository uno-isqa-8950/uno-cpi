import user from "../../../../support/commands"

describe("List community types", () => {
    beforeEach(() => {
        cy.on('uncaught:exception', (err) => {
            if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
            {
                return false
            }
        })
        cy.fixture("datareports").then(function(data) {
            this.data = data
        })

        cy.loginAdminUser(user)
        cy.visit(Cypress.env('baseUrl'))
    })

    const adminHref = `a[href="/admin"]`,
        administratorLink = '[data-cy="administrator"]',
        adminTable = '#content-main',
        columnLink = '.model-communitytype > th > a',
        add = `a[href="/admin/partners/communitytype/add/"]`,
        change = ':nth-child(1) > .field-__str__ > a',
        communityType = 'input[name="community_type"]',
        form = 'form',
        continue_button = 'input[name="_continue"]',
        add_another = 'input[name="_addanother"]',
        deleteButton = 'div > [type="submit"]',
        deleteLink = '.deletelink'


    it('Can navigate to admin view', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()
    })

    it('Can add a new community type', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink)
                .get(add).click()
                .url().should('include', '/admin/partners/communitytype/add/')

            cy.get(communityType).type(this.data.community_type7)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')

        })
    })

    it('Can change a community type', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Community types').click()
            cy.get(change).click()

            cy.get(communityType).clear()
            cy.get(communityType).type(this.data.community_type8)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a community type, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Community types').click()
            cy.get(change).click()

            cy.get(communityType).clear()
            cy.get(communityType).type(this.data.community_type9)
                .should('be.empty').and('be.visible')

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change a community type, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Community types').click()
            cy.get(change).click()

            cy.get(communityType).clear()
            cy.get(communityType).type(this.data.community_type10)
                .should('be.empty').and('be.visible')

            cy.get(add_another).click()

            cy.get(communityType).type(this.data.community_type11)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')


        })
    })

    it('Data cleanup', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Community types').click()
            cy.get(change).click()
        })

        cy.get(deleteLink).click()
        cy.get(deleteButton).click()

        cy.get(adminTable).within(() => {
            cy.get(change).click()
        })

        cy.get(deleteLink).click()
        cy.get(deleteButton).click()
    })

})
