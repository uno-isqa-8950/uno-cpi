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

describe('Charts Project and Partner Trend', () => {
  beforeEach(function() {
    cy.fixture("datareports").then(function(data) {
      this.data = data
      cy.get('#login').click()
      cy.loginAdminUser(user)
    })
  })
  it('visits the site', function() {
    cy.visit(Cypress.env('baseUrl'))
  })
  //Check navigation to Project and Partner Trends charts
  it('Check navigation', function () {
    cy.get("[data-cy='analytics']").click()
    cy.get("[data-cy='charts']").next("[data-cy='chartsdropdown']").then($el => {
      cy.wrap($el).invoke('show')
      cy.wrap($el).get("[data-cy='Project and Partner Trends']").click()
    })
      cy.get("[data-cy='Project and Partner Trends']").should('contain.text', 'Project and Partner Trends')
  })
  //Hide Filter
  it('Hide Filters', function () {
    cy.get("[data-cy='analytics']").click().should('be.visible')
    cy.get("[data-cy='charts']").next("[data-cy='chartsdropdown']").then($el => {
      cy.wrap($el).invoke('show').should('be.visible')
      cy.wrap($el).get("[data-cy='Project and Partner Trends']").click()
    })
    cy.get('[data-cy="hide filters"]').should('have.value', 'Hide Filters')
    cy.get('[data-cy="hide filters"]').click()
    // check the filers are they visible
    cy.get('[data-cy="hide filters"]').click()
    cy.get('[data-cy="hide filters"]').should('have.value', 'Hide Filters')
    cy.get('.select2-selection__placeholder').should('be.visible')
  })
  //Reset filters
  it('Reset Filters', function () {
     cy.get("[data-cy='analytics']").click()
     cy.get("[data-cy='charts']").next("[data-cy='chartsdropdown']").then($el => {
         cy.wrap($el).invoke('show')
         cy.wrap($el).get("[data-cy='Project and Partner Trends']").click()
     })
     cy.get('#select2-id_mission-container > .select2-selection__placeholder').contains('All Focus Area')
     cy.get('[data-cy="mission"]').select(this.data.focus_area1,{force:true})
     cy.get('#select2-id_mission-container').should('have.text' ,this.data.focus_area1)

     cy.get('#select2-id_community_type-container > .select2-selection__placeholder').contains('All Community Organization Types')
     cy.get('[data-cy="community_type"]').select(this.data.community_type5,{force:true})
     cy.get('#select2-id_community_type-container').should('have.text' ,this.data.community_type5)

     cy.get('#select2-id_engagement_type-container > .select2-selection__placeholder').contains('All Engagement Type')
     cy.get('[data-cy="engagement_type"]').select(this.data.engagement_type3,{force:true})
     cy.get('#select2-id_engagement_type-container').should('have.text' ,this.data.engagement_type3)

     cy.get('[data-cy="reset filters"]').should('have.value', 'Reset Filters')
     cy.get('[data-cy="reset filters"]').click()
     // check the filers are they visible
     cy.get('[data-cy="reset filters"]').click()
     cy.get('[data-cy="reset filters"]').should('have.value', 'Reset Filters')
     cy.get('.select2-selection__placeholder').should('be.visible')

  })
  // Filter options
  it('Analytic Charts Project and Partner Trends', function() {
    cy.get("[data-cy='analytics']").click().should('be.visible')
    cy.get("[data-cy='charts']").next("[data-cy='chartsdropdown']").then($el => {
      cy.wrap($el).invoke('show').should('be.visible')
      cy.wrap($el).get("[data-cy='Project and Partner Trends']").click()
    })

    cy.get('#select2-id_mission-container > .select2-selection__placeholder').contains('All Focus Area')
    cy.get('[data-cy="mission"]').select(this.data.focus_area1,{force:true})
    cy.get('#select2-id_mission-container').should('have.text' ,this.data.focus_area1)

    cy.get('#select2-id_community_type-container > .select2-selection__placeholder').contains('All Community Organization Types')
    cy.get('[data-cy="community_type"]').select(this.data.community_type5,{force:true})
    cy.get('#select2-id_community_type-container').should('have.text' ,this.data.community_type5)

    cy.get('#select2-id_engagement_type-container > .select2-selection__placeholder').contains('All Engagement Type')
    cy.get('[data-cy="engagement_type"]').select(this.data.engagement_type3,{force:true})
    cy.get('#select2-id_engagement_type-container').should('have.text' ,this.data.engagement_type3)

    cy.get('#select2-id_college_name-container > .select2-selection__placeholder').contains('All College and Main Units')
    cy.get('[data-cy="college_name"]').select(this.data.college_name1,{force:true})
    cy.get('#select2-id_college_name-container').should('have.text' ,this.data.college_name1)

    cy.get('#select2-id_campus_partner-container > .select2-selection__placeholder').contains('All Campus Partner')
    cy.get('[data-cy="campus_partner"]').select(this.data.campus_partner3,{force:true})
    cy.get('#select2-id_campus_partner-container').should('have.text' ,this.data.campus_partner3)

    cy.get('#select2-id_weitz_cec_part-container > .select2-selection__placeholder').contains('All (CEC/Non-CEC Partners)')
    cy.get('[data-cy="weitz_cec_part"]').select(this.data.cec_part1,{force:true})
    cy.get('#select2-id_weitz_cec_part-container').should('have.text' ,this.data.cec_part1)

    cy.get('.highcharts-root').should('be.visible').and(chart => {
      expect(chart.height()).to.be.greaterThan(200)
    })
    cy.get('.highcharts-yaxis').contains('Projects/Partners')
    cy.get('.highcharts-xaxis').contains('Academic Years')
  })
  //Verify chart legends
  it('Chart legends', function () {
    cy.get("[data-cy='analytics']").click()
    cy.get("[data-cy='charts']").next("[data-cy='chartsdropdown']").then($el => {
      cy.wrap($el).invoke('show')
      cy.wrap($el).get("[data-cy='Project and Partner Trends']").click()
    })
    cy.get('.highcharts-series-0 > text').contains("Projects").should("be.visible")
    //cy.get('.highcharts-series-0 > path').should('have.attr', 'fill', 'turquoise')
    cy.get('.highcharts-series-1 > text').contains("Community Partners").should("be.visible")
    //cy.get('.highcharts-series-1 > path').should('have.attr', 'fill', 'teal')
    cy.get('.highcharts-series-2 > text').contains("Campus Partners").should("be.visible")
    //cy.get('.highcharts-series-2 > path').should('have.attr', 'fill', 'blue')
    })
})