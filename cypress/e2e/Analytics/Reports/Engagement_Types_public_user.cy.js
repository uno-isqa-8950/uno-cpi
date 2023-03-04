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
describe('Analytic Reports Public user', () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
        this.data = data
        })
    })
    it('visits the form', function() {
        cy.visit(Cypress.env('baseUrl'))
    })
   //Check navigation
   it('Check navigation', function() {
    cy.contains('Analytics').click()
    cy.contains('Reports').next('.dropdown-menu').then($el => {
        cy.wrap($el).invoke('show')
        cy.wrap($el).contains('Engagement Types').click()
    })
    })
    it('Check if it is Engagement Type Report', function() {
        cy.contains('Analytics').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Type').click()
        })
        cy.get('.heading').should('contain.text', 'Engagement Types Report')
    })
    it('Hide Filters', function() {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Type').click()
        })
        cy.get('#hidefilterbtn').should('have.class', 'btn btn-secondary')
        cy.get('#hidefilterbtn').click()
        cy.get('.select2-selection__placeholder').should('not.be.visible')
        // check the filers are they visible
        cy.get('#hidefilterbtn').click()
        cy.get('#hidefilterbtn').should('have.class', 'btn btn-secondary')
        cy.get('.select2-selection__placeholder').should('be.visible')
        })
    it('Reset Filters', function() {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Type').click()
        })
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li) => {
            cy.wrap($li).contains(this.data.academic_year3).click();
        })
        cy.get('#select2-id_mission-container').click()
        cy.get('#select2-id_mission-results').then(($li) => {
            cy.wrap($li).contains(this.data.focus_area3).click();
        })
        cy.get('#select2-id_academic_year-container').should('contain.text', this.data.academic_year3)
        cy.get('#resetfilterbtn').click()
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
        })
    // Filter Options    
    it('filter options', function() {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Type').click()
        })
        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li) => {
            cy.wrap($li).contains(this.data.academic_year1).click();
        })
        cy.get('#select2-id_mission-container').click()
        cy.get('#select2-id_mission-results').then(($li) => {
            cy.wrap($li).contains(this.data.focus_area4).click();
        })
        cy.get('#select2-id_community_type-container').click()
        cy.get('#select2-id_community_type-results').then(($li) => {
            cy.wrap($li).contains(this.data.community_type2).click();
        })
        cy.get('#select2-id_college_name-container').click()
        cy.get('#select2-id_college_name-results').then(($li) => {
            cy.wrap($li).contains(this.data.college_name3).click();
        })
        cy.get('#select2-id_campus_partner-container').click()
        cy.get('#select2-id_campus_partner-results').then(($li) => {
            cy.wrap($li).contains(this.data.select_all).click();
        })
        cy.get('#select2-id_weitz_cec_part-container').click()
        cy.get('#select2-id_weitz_cec_part-results').then(($li) => {
            cy.wrap($li).contains(this.data.cec_part3).click();
        })
        cy.get('.buttons-csv').click()
        cy.get('.buttons-pdf').click()
    })
    it('Check if report contains all Engagement Type', function () {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Type').click()
        })
        cy.get(':nth-child(1) > .sorting_1').should('contain' ,this.data.engagement_type1)
        cy.get(':nth-child(2) > .sorting_1').should('contain' ,this.data.engagement_type2)
        cy.get(':nth-child(3) > .sorting_1').should('contain' ,this.data.engagement_type3)
        cy.get(':nth-child(4) > .sorting_1').should('contain' ,this.data.engagement_type4)
        cy.get(':nth-child(5) > .sorting_1').should('contain' ,this.data.engagement_type5)
        cy.get(':nth-child(6) > .sorting_1').should('contain' ,this.data.engagement_type6)
    })
    it("Check conectivity to Community Partners report", function() {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Type').click()
        })
        cy.get(':nth-child(1) > :nth-child(3) > .class1').invoke('attr', 'target', '_self').click()
        cy.get('.heading').should('contain.text', 'Community Partners Report')
        cy.url().should('contain', 'https://uno-cpi-dev.herokuapp.com/community-public-report')
    })
    it("Check conectivity to Projects report", function() {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Type').click()
        })
        cy.get(':nth-child(1) > :nth-child(2) > .class1').invoke('attr', 'target', '_self').click()
        cy.get('.heading').should('contain.text', 'Projects Report')
        cy.url().should('contain', 'https://uno-cpi-dev.herokuapp.com/projectspublicreport/')
    })
    it("Check tooltip text for 6 Engagement Type", function() {
        cy.get('#analyticnav').click()
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Type').click()
        })
        //Engagement Type 1
        cy.get(':nth-child(1) > .sorting_1 > span > .fa').trigger('mouseover').invoke('show')
        cy.contains('Participation in the governing body of a community partner.')
        //Engagement Type 2
        cy.get(':nth-child(2) > .sorting_1 > span > .fa').trigger('mouseover').invoke('show')
        cy.contains('Professional experiences that provide an opportunity to put academic knowledge in practice or learn more about a specific profession. During these experiences, it is expected that students gain intensive experience applying principles of civic and community engagement and disciplinary knowledge and skills in a community setting.')
        //Engagement Type 3
        cy.get(':nth-child(3) > .sorting_1 > span > .fa').trigger('mouseover').invoke('show')
        cy.contains('Engaged research (the scholarship of engagement), defined by the New England Resource Center for Higher Education (NERCHE) – A type of engagement that “redefines faculty scholarly work from application of academic expertise to community engaged scholarship that involves the faculty member in a reciprocal partnership with the community."')
        //Engagement Type 4
        cy.get(':nth-child(4) > .sorting_1 > span > .fa').trigger('mouseover').invoke('show')
        cy.contains('Refers to activities tailored to expand or transfer knowledge (e.g. access to higher education, presentations, workshops, etc.).')
        //Engagement Type 5
        cy.get(':nth-child(5) > .sorting_1 > span > .fa').trigger('mouseover').invoke('show')
        cy.contains('A method of teaching that combines classroom instruction with meaningful, community-identified service. This form of engaged teaching and learning emphasizes critical thinking by using reflection to connect course context with real-world experiences. Service learning instructors partner with community organizations as co-teachers and encourage a heightened sense of community, civic engagement, and personal responsibility for students while building capacity and contributing real community impact.')
        //Engagement Type 6
        cy.get(':nth-child(6) > .sorting_1 > span > .fa').trigger('mouseover').invoke('show')
        cy.contains('A non-curriculum, non-fee based community involvement that provides community or societal assistance, ultimately aiming towards community and societal improvement. Exemplary efforts may be recognized through scholarships, awards, recognition, and other rewards.')
    })
})