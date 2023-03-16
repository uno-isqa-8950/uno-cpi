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


describe("List household income", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
        cy.get('#login').click().loginAdminUser(user)
        })
    })

    const adminHref = `a[href="/admin"]`,
        administratorLink = `a[class="nav-link dropdown-toggle"]`,
        adminTable = '#content-main',
        householdIncomeColumn = '.model-householdincome > th > a',
        addHouseholdIncome = `a[href="/admin/home/householdincome/add/"]`,
        changeHouseholdIncome = ':nth-child(1) > .field-county > a',
        id = 'input[name="id2"]',
        county = 'input[name="county"]',
        state = 'input[name="state"]',
        median_income = 'input[name="median_income"]',
        margin_error = 'input[name="margin_error"]',
        rank = 'input[name="rank"]',
        form = 'form',
        continue_button = 'input[name="_continue"]',
        add_another = 'input[name="_addanother"]',
        deleteHouseholdButton = 'div > [type="submit"]',
        deleteHouseholdIncome = '.deletelink'


    it('Can navigate to admin view', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()
    })

    it('Can add a household income', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(householdIncomeColumn)
                .get(addHouseholdIncome).click()
                .url().should('include', '/admin/home/householdincome/add/')

            cy.get(id).type(this.data.household_id1)
                .should('be.empty').and('be.visible')
            cy.get(county).type(this.data.household_county1)
                .should('be.empty').and('be.visible')
            cy.get(state).type(this.data.household_state1)
                .should('be.empty').and('be.visible')
            cy.get(median_income).type(this.data.household_median_income1)
                .should('be.empty').and('be.visible')
            cy.get(margin_error).type(this.data.household_margin_error1)
                .should('be.empty').and('be.visible')
            cy.get(rank).type(this.data.household_rank1)
                .should('be.empty').and('be.visible')
            cy.get(form).submit().should('be.visible')

        })
    })

    it('Can change household income', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(householdIncomeColumn).contains('Household incomes').click()
            cy.get(changeHouseholdIncome).click()

            cy.get(median_income).clear()
            cy.get(median_income).type(this.data.household_median_income2)
                .should('be.empty').and('be.visible')
            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change household income, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(householdIncomeColumn).contains('Household incomes').click()
            cy.get(changeHouseholdIncome).click()

            cy.get(rank).clear()
            cy.get(rank).type(this.data.household_rank2)
                .should('be.empty').and('be.visible')

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change household income, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(householdIncomeColumn).contains('Household incomes').click()
            cy.get(changeHouseholdIncome).click()

            cy.get(margin_error).clear()
            cy.get(margin_error).type(this.data.household_margin_error1)
                .should('be.empty').and('be.visible')

            cy.get(add_another).click()

            cy.get(id).type(this.data.household_id2)
                .should('be.empty').and('be.visible')
            cy.get(county).type(this.data.household_county2)
                .should('be.empty').and('be.visible')
            cy.get(state).type(this.data.household_state2)
                .should('be.empty').and('be.visible')
            cy.get(median_income).type(this.data.household_median_income3)
                .should('be.empty').and('be.visible')
            cy.get(margin_error).type(this.data.household_margin_error2)
                .should('be.empty').and('be.visible')
            cy.get(rank).type(this.data.household_rank2)
                .should('be.empty').and('be.visible')
            cy.get(form).submit().should('be.visible')
        })
    })

    it('Data cleanup', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(householdIncomeColumn).contains('Household incomes').click()
            cy.get(changeHouseholdIncome).click()
        })

        cy.get(deleteHouseholdIncome).click()
        cy.get(deleteHouseholdButton).click()

        cy.get(adminTable).within(() => {
            cy.get(changeHouseholdIncome).click()
        })

        cy.get(deleteHouseholdIncome).click()
        cy.get(deleteHouseholdButton).click()
    })


})
