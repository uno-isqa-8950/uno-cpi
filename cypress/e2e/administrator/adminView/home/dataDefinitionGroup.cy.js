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


describe("List data definition groups", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
        })
    })

    const adminHref = `a[href="/admin"]`,
        administratorLink = '[data-cy="administrator"]',
        adminTable = '#content-main',
        dataDefinitionColumn = '.model-datadefinitiongroup > th > a',
        addDataDefinitionGroup = `a[href="/admin/home/datadefinitiongroup/add/"]`,
        changeDataDefinitionGroup = ':nth-child(1) > .field-group > a',
        group_name = 'input[name="group"]',
        form = 'form',
        continue_button = 'input[name="_continue"]',
        add_another = 'input[name="_addanother"]',
        searhbar = '#searchbar',
        searh_button = '#changelist-search > div > [type="submit"]',
        deleteGroupButton = 'div > [type="submit"]',
        deleteDataGroup = '.deletelink'


    it('Can navigate to admin view', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()
    })

    it('Can search for a data definition group', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(dataDefinitionColumn).contains('Data definition groups').click()
            cy.get(searhbar).type(this.data.data_definition_group1)
            cy.get(searh_button).click().should('be.visible')
        })
    })


    it('Can add a new data definition group', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(dataDefinitionColumn)
                .get(addDataDefinitionGroup).click()
                .url().should('include', '/admin/home/datadefinitiongroup/add/')

            cy.get(group_name).clear()
            cy.get(group_name).type(this.data.group_name1)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')

        })
    })

    it('Can change a data definition group', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(dataDefinitionColumn).contains('Data definition groups').click()
            cy.get(changeDataDefinitionGroup).click()

            cy.get(group_name).clear()
            cy.get(group_name).type(this.data.group_name2)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a data definition group, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(dataDefinitionColumn).contains('Data definition groups').click()
            cy.get(changeDataDefinitionGroup).click()

            cy.get(group_name).clear()
            cy.get(group_name).type(this.data.group_name3)
                .should('be.empty').and('be.visible')

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change a data definition group, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(dataDefinitionColumn).contains('Data definition groups').click()
            cy.get(changeDataDefinitionGroup).click()

            cy.get(group_name).clear()
            cy.get(group_name).type(this.data.group_name4)
                .should('be.empty').and('be.visible')

            cy.get(add_another).click()

            cy.get(group_name).clear()
            cy.get(group_name).type(this.data.group_name5)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Data cleanup', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(dataDefinitionColumn).contains('Data definition groups').click()
            cy.get(changeDataDefinitionGroup).click()
        })

        cy.get(deleteDataGroup).click()
        cy.get(deleteGroupButton).click()

        cy.get(adminTable).within(() => {
            cy.get(changeDataDefinitionGroup).click()
        })

        cy.get(deleteDataGroup).click()
        cy.get(deleteGroupButton).click()
    })
})
