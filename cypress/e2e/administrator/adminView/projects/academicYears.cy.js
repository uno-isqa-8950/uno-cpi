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


describe("List academic years", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
        })
    })

    const adminHref = `a[href="/admin"]`,
        administratorLink = '[data-cy="administrator"]',
        adminTable = '#content-main',
        columnLink = '.model-academicyear > th > a',
        add = `a[href="/admin/projects/academicyear/add/"]`,
        change = ':nth-child(1) > .field-academic_year > a',
        academicYear = 'input[name="academic_year"]',
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

    it('Can add an academic year', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink)
                .get(add).click()
                .url().should('include', '/admin/projects/academicyear/add/')

            cy.get(academicYear).type(this.data.academic_year5)
                .should('be.empty').and('be.visible')
            cy.get(description).type(this.data.partner_description1)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')

        })
    })

    it('Can change an academic year', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Academic years').click()
            cy.get(change).click()

            cy.get(academicYear).clear()
            cy.get(academicYear).type(this.data.academic_year6)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change an academic year, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Academic years').click()
            cy.get(change).click()

            cy.get(description).clear()
            cy.get(description).type(this.data.partner_description2)
                .should('be.empty').and('be.visible')

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change an academic year, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Academic years').click()
            cy.get(change).click()

            cy.get(academicYear).clear()
            cy.get(academicYear).type(this.data.academic_year2)
                .should('be.empty').and('be.visible')

            cy.get(add_another).click()

            cy.get(academicYear).type(this.data.academic_year7)
                .should('be.empty').and('be.visible')
            cy.get(description).type(this.data.partner_description3)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')


        })
    })

    it('Data cleanup', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Academic years').click()
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
