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
describe('Projects Reports Public user', () => {
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
    cy.get('[data-cy="analytics"]').click()
    cy.get('[data-cy="reports"]').next('[data-cy="reportsdropdown"]').then($el => {
        cy.wrap($el).invoke('show')
        cy.wrap($el).get('[data-cy="projectsreport"]').click()
    })
    })
    it('Check if it is Projects Report', function() {
        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="reports"]').next('[data-cy="reportsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).get('[data-cy="projectsreport"]').click()
        })
        cy.get('[data-cy="heading"]').should('contain.text', 'Projects Report')
    })
    it('Hide Filters', function() {
        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="reports"]').next('[data-cy="reportsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).get('[data-cy="projectsreport"]').click()
        })
        cy.get('[data-cy="Hide Filters"]').should('have.class', 'btn btn-secondary')
        cy.get('[data-cy="Hide Filters"]').click() 
        cy.get('[data-cy="collapse show"]').should('not.be.visible')
        // check the filers are they visible
        cy.get('[data-cy="Hide Filters"]').click() 
        cy.get('[data-cy="Hide Filters"]').click() .should('have.class', 'btn btn-secondary')
        cy.get('[data-cy="collapse show"]').should('be.visible')
        })
    it('Reset Filters', function() {
        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="reports"]').next('[data-cy="reportsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).get('[data-cy="projectsreport"]').click()
        })
        cy.get('[data-cy="academic-year"]').contains('Previous Academic Year')
        cy.get('[data-cy="academic_year"]').select(this.data.academic_year1,{force:true})
        cy.get('[data-cy="id_community_type"]').select(this.data.community_type3,{force:true})
        cy.get('[data-cy="academic_year"]').should('contain.text', this.data.academic_year1)
        cy.get('[data-cy="Reset Filters"]').click()
        cy.get('[data-cy="academic-year"]').contains('Previous Academic Year')
        })
    // Filter Options
    it('filter options', function() {
        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="reports"]').next('[data-cy="reportsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).get('[data-cy="projectsreport"]').click()
        })
        cy.get('[data-cy="academic-year"]').contains('Previous Academic Year')
        cy.get('[data-cy="academic_year"]').select(this.data.academic_year4,{force:true})
        cy.get('[data-cy="mission"]').select(this.data.focus_area4,{force:true})
        cy.get('[data-cy="engagement-type"]').select(this.data.engagement_type2,{force:true})
        cy.get('[data-cy="id_community_type"]').select(this.data.community_type5,{force:true})
        cy.get('[data-cy="college-name"]').select(this.data.college_name1,{force:true})
        cy.get('[data-cy="id_campus_partner"]').select(this.data.select_all,{force:true})
        cy.get('[data-cy="weitz_cec_part"]').select(this.data.cec_part4,{force:true})
        cy.get('[data-cy="applyfilters"]').click()
    })

    it("Check Card View", function()
    {
        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="reports"]').next('[data-cy="reportsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).get('[data-cy="projectsreport"]').click({force: true})
        })
        cy.get('[data-cy="academic_year"]').select(this.data.academic_year1,{force:true})
        cy.get('[data-cy="mission"]').select(this.data.focus_area4,{force:true})
        cy.get('[data-cy="engagement-type"]').select(this.data.select_all,{force:true})
        cy.get('[data-cy="id_campus_partner"]').select(this.data.campus_partner3,{force:true})
        cy.get('[data-cy="applyfilters"]').click()
        //verify if they are present in card structure
        cy.get('[data-cy="mission"]').contains(this.data.focus_area4).should("be.visible")
        cy.get('[data-cy="academic_year"]').contains(this.data.academic_year1).should("be.visible")
        cy.get('[data-cy="id_community_type"]').contains(this.data.select_all).should("be.visible")
        cy.get('[data-cy="id_campus_partner"]').contains(this.data.campus_partner3).should("be.visible")
        //cy.get('div [class="col-md-6 col-lg-6 col-sm-12"] > .ul').children().contains(this.data.campus_partner3).should("be.visible")
        //cy.get('div[class="col-sm-12 col-lg-6"]').contains("Engagement Types:").should("be.visible")
    })
    it("Check Table view", function()
    {
        cy.get('[data-cy="analytics"]').click()
        cy.get('[data-cy="reports"]').next('[data-cy="reportsdropdown"]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).get('[data-cy="projectsreport"]').click()
        })
        cy.get('[data-cy="academic_year"]').select(this.data.academic_year1,{force:true})
        cy.get('[data-cy="mission"]').select(this.data.select_all,{force:true})
        cy.get('[data-cy="engagement-type"]').select(this.data.engagement_type2,{force:true})
        cy.get('[data-cy="applyfilters"]').click()
        cy.wait(1000)
        cy.get('[data-cy="Table View"]').click({force:true})
        cy.wait(1000)
        cy.url().should('contain', Cypress.env('baseUrl')+'projectspublictableview')
        cy.get('[data-cy="box"]').get('.buttons-csv').should("be.visible").click()
        cy.get('[data-cy="box"]').get('.buttons-pdf').should("be.visible").click()
        cy.get(':nth-child(1) > .sorting_1').click()
        cy.get('[data-dtr-index="8"]').contains(this.data.academic_year1)
        cy.get('[data-dtr-index="4"]').contains(this.data.engagement_type2)
        cy.get('#btn-table').click()
      })
})