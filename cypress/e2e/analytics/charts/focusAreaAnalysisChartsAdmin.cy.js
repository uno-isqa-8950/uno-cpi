import user from "../../../support/commands";
describe('Charts Focus Area Analysis Admin User', () => {
beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
      {
        return false
      }
    })
    cy.fixture("datareports").then(function(data) {
      this.data = data
    })
    cy.loginAdminUser(user) // Admin User is logged in before the test begins
    cy.visit(Cypress.env('baseUrl'))
  })
  
  //Check navigation for Focus Area Analysis chart
  it('Check Navigation', function() {
    cy.get("[data-cy='analytics']").click().should('be.visible')
    cy.get("[data-cy='charts']").next("[data-cy='chartsdropdown']").then($el => {
      cy.wrap($el).invoke('show').should('be.visible')
      cy.wrap($el).get("[data-cy='Focus Area Analysis']").click()
    })
    cy.get("[data-cy='Focus Area Analysis']").should('contain.text', 'Focus Area Analysis')
  })
  //Hide Filters
  it('Hide Filters', function() {
    cy.get("[data-cy='analytics']").click().should('be.visible')
    cy.get("[data-cy='charts']").next("[data-cy='chartsdropdown']").then($el => {
      cy.wrap($el).invoke('show').should('be.visible')
      cy.wrap($el).get("[data-cy='Focus Area Analysis']").click()
    })
    cy.get('[data-cy="hide filters"]').should('have.value', 'Hide Filters')
    cy.get('[data-cy="hide filters"]').click()
    // check the filers are they visible
    cy.get('[data-cy="hide filters"]').click()
    cy.get('[data-cy="hide filters"]').should('have.value', 'Hide Filters')
    cy.get('.select2-selection__placeholder').should('be.visible')
  })

  //Reset Filters
  it('Reset Filters', function() {
    cy.get("[data-cy='analytics']").click().should('be.visible')
    cy.get("[data-cy='charts']").next("[data-cy='chartsdropdown']").then($el => {
      cy.wrap($el).invoke('show').should('be.visible')
      cy.wrap($el).get("[data-cy='Focus Area Analysis']").click()
    })
    cy.get('#select2-id_academicyear-container > .select2-selection__placeholder').contains('2020-21')
    cy.get('[data-cy="start_academicyear"]').select(this.data.academic_year1, {force:true})
    cy.get('#select2-id_academicyear-container').should('have.text', this.data.academic_year1)

    cy.get('#select2-id_endacademicyear-container > .select2-selection__placeholder').contains('2021-22')
    cy.get('[data-cy="end_academicyear"]').select(this.data.academic_year1, {force:true})
    cy.get('#select2-id_endacademicyear-container').should('have.text', this.data.academic_year1)

    cy.get('#select2-id_engagement_type-container > .select2-selection__placeholder').contains('All Engagement Types')
    cy.get('[data-cy="engagement_type"]').select(this.data.engagement_type3, {force:true})
    cy.get('#select2-id_engagement_type-container').should('have.text', this.data.engagement_type3)

    cy.get('#select2-id_community_type-container > .select2-selection__placeholder').contains('All Community Organization Types')
    cy.get('[data-cy="community_type"]').select(this.data.community_type1, {force:true})
    cy.get('#select2-id_community_type-container').should('have.text', this.data.community_type1)

    cy.get('[data-cy="reset filters"]').should('have.value', 'Reset Filters')
    cy.get('[data-cy="reset filters"]').click()
    // check the filers are they visible
    cy.get('[data-cy="reset filters"]').click()
    cy.get('[data-cy="reset filters"]').should('have.value', 'Reset Filters')
    cy.get('.select2-selection__placeholder').should('be.visible')
  })
  //Validate error pop up for filter options
  it('Alert for filter option', function() {
    cy.get("[data-cy='analytics']").click().should('be.visible')
    cy.get("[data-cy='charts']").next("[data-cy='chartsdropdown']").then($el => {
      cy.wrap($el).invoke('show').should('be.visible')
      cy.wrap($el).get("[data-cy='Focus Area Analysis']").click()
    })

    cy.get('#select2-id_campus_partner-container > .select2-selection__placeholder').contains('All Campus Partners')
    cy.get('[data-cy="campus_partner"]').select(this.data.campus_partner3, {force:true})
    cy.get('#select2-id_campus_partner-container').should('have.text', this.data.campus_partner3)

    cy.get('#select2-id_academicyear-container > .select2-selection__placeholder').contains('2020-21')
    cy.get('[data-cy="start_academicyear"]').select(this.data.academic_year1, {force:true})
    cy.get('#select2-id_academicyear-container').should('have.text', this.data.academic_year1)

    cy.get('#select2-id_endacademicyear-container > .select2-selection__placeholder').contains('2021-22')
    cy.get('[data-cy="end_academicyear"]').select(this.data.academic_year1, {force:true})
    cy.get('#select2-id_endacademicyear-container').should('have.text', this.data.academic_year1)

    cy.get('#select2-id_engagement_type-container > .select2-selection__placeholder').contains('All Engagement Types')
    cy.get('[data-cy="engagement_type"]').select(this.data.engagement_type3, {force:true})
    cy.get('#select2-id_engagement_type-container').should('have.text', this.data.engagement_type3)

    cy.get('#select2-id_college_name-container > .select2-selection__placeholder').contains('All College and Main Units')
    cy.get('[data-cy="college_name"]').select(this.data.college_name2, {force:true})
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('There are no projects associated with your selection criteria');
    })
  })
  //Filter options
  it('Analytic Charts Focus Area Analysis Admin User', function() {
    cy.get("[data-cy='analytics']").click().should('be.visible')
    cy.get("[data-cy='charts']").next("[data-cy='chartsdropdown']").then($el => {
      cy.wrap($el).invoke('show').should('be.visible')
      cy.wrap($el).get("[data-cy='Focus Area Analysis']").click()
    })

    cy.get('#select2-id_campus_partner-container > .select2-selection__placeholder').contains('All Campus Partners')
    cy.get('[data-cy="campus_partner"]').select(this.data.campus_partner3,{force:true})
    cy.get('#select2-id_campus_partner-container').should('have.text' ,this.data.campus_partner3)

    cy.get('#select2-id_academicyear-container > .select2-selection__placeholder').contains('2020-21')
    cy.get('[data-cy="start_academicyear"]').select(this.data.academic_year1,{force:true})
    cy.get('#select2-id_academicyear-container').should('have.text' ,this.data.academic_year1)

    cy.get('#select2-id_endacademicyear-container > .select2-selection__placeholder').contains('2021-22')
    cy.get('[data-cy="end_academicyear"]').select(this.data.academic_year1, {force:true})
    cy.get('#select2-id_endacademicyear-container').should('have.text', this.data.academic_year1)

    cy.get('#select2-id_engagement_type-container > .select2-selection__placeholder').contains('All Engagement Types')
    cy.get('[data-cy="engagement_type"]').select(this.data.engagement_type3,{force:true})
    cy.get('#select2-id_engagement_type-container').should('have.text' ,this.data.engagement_type3)

    cy.get('#select2-id_college_name-container > .select2-selection__placeholder').contains('All College and Main Units')
    cy.get('[data-cy="college_name"]').select(this.data.college_name1,{force:true})
    cy.get('#select2-id_college_name-container').should('have.text' ,this.data.college_name1)

    cy.get('#select2-id_weitz_cec_part-container > .select2-selection__placeholder').contains('All (CEC/Non-CEC Partners)')
    cy.get('[data-cy="weitz_cec_part"]').select(this.data.cec_part4,{force:true})
    // cy.get('#select2-id_weitz_cec_partr-container').should('have.text' ,this.data.cec_part4)

    cy.get('#select2-id_community_type-container > .select2-selection__placeholder').contains('All Community Organization Types')
    cy.get('[data-cy="community_type"]').select(this.data.community_type5,{force:true})
    cy.get('#select2-id_community_type-container').should('have.text' ,this.data.community_type5)

    cy.get('#select2-id_legislative_value-container > .select2-selection__placeholder').contains('All Legislative Districts')
    cy.get('[data-cy="legislative_value"]').select(this.data.legislative_dist9,{force:true})
    cy.get('#select2-id_legislative_value-container').should('have.text' ,this.data.legislative_dist9)

    cy.get('.highcharts-root').should('be.visible').and(chart => {
      expect(chart.height()).to.be.greaterThan(200)
    })
    cy.get('.highcharts-yaxis').contains('Focus Area')
    cy.get('.highcharts-xaxis').contains('Projects')
    cy.get('.highcharts-yaxis-labels').filter(':contains("Arts, Culture and Humanities")').should('exist')
    cy.get('.highcharts-yaxis-labels').filter(':contains("Economic Impact")').should('exist')
    cy.get('.highcharts-yaxis-labels').filter(':contains("Educational Support")').should('exist')
    cy.get('.highcharts-yaxis-labels').filter(':contains("Environmental Stewardship")').should('exist')
    cy.get('.highcharts-yaxis-labels').filter(':contains("Health and Wellness")').should('exist')
    cy.get('.highcharts-yaxis-labels').filter(':contains("International Service")').should('exist')
    cy.get('.highcharts-yaxis-labels').filter(':contains("Social Justice")').should('exist')
  })

  it('Chart legends', function () {
    cy.get("[data-cy='analytics']").click()
    cy.get("[data-cy='charts']").next("[data-cy='chartsdropdown']").then($el => {
      cy.wrap($el).invoke('show')
      cy.wrap($el).get("[data-cy='Focus Area Analysis']").click()
    })

    cy.get('.highcharts-series-1 > text').contains("Analysis Start Year").should("be.visible")
    cy.get('.highcharts-series-1 > path').should('have.attr', 'fill', 'teal')
    cy.get('.highcharts-series-2 > text').contains("Analysis Comparison (End) Year").should("be.visible")
    cy.get('.highcharts-series-2 > path').should('have.attr', 'fill', 'blue')
    cy.get('.highcharts-series-3 > text').contains("Increase In Projects").should("be.visible")
    cy.get('.highcharts-series-3 > path').should('have.attr', 'fill', 'none')
    cy.get('.highcharts-series-4 > text').contains("Decrease In Projects").should("be.visible")
    cy.get('.highcharts-series-4 > path').should('have.attr', 'fill', 'none')
  })


})