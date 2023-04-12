import user from "../../../../support/commands"

describe("List campus partners", () => {
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
        columnLink = '.model-campuspartner > th > a',
        add = `a[href="/admin/partners/campuspartner/add/"]`,
        change = ':nth-child(1) > .field-name > a',
        campusPartnerName = 'input[name="name"]',
        campusCollegeName = 'select[name="college_name"]',
        campusPartnerUniversity = 'select[name="university"]',
        campusEducationSystem = 'select[name="education_system"]',
        campusPartnerStatus = 'select[name="partner_status"]',
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

    it('Can search for a campus partner', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Campus partners').click()
            cy.get(searhbar).type(this.data.campus_partner_search)
            cy.get(searh_button).click().should('be.visible')
        })
    })

    it('Can add a new campus partner', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink)
                .get(add).click()
                .url().should('include', '/admin/partners/campuspartner/add/')

            cy.get(campusPartnerName).type(this.data.campus_partner_name1)
                .should('be.empty').and('be.visible')
            cy.get(campusCollegeName).should('be.visible')
                .select(this.data.campus_partner_college1, {force: true})
            cy.get(campusPartnerUniversity).should('be.visible')
                .select(this.data.university2, {force: true})
            cy.get(campusEducationSystem).should('be.visible')
                .select(this.data.campus_partner_education_system, {force: true})
            cy.get(campusPartnerStatus).should('be.visible')
                .select(this.data.campus_partner_status1, {force: true})

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a campus partner', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Campus partners').click()
            cy.get(change).click()

            cy.get(campusCollegeName).should('be.visible')
                .select(this.data.campus_partner_college2, {force: true})

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a campus partner, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Campus partners').click()
            cy.get(change).click()

            cy.get(campusPartnerUniversity).should('be.visible')
                .select(this.data.university1, {force: true})

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change a campus partner active year, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Campus partners').click()
            cy.get(change).click()

            cy.get(campusPartnerStatus).should('be.visible')
                .select(this.data.campus_partner_status2, {force: true})

            cy.get(add_another).click()

            cy.get(campusPartnerName).type(this.data.campus_partner_name2)
                .should('be.empty').and('be.visible')
            cy.get(campusCollegeName).should('be.visible')
                .select(this.data.campus_partner_college3, {force: true})
            cy.get(campusPartnerUniversity).should('be.visible')
                .select(this.data.university1, {force: true})
            cy.get(campusEducationSystem).should('be.visible')
                .select(this.data.campus_partner_education_system, {force: true})
            cy.get(campusPartnerStatus).should('be.visible')
                .select(this.data.campus_partner_status3, {force: true})

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Data cleanup', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Campus partners').click()
            cy.get(searhbar).type(this.data.campus_partner_name1)
            cy.get(searh_button).click().should('be.visible')
            cy.get(change).click()
        })

        cy.get(deleteLink).click()
        cy.get(deleteButton).click()

        cy.get(adminTable).within(() => {
            cy.get(searhbar).clear()
            cy.get(searhbar).type(this.data.campus_partner_name2)
            cy.get(searh_button).click().should('be.visible')
            cy.get(change).click()
        })

        cy.get(deleteLink).click()
        cy.get(deleteButton).click()
    })

})
