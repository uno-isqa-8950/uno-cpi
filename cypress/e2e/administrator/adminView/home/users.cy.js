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


describe("List users", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
        })
    })

    const adminHref = `a[href="/admin"]`,
        administratorLink = '[data-cy="administrator"]',
        adminTable = '#content-main',
        userColumn = '.model-user > th > a',
        addUser = `a[href="/admin/home/user/add/"]`,
        changeUser = ':nth-child(1) > .field-email > a',
        email = 'input[name="email"]',
        password = 'input[name="password"]',
        first_name = 'input[name="first_name"]',
        last_name = 'input[name="last_name"]',
        university = 'select[name="university"]',
        loginDate = 'input[name="last_login_0"]',
        loginTime = 'input[name="last_login_1"]',
        form = 'form',
        continue_button = 'input[name="_continue"]',
        add_another = 'input[name="_addanother"]',
        searhbar = '#searchbar',
        searh_button = '#changelist-search > div > [type="submit"]',
        deleteUserButton = 'div > [type="submit"]',
        deleteUser = '.deletelink'


    it('Can navigate to admin view', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()
    })

    it('Can search for a user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(userColumn).contains('Users').click()
            cy.get(searhbar).type(this.data.user_search)
            cy.get(searh_button).click().should('be.visible')
        })
    })


    it('Can add a new user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(userColumn)
                .get(addUser).click()
                .url().should('include', '/admin/home/user/add/')

            cy.get(email).type(this.data.user_email1)
                .should('be.empty').and('be.visible')
            cy.get(password).type(this.data.user_password1)
                .should('be.empty').and('be.visible')
            cy.get(first_name).type(this.data.user_first_name1)
                .should('be.empty').and('be.visible')
            cy.get(last_name).type(this.data.user_last_name1)
                .should('be.empty').and('be.visible')
            cy.get(university).should('be.visible').select(this.data.university1, {force: true})
            cy.get(loginDate).type(this.data.user_date1)
                .should('be.empty').and('be.visible')
            cy.get(loginTime).type(this.data.user_time1)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')

        })
    })

    it('Can change a user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(userColumn).contains('Users').click()
            cy.get(changeUser).click()

            cy.get(last_name).clear()
            cy.get(last_name).type(this.data.user_last_name2)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a user, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(userColumn).contains('Users').click()
            cy.get(changeUser).click()

            cy.get(password).clear()
            cy.get(password).type(this.data.user_password2)
                .should('be.empty').and('be.visible')

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change a user, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(userColumn).contains('Users').click()
            cy.get(changeUser).click()

            cy.get(university).should('be.visible')
                .select(this.data.university2, {force: true})

            cy.get(add_another).click()

            cy.get(email).type(this.data.user_email2)
                .should('be.empty').and('be.visible')
            cy.get(password).type(this.data.user_password3)
                .should('be.empty').and('be.visible')
            cy.get(first_name).type(this.data.user_first_name2)
                .should('be.empty').and('be.visible')
            cy.get(last_name).type(this.data.user_last_name3)
                .should('be.empty').and('be.visible')
            cy.get(university).should('be.visible').select(this.data.university1, {force: true})
            cy.get(loginDate).type(this.data.user_date2)
                .should('be.empty').and('be.visible')
            cy.get(loginTime).type(this.data.user_time2)
                .should('be.empty').and('be.visible')
            cy.get(form).submit().should('be.visible')
        })
    })

    it('Data cleanup', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(userColumn).contains('Users').click()
            cy.get(searhbar).type(this.data.user_email1)
            cy.get(searh_button).click().should('be.visible')
            cy.get(changeUser).click()
        })

        cy.get(deleteUser).click()
        cy.get(deleteUserButton).click()

        cy.get(adminTable).within(() => {
            cy.get(searhbar).clear()
            cy.get(searhbar).type(this.data.user_email2)
            cy.get(searh_button).click().should('be.visible')
            cy.get(changeUser).click()
        })

        cy.get(deleteUser).click()
        cy.get(deleteUserButton).click()
        cy.get(searhbar).clear()
    })


})
