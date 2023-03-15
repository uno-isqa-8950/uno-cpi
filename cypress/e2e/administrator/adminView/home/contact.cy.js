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


describe("List contacts", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
        })
    })

    const adminHref = `a[href="/admin"]`,
        administratorLink = `a[class="nav-link dropdown-toggle"]`,
        adminTable = '#content-main',
        contactColumn = '.model-contact > th > a',
        addAdminContact = `a[href="/admin/home/contact/add/"]`,
        changeAdminContact = ':nth-child(1) > .field-first_name > a',
        first_name = 'input[name="first_name"]',
        last_name = 'input[name="last_name"]',
        work_phone = 'input[name="work_phone"]',
        cell_phone = 'input[name="cell_phone"]',
        email = 'input[name="email_id"]',
        contact_type = 'select[name="contact_type"]',
        community_partner = 'select[name="community_partner"]',
        campus_partner = 'select[name="campus_partner"]',
        form = 'form',
        continue_button = 'input[name="_continue"]',
        add_another = 'input[name="_addanother"]',
        searhbar = '#searchbar',
        searh_button = '#changelist-search > div > [type="submit"]'


    it('Can navigate to admin view', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()
    })

    it('Can search for a contact', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(contactColumn).contains('Contacts').click()
            cy.get(searhbar).type(this.data.contact_search)
            cy.get(searh_button).click().should('be.visible')
        })
    })


    it('Can add a new contact', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(contactColumn)
                .get(addAdminContact).click()
                .url().should('include', '/admin/home/contact/')

            cy.get(first_name).type(this.data.contact_first_name1)
                .should('be.empty').and('be.visible')
            cy.get(last_name).type(this.data.contact_last_name1)
                .should('be.empty').and('be.visible')
            cy.get(work_phone).type(this.data.contact_work_phone1)
                .should('be.empty').and('be.visible')
            cy.get(cell_phone).type(this.data.contact_cell_phone1)
                .should('be.empty').and('be.visible')
            cy.get(email).type(this.data.contact_email1)
                .should('be.empty').and('be.visible')
            cy.get(contact_type).should('be.visible').select(this.data.contact_type1, {force: true})
            cy.get(community_partner).should('be.visible')
                .select(this.data.contact_community_partner1, {force: true})
            cy.get(campus_partner).should('be.visible')
                .select(this.data.contact_campus_partner1, {force: true})
            cy.get(form).submit().should('be.visible')

        })
    })

    it('Can change a contact', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(contactColumn).contains('Contacts').click()
            cy.get(changeAdminContact).click()

            cy.get(campus_partner).should('be.visible')
                .select(this.data.contact_campus_partner1, {force: true})
            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a contact, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(contactColumn).contains('Contacts').click()
            cy.get(changeAdminContact).click()

            cy.get(contact_type).should('be.visible').select(this.data.contact_type2, {force: true})
            cy.get(community_partner).should('be.visible')
                .select(this.data.contact_community_partner1, {force: true})

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change a contact, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(contactColumn).contains('Contacts').click()
            cy.get(changeAdminContact).click()

            cy.get(campus_partner).should('be.visible')
                .select(this.data.contact_campus_partner1, {force: true})

            cy.get(add_another).click()

            cy.get(first_name).type(this.data.contact_first_name2)
                .should('be.empty').and('be.visible')
            cy.get(last_name).type(this.data.contact_last_name2)
                .should('be.empty').and('be.visible')
            cy.get(work_phone).type(this.data.contact_work_phone2)
                .should('be.empty').and('be.visible')
            cy.get(cell_phone).type(this.data.contact_cell_phone2)
                .should('be.empty').and('be.visible')
            cy.get(email).type(this.data.contact_email2)
                .should('be.empty').and('be.visible')
            cy.get(contact_type).should('be.visible').select(this.data.contact_type1, {force: true})
            cy.get(community_partner).should('be.visible')
                .select(this.data.contact_community_partner1, {force: true})
            cy.get(campus_partner).should('be.visible')
                .select(this.data.contact_campus_partner2, {force: true})
            cy.get(form).submit().should('be.visible')


        })
    })

    /*it('Can delete a contact', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(contactColumn).contains('Contacts').click()
            cy.get(changeAdminContact).click()

            cy.get(deleteAdminContact).click()

            cy.get(deleteContactButton).click().should('be.visible')
        })
    })

    it('Cannot delete a contact', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(contactColumn).contains('Contacts').click()
            cy.get(changeAdminContact).click()

            cy.get(deleteAdminContact).click()
            cy.get(noDelete).click().should('be.visible')
        })
    })

    it('Can delete a contact', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(contactColumn).contains('Contacts').click()
            cy.get(changeAdminContact).click()

            cy.get(deleteAdminContact).click()

            cy.get(deleteContactButton).click().should('be.visible')
        })
    })*/





})
