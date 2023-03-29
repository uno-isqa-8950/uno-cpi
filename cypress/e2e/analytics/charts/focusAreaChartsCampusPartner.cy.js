import user from "../../../support/commands";

beforeEach(() => {
  cy.on('uncaught:exception', (err, runnable) => {
    if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
    {
      return false
    }
  })
  cy.visit(Cypress.env('baseUrl'))
})

describe('Charts Focus Area Campus Partner User', () => {
  beforeEach(function() {
    cy.fixture("datareports").then(function(data) {
      this.data = data
      cy.get('#login').click()
      cy.loginCampusUser(user)
    })
  })

  it('visits the site', function() {
    cy.visit(Cypress.env('baseUrl'))
  })
  //Check navigation for Focus Area chart
  it('Check Navigation', function() {
    cy.get("[data-cy='analytics']").click().should('be.visible')
    cy.get("[data-cy='charts']").next("[data-cy='chartsdropdown']").then($el => {
      cy.wrap($el).invoke('show').should('be.visible')
      cy.wrap($el).get("[data-cy='Focus Areas']").click()
    })
    cy.get("[data-cy='Focus Areas']").should('contain.text', 'Focus Areas')
  })
  //Hide Filters
  it('Hide Filters', function() {
    cy.get("[data-cy='analytics']").click().should('be.visible')
    cy.get("[data-cy='charts']").next("[data-cy='chartsdropdown']").then($el => {
      cy.wrap($el).invoke('show').should('be.visible')
      cy.wrap($el).get("[data-cy='Focus Areas']").click()
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
      cy.wrap($el).get("[data-cy='Focus Areas']").click()
    })
    cy.get('#select2-id_academicyear-container > .select2-selection__placeholder').contains('Previous Academic Year')
    cy.get('[data-cy="academic_year"]').select(this.data.academic_year1, {force: true})
    cy.get('#select2-id_academicyear-container').should('have.text', this.data.academic_year1)

    cy.get('#select2-id_engagement_type-container > .select2-selection__placeholder').contains('All Engagement Types')
    cy.get('[data-cy="engagement_type"]').select(this.data.engagement_type3, {force: true})
    cy.get('#select2-id_engagement_type-container').should('have.text', this.data.engagement_type3)

    cy.get('#select2-id_community_type-container > .select2-selection__placeholder').contains('All Community Organization Types')
    cy.get('[data-cy="community_type"]').select(this.data.community_type1, {force: true})
    cy.get('#select2-id_community_type-container').should('have.text', this.data.community_type1)

    cy.get('[data-cy="reset filters"]').should('have.value', 'Reset Filters')
    cy.get('[data-cy="reset filters"]').click()
    // check the filers are they visible
    cy.get('[data-cy="reset filters"]').click()
    cy.get('[data-cy="reset filters"]').should('have.value', 'Reset Filters')
    cy.get('.select2-selection__placeholder').should('be.visible')
  })

  //Filter options
  it('Analytic Charts Focus Area Campus User', function() {
    cy.get("[data-cy='analytics']").click().should('be.visible')
    cy.get("[data-cy='charts']").next("[data-cy='chartsdropdown']").then($el => {
      cy.wrap($el).invoke('show').should('be.visible')
      cy.wrap($el).get("[data-cy='Focus Areas']").click()
    })

    cy.get('#select2-id_academicyear-container > .select2-selection__placeholder').contains('Previous Academic Year')
    cy.get('[data-cy="academic_year"]').select(this.data.academic_year1,{force:true})
    cy.get('#select2-id_academicyear-container').should('have.text' ,this.data.academic_year1)

    cy.get('#select2-id_engagement_type-container > .select2-selection__placeholder').contains('All Engagement Types')
    cy.get('[data-cy="engagement_type"]').select(this.data.engagement_type3,{force:true})
    cy.get('#select2-id_engagement_type-container').should('have.text' ,this.data.engagement_type3)

    cy.get('#select2-id_community_type-container > .select2-selection__placeholder').contains('All Community Organization Types')
    cy.get('[data-cy="community_type"]').select(this.data.community_type1,{force:true})
    cy.get('#select2-id_community_type-container').should('have.text' ,this.data.community_type1)

    cy.get('#select2-id_college_name-container > .select2-selection__placeholder').contains('All College and Main Units')
    cy.get('[data-cy="college_name"]').select(this.data.college_name3,{force:true})
    cy.get('#select2-id_college_name-container').should('have.text' ,this.data.college_name3)

    cy.get('#select2-id_campus_partner-container > .select2-selection__placeholder').contains('All Campus Partner')
    cy.get('[data-cy="campus_partner"]').select(this.data.campus_partner3,{force:true})
    cy.get('#select2-id_campus_partner-container').should('have.text' ,this.data.campus_partner3)

    cy.get('#select2-id_weitz_cec_part-container > .select2-selection__placeholder').contains('All (CEC/Non-CEC Partners)')
    cy.get('[data-cy="weitz_cec_part"]').select(this.data.cec_part1,{force:true})
    cy.get('#select2-id_weitz_cec_partr-container').should('have.text' ,this.data.cec_part1)

    cy.get('.highcharts-root').should('be.visible').and(chart => {
      expect(chart.height()).to.be.greaterThan(200)
    })
    cy.get('.highcharts-xaxis').contains('Focus Areas')
    cy.get('.highcharts-yaxis').contains('Projects/Community Partners')
    cy.get('.highcharts-xaxis-labels').filter(':contains("Arts, Culture and Humanities")').should('exist')
    cy.get('.highcharts-xaxis-labels').filter(':contains("Economic Impact")').should('exist')
    cy.get('.highcharts-xaxis-labels').filter(':contains("Educational Support")').should('exist')
    cy.get('.highcharts-xaxis-labels').filter(':contains("Environmental Stewardship")').should('exist')
    cy.get('.highcharts-xaxis-labels').filter(':contains("Health and Wellness")').should('exist')
    cy.get('.highcharts-xaxis-labels').filter(':contains("International Service")').should('exist')
    cy.get('.highcharts-xaxis-labels').filter(':contains("Social Justice")').should('exist')
  })

  it('Chart legends', function () {
    cy.get("[data-cy='analytics']").click()
    cy.get("[data-cy='charts']").next("[data-cy='chartsdropdown']").then($el => {
      cy.wrap($el).invoke('show')
      cy.wrap($el).get("[data-cy='Focus Areas']").click()
    })
    cy.get('.highcharts-series-0 > text').contains("Projects").should("be.visible")
    cy.get('.highcharts-series-0 > rect').should('have.attr', 'fill', 'turquoise')
    cy.get('.highcharts-series-1 > text').contains("Community Partners").should("be.visible")
    cy.get('.highcharts-series-1 > rect').should('have.attr', 'fill', 'teal')
  })


})