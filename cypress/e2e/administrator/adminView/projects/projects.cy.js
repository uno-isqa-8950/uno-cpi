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


describe("List projects", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
            cy.get('#login').click().loginAdminUser(user)
        })
    })

    const adminHref = `a[href="/admin"]`,
        administratorLink = '[data-cy="administrator"]',
        adminTable = '#content-main',
        columnLink = '.model-project > th > a',
        add = `a[href="/admin/projects/project/add/"]`,
        change = ':nth-child(1) > .field-project_name > a',
        projectName = 'input[name="project_name"]',
        engagementType = 'select[name="engagement_type"]',
        activityType = 'select[name="activity_type"]',
        facilitator = 'input[name="facilitator"]',
        description = 'textarea[name="description"]',
        semester = 'input[name="semester"]',
        endSemester = 'input[name="end_semester"]',
        academicYear = 'select[name="academic_year"]',
        endAcademicYear = 'select[name="end_academic_year"]',
        totalUnoStudents = 'input[name="total_uno_students"]',
        totalUnoHours = 'input[name="total_uno_hours"]',
        totalK12Students = 'input[name="total_k12_students"]',
        totalK12Hours = 'input[name="total_k12_hours"]',
        totalUnoFaculty = 'input[name="total_uno_faculty"]',
        otherTotal = 'input[name="total_other_community_members"]',
        startDate = 'input[name="start_date"]',
        endDate = 'input[name="end_date"]',
        address = 'input[name="address_line1"]',
        country = 'input[name="country"]',
        city = 'input[name="city"]',
        state = 'input[name="state"]',
        zip = 'input[name="zip"]',
        county = 'input[name="county"]',
        legislativeDistrict = 'input[name="legislative_district"]',
        householdIncome = 'input[name="median_household_income"]',
        latitude = 'input[name="latitude"]',
        longitude = 'input[name="longitude"]',
        createdBy = 'select[name="created_by"]',
        updatedBy = 'select[name="updated_by"]',
        subcategory = 'select[name="subcategory"]',
        missionArea = 'select[name="mission_area"]',
        communityPartner = 'select[name="community_partner"]',
        campusPartner = 'select[name="campus_partner"]',
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

    it('Can search for a project', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Projects').click()
            cy.get(searhbar).type(this.data.project_search)
            cy.get(searh_button).click().should('be.visible')
        })
    })


    it('Can add a new project', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink)
                .get(add).click()
                .url().should('include', '/admin/projects/project/add/')

            cy.get(projectName).type(this.data.project_name01)
                .should('be.empty').and('be.visible')
            cy.get(engagementType).should('be.visible')
                .select(this.data.engagement_type3, {force: true})
            cy.get(activityType).should('be.visible')
                .select(this.data.activity_name1, {force: true})
            cy.get(facilitator).type(this.data.facilitator1)
                .should('be.empty').and('be.visible')
            cy.get(description).type(this.data.description1)
                .should('be.empty').and('be.visible')
            cy.get(semester).type(this.data.semester1)
                .should('be.empty').and('be.visible')
            cy.get(endSemester).type(this.data.semester2)
                .should('be.empty').and('be.visible')
            cy.get(academicYear).should('be.visible')
                .select(this.data.academic_year1, {force: true})
            cy.get(endAcademicYear).should('be.visible')
                .select(this.data.academic_year4, {force: true})
            cy.get(totalUnoStudents).clear()
            cy.get(totalUnoStudents).type(this.data.total_uno_students1)
                .should('be.empty').and('be.visible')
            cy.get(totalUnoHours).clear()
            cy.get(totalUnoHours).type(this.data.total_uno_hours1)
                .should('be.empty').and('be.visible')
            cy.get(totalK12Students).clear()
            cy.get(totalK12Students).type(this.data.total_k12_students1)
                .should('be.empty').and('be.visible')
            cy.get(totalK12Hours).clear()
            cy.get(totalK12Hours).type(this.data.total_k12_hours1)
                .should('be.empty').and('be.visible')
            cy.get(totalUnoFaculty).clear()
            cy.get(totalUnoFaculty).type(this.data.total_uno_faculty1)
                .should('be.empty').and('be.visible')
            cy.get(otherTotal).clear()
            cy.get(otherTotal).type(this.data.other_total1)
                .should('be.empty').and('be.visible')
            cy.get(startDate).type(this.data.project_start_date1)
                .should('be.empty').and('be.visible')
            cy.get(endDate).type(this.data.project_end_date1)
                .should('be.empty').and('be.visible')
            cy.get(address).type(this.data.project_address1)
                .should('be.empty').and('be.visible')
            cy.get(country).type(this.data.community_partner_country)
                .should('be.empty').and('be.visible')
            cy.get(city).type(this.data.project_city1)
                .should('be.empty').and('be.visible')
            cy.get(state).type(this.data.project_state1)
                .should('be.empty').and('be.visible')
            cy.get(zip).type(this.data.project_zip1)
                .should('be.empty').and('be.visible')
            cy.get(county).type(this.data.project_county1)
                .should('be.empty').and('be.visible')
            cy.get(legislativeDistrict).type(this.data.project_legislative_district1)
                .should('be.empty').and('be.visible')
            cy.get(householdIncome).type(this.data.project_household_income1)
                .should('be.empty').and('be.visible')
            cy.get(latitude).type(this.data.project_latitude1)
                .should('be.empty').and('be.visible')
            cy.get(longitude).type(this.data.project_longitude1)
                .should('be.empty').and('be.visible')
            cy.get(createdBy).should('be.visible')
                .select(this.data.project_created_by1, {force: true})
            cy.get(updatedBy).should('be.visible')
                .select(this.data.project_updated_by1, {force: true})
            cy.get(subcategory).should('be.visible')
                .select(this.data.mission_subcategory1, {force: true})
            cy.get(missionArea).should('be.visible')
                .select(this.data.mission_area1, {force: true})
            cy.get(communityPartner).should('be.visible')
                .select(this.data.community_partner4, {force: true})
            cy.get(campusPartner).should('be.visible')
                .select(this.data.campus_partner1, {force: true})

            cy.get(form).submit().should('be.visible')

        })
    })

    it('Can change a project', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Projects').click()
            cy.get(change).click()

            cy.get(createdBy).should('be.visible')
                .select(this.data.project_created_by2, {force: true})

            cy.get(form).submit().should('be.visible')
        })
    })

    it('Can change a project, save and continue editing', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Projects').click()
            cy.get(change).click()

            cy.get(updatedBy).should('be.visible')
                .select(this.data.project_updated_by2, {force: true})

            cy.get(continue_button).click().should('be.visible')
        })
    })

    it('Can change a project, save and add another one', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Projects').click()
            cy.get(change).click()

            cy.get(engagementType).should('be.visible')
                .select(this.data.engagement_type1, {force: true})

            cy.get(add_another).click()

            cy.get(projectName).type(this.data.project_name02)
                .should('be.empty').and('be.visible')
            cy.get(engagementType).should('be.visible')
                .select(this.data.engagement_type4, {force: true})
            cy.get(activityType).should('be.visible')
                .select(this.data.activity_name2, {force: true})
            cy.get(facilitator).type(this.data.facilitator2)
                .should('be.empty').and('be.visible')
            cy.get(description).type(this.data.description2)
                .should('be.empty').and('be.visible')
            cy.get(semester).type(this.data.semester2)
                .should('be.empty').and('be.visible')
            cy.get(endSemester).type(this.data.semester2)
                .should('be.empty').and('be.visible')
            cy.get(academicYear).should('be.visible')
                .select(this.data.academic_year2, {force: true})
            cy.get(endAcademicYear).should('be.visible')
                .select(this.data.academic_year4, {force: true})
            cy.get(totalUnoStudents).clear()
            cy.get(totalUnoStudents).type(this.data.total_uno_students2)
                .should('be.empty').and('be.visible')
            cy.get(totalUnoHours).clear()
            cy.get(totalUnoHours).type(this.data.total_uno_hours2)
                .should('be.empty').and('be.visible')
            cy.get(totalK12Students).clear()
            cy.get(totalK12Students).type(this.data.total_k12_students2)
                .should('be.empty').and('be.visible')
            cy.get(totalK12Hours).clear()
            cy.get(totalK12Hours).type(this.data.total_k12_hours2)
                .should('be.empty').and('be.visible')
            cy.get(totalUnoFaculty).clear()
            cy.get(totalUnoFaculty).type(this.data.total_uno_faculty2)
                .should('be.empty').and('be.visible')
            cy.get(otherTotal).clear()
            cy.get(otherTotal).type(this.data.other_total2)
                .should('be.empty').and('be.visible')
            cy.get(startDate).type(this.data.project_start_date2)
                .should('be.empty').and('be.visible')
            cy.get(endDate).type(this.data.project_end_date2)
                .should('be.empty').and('be.visible')
            cy.get(address).type(this.data.project_address2)
                .should('be.empty').and('be.visible')
            cy.get(country).type(this.data.community_partner_country)
                .should('be.empty').and('be.visible')
            cy.get(city).type(this.data.project_city2)
                .should('be.empty').and('be.visible')
            cy.get(state).type(this.data.project_state2)
                .should('be.empty').and('be.visible')
            cy.get(zip).type(this.data.project_zip2)
                .should('be.empty').and('be.visible')
            cy.get(county).type(this.data.project_county2)
                .should('be.empty').and('be.visible')
            cy.get(legislativeDistrict).type(this.data.project_legislative_district2)
                .should('be.empty').and('be.visible')
            cy.get(householdIncome).type(this.data.project_household_income2)
                .should('be.empty').and('be.visible')
            cy.get(latitude).type(this.data.project_latitude2)
                .should('be.empty').and('be.visible')
            cy.get(longitude).type(this.data.project_longitude2)
                .should('be.empty').and('be.visible')
            cy.get(createdBy).should('be.visible')
                .select(this.data.project_created_by3, {force: true})
            cy.get(updatedBy).should('be.visible')
                .select(this.data.project_updated_by3, {force: true})
            cy.get(subcategory).should('be.visible')
                .select(this.data.mission_subcategory2, {force: true})
            cy.get(missionArea).should('be.visible')
                .select(this.data.mission_area2, {force: true})
            cy.get(communityPartner).should('be.visible')
                .select(this.data.community_partner5, {force: true})
            cy.get(campusPartner).should('be.visible')
                .select(this.data.campus_partner2, {force: true})

            cy.get(form).submit().should('be.visible')


        })
    })

    it('Data cleanup', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(adminHref).invoke('removeAttr', 'target').click()

        cy.get(adminTable).within(() => {
            cy.get(columnLink).contains('Projects').click()
            cy.get(searhbar).type(this.data.project_name01)
            cy.get(searh_button).click().should('be.visible')
            cy.get(change).click()
        })

        cy.get(deleteLink).click()
        cy.get(deleteButton).click()

        cy.get(adminTable).within(() => {
            cy.get(searhbar).clear()
            cy.get(searhbar).type(this.data.project_name02)
            cy.get(searh_button).click().should('be.visible')
            cy.get(change).click()
        })

        cy.get(deleteLink).click()
        cy.get(deleteButton).click()
    })

})
