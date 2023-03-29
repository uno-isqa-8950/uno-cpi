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


describe("List community partners", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
        })
    })

    const adminHref = `a[href="/admin"]`,
        administratorLink = '[data-cy="administrator"]',
        adminTable = '#content-main',
        columnLink = '.model-communitypartner > th > a',
        add = `a[href="/admin/partners/communitypartner/add/"]`,
        change = ':nth-child(1) > .field-name > a',
        name = 'input[name="name"]',
        acronym = 'input[name="acronym"]',
        websiteUrl = 'input[name="website_url"]',
        communityType = 'select[name="community_type"]',
        k12Level = 'input[name="k12_level"]',
        address = 'input[name="address_line1"]',
        county = 'input[name="county"]',
        country = 'input[name="country"]',
        city = 'input[name="city"]',
        state = 'input[name="state"]',
        zip = 'input[name="zip"]',
        latitude = 'input[name="latitude"]',
        longitude = 'input[name="longitude"]',
        communityPartnerStatus = 'select[name="partner_status"]',
        legislativeDistrict = 'input[name="legislative_district"]',
        householdIncome = 'input[name="median_household_income"]',
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

    it('Can search for a community partner', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Community partners').click()
            cy.get(searhbar).type(this.data.community_partner_search)
            cy.get(searh_button).click().should('be.visible')
        })
    })


    it('Can add a new community partner', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink)
                .get(add).click()
                .url().should('include', '/admin/partners/communitypartner/add/')

            cy.get(name).type(this.data.community_partner_name1)
                .should('be.empty').and('be.visible')
            cy.get(acronym).type(this.data.community_partner_acronym1)
                .should('be.empty').and('be.visible')
            cy.get(websiteUrl).type(this.data.community_partner_website1)
                .should('be.empty').and('be.visible')
            cy.get(communityType).should('be.visible')
                .select(this.data.community_type1, {force: true})
            cy.get(k12Level).type(this.data.community_partner_level1)
                .should('be.empty').and('be.visible')
            cy.get(address).type(this.data.community_partner_address1)
                .should('be.empty').and('be.visible')
            cy.get(county).type(this.data.community_partner_county1)
                .should('be.empty').and('be.visible')
            cy.get(country).type(this.data.community_partner_country)
                .should('be.empty').and('be.visible')
            cy.get(city).type(this.data.community_partner_city1)
                .should('be.empty').and('be.visible')
            cy.get(state).type(this.data.community_partner_state1)
                .should('be.empty').and('be.visible')
            cy.get(zip).type(this.data.community_partner_zip1)
                .should('be.empty').and('be.visible')
            cy.get(latitude).type(this.data.community_partner_latitude1)
                .should('be.empty').and('be.visible')
            cy.get(longitude).type(this.data.community_partner_longitude1)
                .should('be.empty').and('be.visible')
            cy.get(communityPartnerStatus).should('be.visible')
                .select(this.data.campus_partner_status1, {force: true})
            cy.get(legislativeDistrict).type(this.data.community_partner_district1)
                .should('be.empty').and('be.visible')
            cy.get(householdIncome).type(this.data.community_partner_income1)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')

        })
    })

    it('Can change a community partner', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Community partners').click()
            cy.get(change).click()

            cy.get(k12Level).type(this.data.community_partner_level2)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a community partner, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Community partners').click()
            cy.get(change).click()

            cy.get(householdIncome).type(this.data.community_partner_income2)
                .should('be.empty').and('be.visible')

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change a community partner, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Community partners').click()
            cy.get(change).click()

            cy.get(communityPartnerStatus).should('be.visible')
                .select(this.data.campus_partner_status2, {force: true})

            cy.get(add_another).click()

            cy.get(name).type(this.data.community_partner_name2)
                .should('be.empty').and('be.visible')
            cy.get(acronym).type(this.data.community_partner_acronym2)
                .should('be.empty').and('be.visible')
            cy.get(websiteUrl).type(this.data.community_partner_website2)
                .should('be.empty').and('be.visible')
            cy.get(communityType).should('be.visible')
                .select(this.data.community_type2, {force: true})
            cy.get(k12Level).type(this.data.community_partner_level2)
                .should('be.empty').and('be.visible')
            cy.get(address).type(this.data.community_partner_address2)
                .should('be.empty').and('be.visible')
            cy.get(county).type(this.data.community_partner_county2)
                .should('be.empty').and('be.visible')
            cy.get(country).type(this.data.community_partner_country)
                .should('be.empty').and('be.visible')
            cy.get(city).type(this.data.community_partner_city2)
                .should('be.empty').and('be.visible')
            cy.get(state).type(this.data.community_partner_state2)
                .should('be.empty').and('be.visible')
            cy.get(zip).type(this.data.community_partner_zip2)
                .should('be.empty').and('be.visible')
            cy.get(latitude).type(this.data.community_partner_latitude2)
                .should('be.empty').and('be.visible')
            cy.get(longitude).type(this.data.community_partner_longitude2)
                .should('be.empty').and('be.visible')
            cy.get(communityPartnerStatus).should('be.visible')
                .select(this.data.campus_partner_status2, {force: true})
            cy.get(legislativeDistrict).type(this.data.community_partner_district2)
                .should('be.empty').and('be.visible')
            cy.get(householdIncome).type(this.data.community_partner_income3)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')


        })
    })

    it('Data cleanup', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Community partners').click()
            cy.get(searhbar).type(this.data.community_partner_name1)
            cy.get(searh_button).click().should('be.visible')
            cy.get(change).click()
        })

        cy.get(deleteLink).click()
        cy.get(deleteButton).click()

        cy.get(adminTable).within(() => {
            cy.get(searhbar).clear()
            cy.get(searhbar).type(this.data.community_partner_name2)
            cy.get(searh_button).click().should('be.visible')
            cy.get(change).click()
        })

        cy.get(deleteLink).click()
        cy.get(deleteButton).click()
        cy.get(searhbar).clear()
    })

})
