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


describe("List mission areas", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
        })
    })

    const adminHref = `a[href="/admin"]`,
        administratorLink = `a[class="nav-link dropdown-toggle"]`,
        adminTable = '#content-main',
        missionAreaColumn = '.model-missionarea > th > a',
        addMissionArea = `a[href="/admin/home/missionarea/add/"]`,
        changeMissionArea = ':nth-child(1) > .field-mission_name > a',
        mission_area_name = 'input[name="mission_name"]',
        description = 'textarea[name="description"]',
        image_url = 'input[name="mission_image_url"]',
        mission_color = 'input[name="mission_color"]',
        form = 'form',
        continue_button = 'input[name="_continue"]',
        add_another = 'input[name="_addanother"]',
        searhbar = '#searchbar',
        searh_button = '#changelist-search > div > [type="submit"]'


    it('Can navigate to admin view', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()
    })

    it('Can search for a mission area', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(missionAreaColumn).contains('Mission areas').click()
            cy.get(searhbar).type(this.data.contact_search)
            cy.get(searh_button).click().should('be.visible')
        })
    })


    it('Can add a new mission area', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(missionAreaColumn)
                .get(addMissionArea).click()
                .url().should('include', '/admin/home/missionarea/add/')

            cy.get(mission_area_name).type(this.data.mission_area_name1)
                .should('be.empty').and('be.visible')
            cy.get(description).type(this.data.mission_area_description1)
                .should('be.empty').and('be.visible')
            cy.get(image_url).type(this.data.mission_area_image1)
                .should('be.empty').and('be.visible')
            cy.get(mission_color).type(this.data.mission_area_color1)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')

        })
    })

    it('Can change a mission area', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(missionAreaColumn).contains('Mission areas').click()
            cy.get(changeMissionArea).click()

            cy.get(mission_area_name).clear()
            cy.get(mission_area_name).type(this.data.mission_area_name2)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a mission area, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(missionAreaColumn).contains('Mission areas').click()
            cy.get(changeMissionArea).click()

            cy.get(mission_color).clear()
            cy.get(mission_color).type(this.data.mission_area_color2)
                .should('be.empty').and('be.visible')

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change a mission area, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(missionAreaColumn).contains('Mission areas').click()
            cy.get(changeMissionArea).click()

            cy.get(mission_color).clear()
            cy.get(mission_color).type(this.data.mission_area_color2)
                .should('be.empty').and('be.visible')

            cy.get(add_another).click()

            cy.get(mission_area_name).type(this.data.mission_area_name2)
                .should('be.empty').and('be.visible')
            cy.get(description).type(this.data.mission_area_description2)
                .should('be.empty').and('be.visible')
            cy.get(image_url).type(this.data.mission_area_image2)
                .should('be.empty').and('be.visible')
            cy.get(mission_color).type(this.data.mission_area_color3)
                .should('be.empty').and('be.visible')

            cy.get(form).submit().should('be.visible')


        })
    })


})
