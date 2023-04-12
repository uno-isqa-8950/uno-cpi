import user from "../../../../support/commands"

describe("List engagement types", () => {
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
        columnLink = '.model-engagementtype > th > a',
        add = `a[href="/admin/projects/engagementtype/add/"]`,
        change = ':nth-child(1) > .field-name > a',
        name = 'input[name="name"]',
        description = 'input[name="description"]',
        form = 'form',
        continue_button = 'input[name="_continue"]',
        add_another = 'input[name="_addanother"]',
        deleteButton = 'div > [type="submit"]',
        deleteLink = '.deletelink'


    it('Can navigate to admin view', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()
    })

    it('Can add an engagement type', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink)
                .get(add).click()
                .url().should('include', '/admin/projects/engagementtype/add/')

            cy.get(name).type(this.data.engagement_type_name1)
                .should('be.empty').and('be.visible')
            cy.get(description).type(this.data.engagement_type_description1)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')

        })
    })

    it('Can change an engagement type', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Engagement types').click()
            cy.get(change).click()

            cy.get(name).clear()
            cy.get(name).type(this.data.engagement_type_description2)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change an engagement type, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Engagement types').click()
            cy.get(change).click()

            cy.get(description).clear()
            cy.get(description).type(this.data.engagement_type_description2)
                .should('be.empty').and('be.visible')

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change an engagement type, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Engagement types').click()
            cy.get(change).click()

            cy.get(name).clear()
            cy.get(name).type(this.data.engagement_type_name3)
                .should('be.empty').and('be.visible')

            cy.get(add_another).click()

            cy.get(name).type(this.data.engagement_type_name2)
                .should('be.empty').and('be.visible')
            cy.get(description).type(this.data.engagement_type_description3)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')


        })
    })

    it('Data cleanup', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Engagement types').click()
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
