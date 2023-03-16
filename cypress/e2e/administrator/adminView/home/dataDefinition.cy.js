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


describe("List data definitions", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
        cy.get('#login').click().loginAdminUser(user)
        })
    })

    const adminHref = `a[href="/admin"]`,
        administratorLink = `a[class="nav-link dropdown-toggle"]`,
        adminTable = '#content-main',
        dataDefinitionColumn = '.model-datadefinition > th > a',
        addAdminDataDefinition = `a[href="/admin/home/datadefinition/add/"]`,
        changeDataDefinition = ':nth-child(1) > .field-title > a',
        id = 'input[name="id"]',
        title = 'input[name="title"]',
        description = 'input[name="description"]',
        group = 'select[name="group"]',
        form = 'form',
        continue_button = 'input[name="_continue"]',
        add_another = 'input[name="_addanother"]',
        searhbar = '#searchbar',
        searh_button = '#changelist-search > div > [type="submit"]',
        deleteDataButton = 'div > [type="submit"]',
        deleteDataDefinition = '.deletelink'


    it('Can navigate to admin view', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()
    })

    it('Can search for a data definition', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(dataDefinitionColumn).contains('Data definitions').click()
            cy.get(searhbar).type(this.data.data_definition_search)
            cy.get(searh_button).click().should('be.visible')
        })
    })


    it('Can add a new data definition', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(dataDefinitionColumn)
                .get(addAdminDataDefinition).click()
                .url().should('include', '/admin/home/datadefinition/add')

            cy.get(id).type(this.data.data_definition_id1)
                .should('be.empty').and('be.visible')
            cy.get(title).type(this.data.data_definition_title1)
                .should('be.empty').and('be.visible')
            cy.get(description).type(this.data.data_definition_description1)
                .should('be.empty').and('be.visible')
            cy.get(group).should('be.visible')
                .select(this.data.data_definition_group1, {force: true})

            cy.get(form).submit().should('be.visible')

        })
    })

    it('Can change a data definition', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(dataDefinitionColumn).contains('Data definitions').click()
            cy.get(changeDataDefinition).click()

            cy.get(description).should('be.visible').clear()
            cy.get(description).type(this.data.data_definition_description2)
                .should('be.empty').and('be.visible')
            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a data definition, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(dataDefinitionColumn).contains('Data definitions').click()
            cy.get(changeDataDefinition).click()

            cy.get(group).should('be.visible').select(this.data.data_definition_group2, {force: true})

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change a data definition, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(dataDefinitionColumn).contains('Data definitions').click()
            cy.get(changeDataDefinition).click()

            cy.get(id).should('be.visible')
            cy.get(id).clear().type(this.data.data_definition_id2)

            cy.get(add_another).click()

            cy.get(id).type(this.data.data_definition_id3)
                .should('be.empty').and('be.visible')
            cy.get(title).type(this.data.data_definition_title2)
                .should('be.empty').and('be.visible')
            cy.get(description).type(this.data.data_definition_description2)
                .should('be.empty').and('be.visible')
            cy.get(group).should('be.visible')
                .select(this.data.data_definition_group2, {force: true})
            cy.get(form).submit().should('be.visible')
        })
    })

    it('Data cleanup', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(dataDefinitionColumn).contains('Data definitions').click()
            cy.get(changeDataDefinition).click()
        })

        cy.get(deleteDataDefinition).click()
        cy.get(deleteDataButton).click()

        cy.get(adminTable).within(() => {
            cy.get(changeDataDefinition).click()
        })

        cy.get(deleteDataDefinition).click()
        cy.get(deleteDataButton).click()

        cy.get(adminTable).within(() => {
            cy.get(changeDataDefinition).click()
        })

        cy.get(deleteDataDefinition).click()
        cy.get(deleteDataButton).click()
    })


})
