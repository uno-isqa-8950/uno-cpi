beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') 
        || err.message.includes('reading \'addEventListener\'')  || err.message.includes('reading \'update\'')|| err.message.includes('null (reading \'style\')'))
       
        {
            return false
        }
    })
    cy.visit(Cypress.env('baseUrl'))
    cy.get('#login').click()
  cy.loginAdminUser()
})

describe('Charts Partnership intensity analysis test', () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
        })
    })

    it('Test partnership intensity analysis page loading with all elements visible ', function() {
        const analyticsNavButton = '[data-cy="analytics"]',
          chartDropdownButton = '[data-cy="charts"]',
          partnershipIntensityAnalysis = '[data-cy="Partner Intensity"]',
          heading = '[data-cy="heading"]',
          hideFiltersButton = '[data-cy="hidefilters"]',
          resetFiltersButton = '[data-cy="resetfilters"]'
        cy.get(analyticsNavButton).contains('Analytics').click()
          .get(chartDropdownButton).contains('Charts').click()
          .get(partnershipIntensityAnalysis).click({force: true})
          .url().should('be.equal', Cypress.env('baseUrl')+'partnershipintensity/') 
          .get(heading).contains('Partnership Intensity Analysis')
          .get(hideFiltersButton).should('exist')
          .get(resetFiltersButton).should('exist')
    })

    it('filter options selectability test', function () {
        const analyticsNavButton = '[data-cy="analytics"]',
          chartDropdownButton = '[data-cy="charts"]',
          partnershipIntensityAnalysis = '[data-cy="Partner Intensity"]'
        cy.get(analyticsNavButton).contains('Analytics').click()
          .get(chartDropdownButton).contains('Charts').click()
          .get(partnershipIntensityAnalysis).click({force: true})
          .url().should('be.equal', Cypress.env('baseUrl')+'partnershipintensity/') 
        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li) => {
            cy.wrap($li).contains(this.data.academic_year1).click();
        })
        cy.get('#select2-id_community_type-container').click()
        cy.get('#select2-id_community_type-results').then(($li) => {
            cy.wrap($li).contains(this.data.community_type1).click();
        })
        cy.get('#select2-id_engagement_type-container').click()
        cy.get('#select2-id_engagement_type-results').then(($li) => {
            cy.wrap($li).contains(this.data.engagement_type5).click();
        })
        cy.get('#select2-id_college_name-container').click()
        cy.get('#select2-id_college_name-results').then(($li) => {
            cy.wrap($li).contains(this.data.select_all).click();
        })
        cy.get('#select2-id_campus_partner-container').click()
        cy.get('#select2-id_campus_partner-results').then(($li) => {
            cy.wrap($li).contains(this.data.select_all).click();
        })
        cy.get('#select2-id_weitz_cec_part-container').click()
        cy.get('#select2-id_weitz_cec_part-results').then(($li) => {
            cy.wrap($li).contains(this.data.cec_part1).click();
        })
        cy.get('#select2-id_legislative_value-container').click()
        cy.get('#select2-id_legislative_value-results').then(($li) => {
            cy.wrap($li).contains(this.data.legislative_dist1).click();
        })

        cy.get('#select2-id_community_partner-container').click()
        cy.get('#select2-id_community_partner-results').then(($li) => {
            cy.wrap($li).contains(this.data.select_all).click();
        })

        cy.get('#select2-id_y_axis-container').click()
        cy.get('#select2-id_y_axis-results').then(($li) => {
            cy.wrap($li).contains(this.data.y_axis1).click();
        })
    })

    it('filter options selecting to test charts rendering with appropriate data', function () {
        const analyticsNavButton = '[data-cy="analytics"]',
          chartDropdownButton = '[data-cy="charts"]',
          partnershipIntensityAnalysis = '[data-cy="Partner Intensity"]'
        cy.get(analyticsNavButton).contains('Analytics').click()
          .get(chartDropdownButton).contains('Charts').click()
          .get(partnershipIntensityAnalysis).click({force: true})
          .url().should('be.equal', Cypress.env('baseUrl')+'partnershipintensity/') 
        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li) => {
            cy.wrap($li).contains(this.data.academic_year1).click();
        })
        cy.get('#select2-id_community_type-container').click()
        cy.get('#select2-id_community_type-results').then(($li) => {
            cy.wrap($li).contains(this.data.community_type1).click();
        })
        cy.get('#select2-id_y_axis-container').click()
        cy.get('#select2-id_y_axis-results').then(($li) => {
            cy.wrap($li).contains(this.data.y_axis1).click();
        })
        cy.get('g[class="highcharts-axis highcharts-xaxis"]').contains('Projects')
        cy.get('g[class="highcharts-axis highcharts-yaxis"]').contains('Number of Campus Partners')
        cy.get('g[class="highcharts-legend highcharts-no-tooltip"]').contains('Arts, Culture and Humanities')
        cy.get('g[class="highcharts-legend highcharts-no-tooltip"]').contains('Economic Impact')
        cy.get('g[class="highcharts-legend highcharts-no-tooltip"]').contains('Educational Support')
        cy.get('g[class="highcharts-legend highcharts-no-tooltip"]').contains('Environmental Stewardship')
        cy.get('g[class="highcharts-legend highcharts-no-tooltip"]').contains('Health and Wellness')
        cy.get('g[class="highcharts-legend highcharts-no-tooltip"]').contains('International Service')
        cy.get('g[class="highcharts-legend highcharts-no-tooltip"]').contains('Social Justice')
    })

    it('Charts plot line and overlapping checkbox test', function () {
        const analyticsNavButton = '[data-cy="analytics"]',
          chartDropdownButton = '[data-cy="charts"]',
          partnershipIntensityAnalysis = '[data-cy="Partner Intensity"]' ,
          overlappingPointsCheckBox =    '[data-cy="showoverlapcheckbox"]'
        cy.get(analyticsNavButton).contains('Analytics').click()
          .get(chartDropdownButton).contains('Charts').click()
          .get(partnershipIntensityAnalysis).click({force: true})
          .url().should('be.equal', Cypress.env('baseUrl')+'partnershipintensity/') 
        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li) => {
            cy.wrap($li).contains(this.data.academic_year1).click();
        })
        cy.get('#select2-id_community_type-container').click()
        cy.get('#select2-id_community_type-results').then(($li) => {
            cy.wrap($li).contains(this.data.community_type1).click();
        })
        cy.get('#select2-id_y_axis-container').click()
        cy.get('#select2-id_y_axis-results').then(($li) => {
            cy.wrap($li).contains(this.data.y_axis1).click();
        })

        cy.get('g[class="highcharts-plot-lines-0"]').should('exist')
        cy.get(overlappingPointsCheckBox).should('exist')
        
    })


});
