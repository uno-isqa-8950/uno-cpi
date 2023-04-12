import user from "../../../../support/commands"

describe("List CEC Building Partner Active Year", () => {
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
        columnLink = '.model-cecpartactiveyrs > th > a',
        add = `a[href="/admin/partners/cecpartactiveyrs/add/"]`,
        change = ':nth-child(1) > .field-start_semester > a',
        startSemester = 'select[name="start_semester"]',
        startAcadYear = 'select[name="start_acad_year"]',
        endSemester = 'select[name="end_semester"]',
        endAcadYear = 'select[name="end_acad_year"]',
        communityPartner = 'select[name="comm_partner"]',
        campusPartner = 'select[name="camp_partner"]',
        form = 'form',
        continue_button = 'input[name="_continue"]',
        add_another = 'input[name="_addanother"]',
        deleteButton = 'div > [type="submit"]',
        deleteLink = '.deletelink'

    it('Can navigate to admin view', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()
    })

    it('Can add a new CEC Building partner active year', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink)
                .get(add).click()
                .url().should('include', '/admin/partners/cecpartactiveyrs/add/')

            cy.get(startSemester).should('be.visible')
                .select(this.data.cec_building_start_semester1, {force: true})
            cy.get(startAcadYear).should('be.visible')
                .select(this.data.cec_building_start_academic1, {force: true})
            cy.get(endSemester).should('be.visible')
                .select(this.data.cec_building_end_semester1, {force: true})
            cy.get(endAcadYear).should('be.visible')
                .select(this.data.cec_building_end_academic1, {force: true})
            cy.get(communityPartner).should('be.visible')
                .select(this.data.community_partner4, {force: true})
            cy.get(campusPartner).should('be.visible')
                .select(this.data.campus_partner12, {force: true})

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a CEC Building partner active year', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('CEC Building Partner Active Year').click()
            cy.get(change).click()

            cy.get(endSemester).should('be.visible')
                .select(this.data.cec_building_end_semester2, {force: true})

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a CEC Building partner active year, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('CEC Building Partner Active Year').click()
            cy.get(change).click()

            cy.get(endAcadYear).should('be.visible')
                .select(this.data.cec_building_end_academic2, {force: true})

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change a CEC Building partner active year, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('CEC Building Partner Active Year').click()
            cy.get(change).click()

            cy.get(communityPartner).should('be.visible')
                .select(this.data.community_partner4, {force: true})

            cy.get(add_another).click()

            cy.get(startSemester).should('be.visible')
                .select(this.data.cec_building_start_semester2, {force: true})
            cy.get(startAcadYear).should('be.visible')
                .select(this.data.cec_building_start_academic2, {force: true})
            cy.get(endSemester).should('be.visible')
                .select(this.data.cec_building_end_semester3, {force: true})
            cy.get(endAcadYear).should('be.visible')
                .select(this.data.cec_building_end_academic3, {force: true})
            cy.get(communityPartner).should('be.visible')
                .select(this.data.community_partner5, {force: true})
            cy.get(campusPartner).should('be.visible')
                .select(this.data.campus_partner13, {force: true})

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Data cleanup', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('CEC Building Partner Active Year').click()
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
