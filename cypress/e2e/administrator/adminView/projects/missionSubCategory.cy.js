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


describe("List mission sub categories", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
        })
    })

    const adminHref = `a[href="/admin"]`,
        administratorLink = '[data-cy="administrator"]',
        adminTable = '#content-main',
        columnLink = '.model-missionsubcategory > th > a',
        add = `a[href="/admin/projects/missionsubcategory/add/"]`,
        change = ':nth-child(1) > .field-secondary_mission_area  > a',
        subCategory = 'select[name="sub_category"]',
        secondaryMissionArea = 'select[name="secondary_mission_area"]',
        form = 'form',
        continue_button = 'input[name="_continue"]',
        add_another = 'input[name="_addanother"]',
        deleteButton = 'div > [type="submit"]',
        deleteLink = '.deletelink'


    it('Can navigate to admin view', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()
    })

    it('Can add a mission sub category', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink)
                .get(add).click()
                .url().should('include', '/admin/projects/missionsubcategory/add/')

            cy.get(subCategory).should('be.visible')
                .select(this.data.mission_subcategory1, {force: true})
            cy.get(secondaryMissionArea).should('be.visible')
                .select(this.data.secondary_mission_area1, {force: true})

            cy.get(form).submit().should('be.visible')

        })
    })

    it('Can change a mission sub category', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Mission sub categorys').click()
            cy.get(change).click()

            cy.get(subCategory).should('be.visible')
                .select(this.data.mission_subcategory2, {force: true})

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a mission sub category, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Mission sub categorys').click()
            cy.get(change).click()

            cy.get(secondaryMissionArea).should('be.visible')
                .select(this.data.secondary_mission_area2, {force: true})

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change a mission sub category, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Mission sub categorys').click()
            cy.get(change).click()

            cy.get(subCategory).should('be.visible')
                .select(this.data.mission_subcategory3, {force: true})

            cy.get(add_another).click()

            cy.get(subCategory).should('be.visible')
                .select(this.data.mission_subcategory2, {force: true})
            cy.get(secondaryMissionArea).should('be.visible')
                .select(this.data.secondary_mission_area3, {force: true})

            cy.get(form).submit().should('be.visible')


        })
    })

    it('Data cleanup', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Mission sub categorys').click()
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
