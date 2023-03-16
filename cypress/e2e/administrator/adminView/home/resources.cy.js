import user from "../../../../support/commands"
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


describe("List resources", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
        })
    })

    const adminHref = `a[href="/admin"]`,
        administratorLink = `a[class="nav-link dropdown-toggle"]`,
        adminTable = '#content-main',
        resourceColumn = '.model-resource > th > a',
        addResource = `a[href="/admin/home/resource/add/"]`,
        changeResource = ':nth-child(1) > .field-resource_descr > a',
        description = 'input[name="resource_descr"]',
        resource_link = 'input[name="resource_link"]',
        listing = 'input[name="listing_order"]',
        form = 'form',
        continue_button = 'input[name="_continue"]',
        add_another = 'input[name="_addanother"]',
        searhbar = '#searchbar',
        searh_button = '#changelist-search > div > [type="submit"]',
        deleteResourceButton = 'div > [type="submit"]',
        deleteResource = '.deletelink'


    it('Can navigate to admin view', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()
    })

    it('Can search for a resource', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(resourceColumn).contains('Resources').click()
            cy.get(searhbar).type(this.data.contact_search)
            cy.get(searh_button).click().should('be.visible')
        })
    })


    it('Can add a new resource', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(resourceColumn)
                .get(addResource).click()
                .url().should('include', '/admin/home/resource/add/')

            cy.get(description).type(this.data.resource_description1)
                .should('be.empty').and('be.visible')
            cy.get(resource_link).type(this.data.resource_link1)
                .should('be.empty').and('be.visible')
            cy.get(listing).type(this.data.resource_listing1)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')

        })
    })

    it('Can change a resource', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(resourceColumn).contains('Resources').click()
            cy.get(changeResource).click()

            cy.get(description).clear()
            cy.get(description).type(this.data.resource_description2)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a resource, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(resourceColumn).contains('Resources').click()
            cy.get(changeResource).click()

            cy.get(listing).clear()
            cy.get(listing).type(this.data.resource_listing2)
                .should('be.empty').and('be.visible')

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change a resource, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(resourceColumn).contains('Resources').click()
            cy.get(changeResource).click()

            cy.get(listing).clear()
            cy.get(listing).type(this.data.resource_listing1)
                .should('be.empty').and('be.visible')

            cy.get(add_another).click()

            cy.get(description).type(this.data.resource_description3)
                .should('be.empty').and('be.visible')
            cy.get(resource_link).type(this.data.resource_link2)
                .should('be.empty').and('be.visible')
            cy.get(listing).type(this.data.resource_listing3)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Data cleanup', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(resourceColumn).contains('Resources').click()
            cy.get(changeResource).click()
        })

        cy.get(deleteResource).click()
        cy.get(deleteResourceButton).click()

        cy.get(adminTable).within(() => {
            cy.get(changeResource).click()
        })

        cy.get(deleteResource).click()
        cy.get(deleteResourceButton).click()
    })


})
