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


describe("List campus partner users", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
        })
    })

    const adminHref = `a[href="/admin"]`,
        administratorLink = '[data-cy="administrator"]',
        adminTable = '#content-main',
        columnLink = '.model-campuspartneruser > th > a',
        add = `a[href="/admin/partners/campuspartneruser/add/"]`,
        change = ':nth-child(1) > .field-campus_partner > a',
        campusPartner = 'select[name="campus_partner"]',
        campusUser = 'select[name="user"]',
        form = 'form',
        continue_button = 'input[name="_continue"]',
        add_another = 'input[name="_addanother"]',
        searhbar = '#searchbar',
        searh_button = '#changelist-search > div > [type="submit"]',
        deleteButton = 'div > [type="submit"]',
        deleteLink = '.deletelink'

    it('Can navigate to admin view', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()
    })

    it('Can search for a campus partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Campus partner users').click()
            cy.get(searhbar).type(this.data.campus_partner_user_search)
            cy.get(searh_button).click().should('be.visible')
        })
    })

    it('Can add a new campus partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink)
                .get(add).click()
                .url().should('include', '/admin/partners/campuspartneruser/add/')

            cy.get(campusPartner).should('be.visible')
                .select(this.data.campus_partner1, {force: true})
            cy.get(campusUser).should('be.visible')
                .select(this.data.campus_partner_user1, {force: true})

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a campus partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Campus partner users').click()
            cy.get(change).click()

            cy.get(campusPartner).should('be.visible')
                .select(this.data.campus_partner2, {force: true})

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a campus partner user, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Campus partner users').click()
            cy.get(change).click()

            cy.get(campusUser).should('be.visible')
                .select(this.data.campus_partner_user2, {force: true})

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change a campus partner users, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Campus partner users').click()
            cy.get(change).click()

            cy.get(campusUser).should('be.visible')
                .select(this.data.campus_partner_user3, {force: true})

            cy.get(add_another).click()

            cy.get(campusPartner).should('be.visible')
                .select(this.data.campus_partner7, {force: true})
            cy.get(campusUser).should('be.visible')
                .select(this.data.campus_partner_user4, {force: true})

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Data cleanup', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Campus partner users').click()
            cy.get(searhbar).type(this.data.campus_partner1)
            cy.get(searh_button).click().should('be.visible')
            cy.get(change).click()
        })

        cy.get(deleteLink).click()
        cy.get(deleteButton).click()

        cy.get(adminTable).within(() => {
            cy.get(searhbar).clear()
            cy.get(searhbar).type(this.data.campus_partner7)
            cy.get(searh_button).click().should('be.visible')
            cy.get(change).click()
        })

        cy.get(deleteLink).click()
        cy.get(deleteButton).click()
    })

})
