beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })
    cy.visit(Cypress.env('baseUrl'))
    cy.get('#login').click()
  cy.loginCampusUser()
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
          partnershipIntensityAnalysis = '[data-cy="partnershipintensity"]'
        cy.get(analyticsNavButton).contains('Analytics').click()
          .get(chartDropdownButton).contains('Charts').click()
          .get(partnershipIntensityAnalysis).click()
          .get()

    })


});
