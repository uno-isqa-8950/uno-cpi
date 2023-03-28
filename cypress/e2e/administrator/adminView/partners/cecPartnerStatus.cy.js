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


describe("List CEC Partner Status", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
        })
    })

    const adminHref = `a[href="/admin"]`,
        administratorLink = '[data-cy="administrator"]',
        adminTable = '#content-main',
        columnLink = '.model-cecpartnerstatus > th > a',
        add = `a[href="/admin/partners/cecpartnerstatus/add/"]`,
        change = ':nth-child(1) > .field-name > a',
        cecPartnerStatusName = 'input[name="name"]',
        cecPartnerStatsDescription = 'input[name="description"]',
        form = 'form',
        continue_button = 'input[name="_continue"]',
        add_another = 'input[name="_addanother"]',
        deleteButton = 'div > [type="submit"]',
        deleteLink = '.deletelink'

    it('Can navigate to admin view', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()
    })

    it('Can add a new CEC Partner Status', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink)
                .get(add).click()
                .url().should('include', '/admin/partners/cecpartnerstatus/add/')

            cy.get(cecPartnerStatusName).type(this.data.cec_partner_status_name1)
                .should('be.empty').and('be.visible')
            cy.get(cecPartnerStatsDescription).type(this.data.cec_partner_status_description1)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a CEC Partner Status', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('CEC Partner Statuses').click()
            cy.get(change).click()

            cy.get(cecPartnerStatusName).clear()
            cy.get(cecPartnerStatusName).type(this.data.cec_partner_status_name2)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a CEC Partner Status, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('CEC Partner Statuses').click()
            cy.get(change).click()

            cy.get(cecPartnerStatsDescription).clear()
            cy.get(cecPartnerStatsDescription).type(this.data.cec_partner_status_description2)
                .should('be.empty').and('be.visible')

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change a CEC Partner Status, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('CEC Partner Statuses').click()
            cy.get(change).click()

            cy.get(cecPartnerStatusName).clear()
            cy.get(cecPartnerStatusName).type(this.data.cec_partner_status_name3)
                .should('be.empty').and('be.visible')

            cy.get(add_another).click()

            cy.get(cecPartnerStatusName).type(this.data.cec_partner_status_name4)
                .should('be.empty').and('be.visible')
            cy.get(cecPartnerStatsDescription).type(this.data.cec_partner_status_description3)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Data cleanup', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('CEC Partner Statuses').click()
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
