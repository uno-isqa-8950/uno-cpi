beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
      {
        return false
      }
    })
    cy.visit("https://uno-cpi-dev.herokuapp.com/")
    });

describe('Navigate to Resources Menu to view external links ', () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
        this.data = data
        })

    })
    
    it('Generating reports for Community partners', function()  {
        cy.get('#analyticnav')
        .click()
      //.el and wrap are used to select the drop down menu options 
        cy.contains('Reports').next('.dropdown-menu').then($el => {
            cy.wrap($el)
            .invoke('show')
          
            cy.wrap($el)
            .contains('Community Partners')
            .click()
           
        })
        //.el and wrap are used to select the drop down menu options for selecting the year 
        cy.get('#select2-id_academic_year-container')
        .click()
        cy.get('#select2-id_academic_year-results')
        .then(($li) => {
            cy.wrap($li)
            .contains(this.data.academic_year1)
            .click()
        })
        //.el and wrap are used to select the drop down and used contains to select the locator with text 'Business'
        cy.get('#select2-id_community_type-container')
        .click()
        cy.get('#select2-id_community_type-results').then(($li) => {
            cy.wrap($li)
            .contains(this.data.community_type1)
            .click()
        })
        //.el and wrap are used to select the drop down and used contains to select the locator with text 'Business'
        cy.get('#select2-id_community_type-container')
        .click()
        cy.get('#select2-id_community_type-results').then(($li) => {
            cy.wrap($li)
            .contains(this.data.community_type1)
            .click()
        })
        //.el and wrap are used to select the drop down and used contains to select the locator with text 'Current Community Building Partners"'
        cy.get('#select2-id_weitz_cec_part-container')
        .click()
        cy.get('#select2-id_weitz_cec_part-results').then(($li) => {
            cy.wrap($li)
            .contains(this.data.cec_part1)
            .click()
        })
        //.el and wrap are used to select the drop down and used contains to select the locator with text 'Academic Affairs'
        cy.get('#select2-id_college_name-container')
        .click()
        cy.get('#select2-id_college_name-results').then(($li) => {
            cy.wrap($li)
            .contains(this.data.college_name1)
            .click()
        })
        //.el and wrap are used to select the drop down and used contains to select the locator with text 'All"'
        cy.get('#select2-id_campus_partner-container')
        .click()
        cy.get('#select2-id_campus_partner-results').then(($li) => {
            cy.wrap($li)
            .contains(this.data.select_all)
            .click()
        })
        //.el and wrap are used to select the drop down and used contains to select the locator with text 'Legislative District 1'
        cy.get('#select2-id_legislative_value-container')
        .click()
        cy.get('#select2-id_legislative_value-results').then(($li) => {
            cy.wrap($li)
            .contains(this.data.legislative_dist1)
            .click()
        })
        //download CSV report
        cy.get('.buttons-csv')
        .click()
        //download PDF report
        cy.get('.buttons-pdf')
        .click()

    })
})

