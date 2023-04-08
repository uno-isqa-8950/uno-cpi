import user from "../../../support/commands"
beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })
    cy.visit(Cypress.env('baseUrl'))})


describe("List and sort campus partner organizations", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
            cy.get('#login').click().loginAdminUser(user)
        })
    })

    const organizationsHref = `a[href="/partners/profile/orgprofile/"]`,
        administratorLink = `a[class="nav-link dropdown-toggle"]`,
        navbar ='.navbar',
        tableHeading = '#example thead th',
        table = '#example',
        tableRow = '[role=row]',
        tableColumn = 'thead tr',
        tableCell = 'td',
        adminTable = '#content-main',
        joinButton = `a[href="/partners/orgprofile/partner_add/"]`,
        addCampusPartner = `a[href="/admin/partners/communitypartner/add/"]`,
        communityPartnerColumn = '.model-communitypartner',
        name = 'input[name="name"]',
        acronym = 'input[name="acronym"]',
        website_url = 'input[name="website_url"]',
        community_type = 'select[name="community_type"]',
        k12_level = 'input[name="k12_level"]',
        address_line1 = 'input[name="address_line1"]',
        county = 'input[name="county"]',
        country = 'input[name="country"]',
        city = 'input[name="city"]',
        state = 'input[name="state"]',
        zip = 'input[name="zip"]',
        active = 'input[name="active"]',
        partner_status = 'select[name="partner_status"]',
        form = 'form',
        searhbar = '#searchbar',
        searh_button = '#changelist-search > div > [type="submit"]',
        changeOrganization = ':nth-child(1) > .field-name > a',
        deleteOrganizationButton = 'div > [type="submit"]',
        deleteOrganization = '.deletelink'


    const tableHeader = [
        'Organization Name',
        'College Name'
    ]

    it('Can navigate to organization details', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(organizationsHref).click()
            .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/partners/profile/orgprofile/')
        cy.get(navbar).should('exist')
    })

    it('Verifies table headers loads', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(organizationsHref).click()
            .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/partners/profile/orgprofile/')
        cy.get(navbar).should('exist')

        cy.get(tableHeading).each(($el, index) => {
            cy.wrap($el).contains(tableHeader[index]).should('be.visible')
        })
    })

    it('Verifies table data loads and sorts ascending', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(organizationsHref).click()
            .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/partners/profile/orgprofile/')
        cy.get(navbar).should('exist')

        cy.get(table).within(() => {
            cy.get(tableRow).should('have.length', 1553)
            cy.get(tableColumn).contains('.sorting_asc', tableHeader[0]).should('be.visible')
        })
    })


    it('Verifies table data loads and sorts descending', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(organizationsHref).click()
            .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/partners/profile/orgprofile/')
        cy.get(navbar).should('exist')

        cy.get(table).within(() => {
            cy.get(tableRow).should('have.length', 1553)
            cy.get(tableColumn).contains('.sorting_asc', tableHeader[0]).should('be.visible').click()
        })
    })

    it('Verifies text in a cell exists', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(organizationsHref).click()
            .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/partners/profile/orgprofile/')
        cy.get(navbar).should('exist')

        cy.get(table).contains(tableCell, this.data.organization_name_test).should('exist')

    })


    it('Join campus partners', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(organizationsHref).click()
            .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/partners/profile/orgprofile/')
        cy.get(navbar).should('exist')

        cy.get(joinButton).click()
            .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/admin/')

        cy.get(adminTable).within(() => {
            cy.get(communityPartnerColumn)
                .get(addCampusPartner).click()
                .url().should('include', '/admin/partners/communitypartner/')

            cy.get(name).type(this.data.organization_name)
                .should('be.empty').and('be.visible')
            cy.get(acronym).type(this.data.organization_acronym)
                .should('be.empty').and('be.visible')
            cy.get(website_url).type(this.data.organization_website_url)
                .should('be.empty').and('be.visible')
            cy.get(community_type).should('be.visible')
                .select(this.data.organization_community_type, {force: true})
            cy.get(k12_level).type(this.data.organization_k12_level)
                .should('be.empty').and('be.visible')
            cy.get(address_line1).type(this.data.organization_address_line1)
                .should('be.empty').and('be.visible')
            cy.get(county).type(this.data.organization_county)
                .should('be.empty').and('be.visible')
            cy.get(country).type(this.data.organization_country)
                .should('be.empty').and('be.visible')
            cy.get(city).type(this.data.organization_city)
                .should('be.empty').and('be.visible')
            cy.get(state).type(this.data.organization_state)
                .should('be.empty').and('be.visible')
            cy.get(zip).type(this.data.organization_zip)
                .should('be.empty').and('be.visible')
            cy.get(active).check().should('be.visible')
            cy.get(partner_status).should('be.visible')
                .select(this.data.organization_partner_status, {force: true})
            cy.get(form).submit().should('be.visible')

            cy.get(searhbar).type(this.data.organization_name)
            cy.get(searh_button).click().should('be.visible')
        })
    })

    it('Data cleanup', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(communityPartnerColumn).contains('Community partners').click()
            cy.get(searhbar).type(this.data.organization_name)
            cy.get(searh_button).click().should('be.visible')
            cy.get(changeOrganization).click()
        })

        cy.get(deleteOrganization).click()
        cy.get(deleteOrganizationButton).click()
    })
})
