import user from "../../../../support/commands"
beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })
    cy.visit(Cypress.env('baseUrl'))
})


describe("List community partner users", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
            cy.get('#login').click().loginAdminUser(user)
        })
    })

    const adminHref = `a[href="/admin"]`,
        administratorLink = '[data-cy="administrator"]',
        adminTable = '#content-main',
        columnLink = '.model-communitypartneruser > th > a',
        add = `a[href="/admin/partners/communitypartneruser/add/"]`,
        change = ':nth-child(1) > .field-community_partner > a',
        communityPartner = 'select[name="community_partner"]',
        user = 'select[name="user"]',
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

    it('Can search for a community partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Community partner users').click()
            cy.get(searhbar).type(this.data.community_partner_user_search)
            cy.get(searh_button).click().should('be.visible')
        })
    })


    it('Can add a new community partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink)
                .get(add).click()
                .url().should('include', '/admin/partners/communitypartneruser/add/')

            cy.get(communityPartner).should('be.visible')
                .select(this.data.community_partner3, {force: true})
            cy.get(user).should('be.visible')
                .select(this.data.community_partner_user1, {force: true})

            cy.get(form).submit().should('be.visible')

        })
    })

    it('Can change a community partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Community partner users').click()
            cy.get(change).click()

            cy.get(user).should('be.visible')
                .select(this.data.community_partner_user2, {force: true})

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a community partner user, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Community partner users').click()
            cy.get(change).click()

            cy.get(user).should('be.visible')
                .select(this.data.community_partner_user3, {force: true})

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change a community partner user, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Community partner users').click()
            cy.get(change).click()

            cy.get(communityPartner).should('be.visible')
                .select(this.data.community_partner3, {force: true})

            cy.get(add_another).click()

            cy.get(communityPartner).should('be.visible')
                .select(this.data.community_partner5, {force: true})
            cy.get(user).should('be.visible')
                .select(this.data.community_partner_user4, {force: true})

            cy.get(form).submit().should('be.visible')


        })
    })

    it('Data cleanup', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Community partner users').click()
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
