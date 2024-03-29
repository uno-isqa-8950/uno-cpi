import user from "../../../../support/commands"

describe("List engagement activity types", () => {
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
        columnLink = '.model-engagementactivitytype > th > a',
        add = `a[href="/admin/projects/engagementactivitytype/add/"]`,
        change = ':nth-child(1) > .field-EngagementTypeName > a',
        engagementTypeName = 'select[name="EngagementTypeName"]',
        activityTypeName = 'select[name="ActivityTypeName"]',
        form = 'form',
        continue_button = 'input[name="_continue"]',
        add_another = 'input[name="_addanother"]',
        deleteButton = 'div > [type="submit"]',
        deleteLink = '.deletelink'


    it('Can navigate to admin view', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()
    })

    it('Can add an engagement activity type', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink)
                .get(add).click()
                .url().should('include', '/admin/projects/engagementactivitytype/add/')

            cy.get(engagementTypeName).should('be.visible')
                .select(this.data.engagement_type1, {force: true})
            cy.get(activityTypeName).should('be.visible')
                .select(this.data.activity_name1, {force: true})

            cy.get(form).submit().should('be.visible')

        })
    })

    it('Can change an engagement activity type', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Engagement activity types').click()
            cy.get(change).click()

            cy.get(engagementTypeName).should('be.visible')
                .select(this.data.engagement_type2, {force: true})


            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change an engagement activity type, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Engagement activity types').click()
            cy.get(change).click()

            cy.get(activityTypeName).should('be.visible')
                .select(this.data.activity_name2, {force: true})

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change an engagement activity type, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Engagement activity types').click()
            cy.get(change).click()

            cy.get(engagementTypeName).should('be.visible')
                .select(this.data.engagement_type3, {force: true})

            cy.get(add_another).click()

            cy.get(engagementTypeName).should('be.visible')
                .select(this.data.engagement_type4, {force: true})
            cy.get(activityTypeName).should('be.visible')
                .select(this.data.activity_name3, {force: true})

            cy.get(form).submit().should('be.visible')


        })
    })

    it('Data cleanup', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Engagement activity types').click()
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
