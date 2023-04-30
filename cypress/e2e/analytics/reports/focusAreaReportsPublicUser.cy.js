/// <reference types="cypress"/>
beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('reading \'style\''))
        {
            return false
        }
    })
    cy.visit(Cypress.env('baseUrl'))
})

describe('Focus Area Reports Public user', () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
        this.data = data
        })
    })
    //Check navigation
    it('Check navigation', function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
    })
    it('Check if it is Focus Area Report', function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get('[data-cy="heading"]').should('contain.text', 'Focus Areas Report')
    })
    // Hide Filters and Reset Filters
    it('Hide Filters', function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        //cy.get('[data-cy="hidefilterbtn"]').should('have.class', 'btn btn-primary')
        cy.get('[data-cy="hidefilterbtn"]').click()
        cy.get('.select2-selection__placeholder').should('not.be.visible')
        // check the filers are they visible
        cy.get('[data-cy="hidefilterbtn"]').click()
        //cy.get('[data-cy="hidefilterbtn"]').should('have.class', 'btn btn-primary')
        cy.get('.select2-selection__placeholder').should('be.visible')
        })
    it('Reset Filters', function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
        cy.get('[data-cy="id_academic_year"]').select(this.data.academic_year3,{force:true})
        cy.get('[data-cy="engagement-type-select"]').select(this.data.engagement_type3,{force:true})
        cy.get('[data-cy="id_academic_year"]').should('contain.text', this.data.academic_year3)
        cy.get('[data-cy="resetfilterbtn"]').click()
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
        })
    // Filter Options    
    it('filter options', function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get('[data-cy="id_academic_year"]').select(this.data.academic_year1,{force:true})
        cy.get('[data-cy="engagement-type-select"]').select(this.data.engagement_type1,{force:true})
        cy.get('[data-cy="community_type"]').select(this.data.community_type1,{force:true})
        cy.get('[data-cy="college_name"]').select(this.data.select_all,{force:true})
        cy.get('[data-cy="campus_partner"]').select(this.data.select_all,{force:true})
        cy.get('[data-cy="weitz_cec_part"]').select(this.data.cec_part1,{force:true})
        cy.get('[data-cy="applyfilters"]').click()
        cy.get('.buttons-csv').click()
        cy.get('.buttons-pdf').click()
    })
    // Check 7 focus area is listed
    it('Check if report contains all Focus Area Report', function () {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get(':nth-child(1) > [data-cy="mission-type"]').contains(this.data.focus_area1)
        cy.get(':nth-child(2) > [data-cy="mission-type"]').contains(this.data.focus_area2)
        cy.get(':nth-child(3) > [data-cy="mission-type"]').contains(this.data.focus_area3)
        cy.get(':nth-child(4) > [data-cy="mission-type"]').contains(this.data.focus_area4)
        cy.get(':nth-child(5) > [data-cy="mission-type"]').contains(this.data.focus_area5)
        cy.get(':nth-child(6) > [data-cy="mission-type"]').contains(this.data.focus_area6)
        cy.get(':nth-child(7) > [data-cy="mission-type"]').contains(this.data.focus_area7)
    })
    it("Check conectivity to Community Partners report", function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get('[data-cy="id_academic_year"]').select(this.data.select_all,{force:true})
        cy.get('[data-cy="applyfilters"]').click()
        cy.get('[data-cy="example"]').contains('td',this.data.focus_area1)
          .parent()
          .find('a[data-cy=community_count]').invoke('attr', 'target', '_self').click()
        cy.get('[data-cy="heading"]').should('contain.text', 'Community Partners Report')
        cy.url().should('contain', Cypress.env('baseUrl')+'community-public-report')
    })
    it("Check conectivity to Projects report", function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get('[data-cy="id_academic_year"]').select(this.data.select_all,{force:true})
        cy.get('[data-cy="applyfilters"]').click()
        cy.get('[data-cy="example"]').contains('td',this.data.focus_area1)
            .parent()
            .find('a[data-cy=project_count]').invoke('attr', 'target', '_self').click()
        cy.get('[data-cy="heading"]').should('contain.text', 'Projects Report')
        cy.url().should('contain', Cypress.env('baseUrl')+'projectspublicreport/')
    })
    it("Check tooltip text for 7 focus areas", function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        //focus area 1
        cy.get('[data-cy="example"]').contains('td',this.data.focus_area1)
            .parent().find('[data-cy="mission-type-tooltip"]').click()
        cy.contains('Projects and organizations that support the need for the improvement through Arts, Culture and Humanities.')
        //focus area 2
        cy.get('[data-cy="example"]').contains('td',this.data.focus_area2)
            .parent().find('[data-cy="mission-type-tooltip"]').click()
        cy.contains('Projects and organizations who address the causes, consequences, and solutions to poverty, with a special focus on meeting the economic needs of those affected by poverty.')
        //focus area 3
                cy.get('[data-cy="example"]').contains('td',this.data.focus_area3)
            .parent().find('[data-cy="mission-type-tooltip"]').click()
        cy.contains('Projects and organizations who support educational and learning needs, as well as inequalities within the community.')
        //focus area 4
        cy.get('[data-cy="example"]').contains('td',this.data.focus_area4)
            .parent().find('[data-cy="mission-type-tooltip"]').click()
        cy.contains('Projects and organizations that support the need for the improvement of our environment through sustainability and awareness.')
        //focus area 5
                cy.get('[data-cy="example"]').contains('td',this.data.focus_area5)
            .parent().find('[data-cy="mission-type-tooltip"]').click()
        cy.contains('Projects and organizations that support and bring awareness to the health and wellness needs of everyone, including specific health concerns of the ill, the aged, those with disabilities, and others in need while advocating for healthy lifestyles.')
        //focus area 6
                cy.get('[data-cy="example"]').contains('td',this.data.focus_area6)
            .parent().find('[data-cy="mission-type-tooltip"]').click()
        cy.contains('Projects and organizations that support international needs and concerns while devoting efforts to both local populations (refugees, immigrants, exchange students, etc.) and those engaged in international travel.')
        //focus area 7
        cy.get('[data-cy="example"]').contains('td',this.data.focus_area7)
            .parent().find('[data-cy="mission-type-tooltip"]').click()
        cy.contains('Projects and organizations that support inequality and corrupt social structures while devoting special efforts to meet the social needs of underprivileged populations.')  
    })
    it("Search in Focus Area Report", function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Focus Area').click()
        })
        cy.get('label > .form-control').type(this.data.focus_area3).click()
        cy.get('[data-cy="mission-type"]').should('contain', this.data.focus_area3)
    })
})