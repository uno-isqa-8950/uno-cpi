import user from "../../../support/commands.js";
describe('Engagement Types Report Administrator', () => {
beforeEach(() => {
    cy.on('uncaught:exception', (err) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
      {
        return false
      }
    })
    cy.fixture("datareports").then(function(data) {
      this.data = data
    })
    cy.loginAdminUser(user)  // Admin User is logged in before the test begins
    cy.visit(Cypress.env('baseUrl'))
  })
    it('visits the form', function() {
        cy.visit(Cypress.env('baseUrl'))
    })
   //Check navigation
   it('Check navigation', function() {
    cy.url().should('be.equal', Cypress.env('baseUrl'))
    cy.get('[data-cy=himg]').click()
    cy.get('[data-cy=analytics]').contains('Analytics').click()
    cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
        cy.wrap($el).invoke('show')
        cy.wrap($el).contains('Engagement Types').click()
    })
    })
    it('Check if it is Engagement Type Report', function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Type').click()
        })
        cy.get('[data-cy=heading]').should('contain.text', 'Engagement Types Report')
    })
    it('Hide Filters', function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Type').click()
        })
        cy.get('[data-cy=hidefilterbtn]').should('have.class', 'btn btn-secondary')
        cy.get('[data-cy=hidefilterbtn]').click()
        cy.get('.select2-selection__placeholder').should('not.be.visible')
        // check the filers are they visible
        cy.get('[data-cy=hidefilterbtn]').click()
        cy.get('[data-cy=hidefilterbtn]').should('have.class', 'btn btn-secondary')
        cy.get('.select2-selection__placeholder').should('be.visible')
        })
    it('Reset Filters', function() {
        const resetFilterButton = '[data-cy=resetfilterbtn]'
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Type').click()
        })
        //Academic year filter
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
        cy.get('[data-cy="academic_year"]').select(this.data.academic_year1,{force:true})
        // Focus area filter
        cy.get('#select2-id_mission-container> .select2-selection__placeholder').contains('All Project Focus Areas')
        cy.get('[data-cy="mission"]').select(this.data.focus_area3,{force:true})
        cy.get('#select2-id_academic_year-container').should('contain.text', this.data.academic_year1)
        cy.get('[data-cy=resetfilterbtn]').click()
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
        })
    // Filter Options    
    it('filter options', function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Type').click()
        })
        //Academic year filter
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
        cy.get('[data-cy="academic_year"]').select(this.data.academic_year1,{force:true})
        //Focus area filter
        cy.get('#select2-id_mission-container> .select2-selection__placeholder').contains('All Project Focus Areas')
        cy.get('[data-cy="mission"]').select(this.data.focus_area4,{force:true})
        //Community type filter
        cy.get('#select2-id_community_type-container> .select2-selection__placeholder').contains('All Community Organization Types')
        cy.get('[data-cy="community_type"]').select(this.data.community_type2,{force:true})
        //Collage name filter
        cy.get('#select2-id_college_name-container> .select2-selection__placeholder').contains('All College and Main Units')
        cy.get('[data-cy="college_name"]').select(this.data.college_name3,{force:true})
        //Campus partner filter
        cy.get('#select2-id_campus_partner-container .select2-selection__placeholder').contains('All Campus Partners')
        cy.get('[data-cy="campus_partner"]').select(this.data.select_all,{force:true})
        //CEC filter
        cy.get('#select2-id_weitz_cec_part-container .select2-selection__placeholder').contains('All (CEC/Non-CEC Partners)')
        cy.get('[data-cy="weitz_cec_part"]').select(this.data.cec_part3,{force:true})
        //Report download
        cy.get('.buttons-csv').click()
        cy.get('.buttons-pdf').click()
    })
    it('Check if report contains all Engagement Type and tooltip', function () {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Type').click()
        })
        //Engagement Type 1
        //cy.get('[data-cy="engagement-type"]').contains('td',this.data.engagement_type1)
        //cy.parent().find('[data-cy=engagement-type-tooltip]').click()
        //cy.contains('Participation in the governing body of a community partner.')
        //Engagement Type 2
        cy.get('[data-cy="engagement-type"]').contains('td',this.data.engagement_type2)
        .parent().find('[data-cy=engagement-type-tooltip]').click()
        //cy.contains('Professional experiences that provide an opportunity to put academic knowledge in practice or learn more about a specific profession. During these experiences, it is expected that students gain intensive experience applying principles of civic and community engagement and disciplinary knowledge and skills in a community setting.')
        //Engagement Type 3
        cy.get('[data-cy="engagement-type"]').contains('td',this.data.engagement_type3)
            .parent().find('[data-cy=engagement-type-tooltip]').click()
        //cy.contains('Engaged research (the scholarship of engagement), defined by the New England Resource Center for Higher Education (NERCHE) – A type of engagement that “redefines faculty scholarly work from application of academic expertise to community engaged scholarship that involves the faculty member in a reciprocal partnership with the community."')
        //Engagement Type 4
        cy.get('[data-cy="engagement-type"]').contains('td',this.data.engagement_type4)
        .parent().find('[data-cy=engagement-type-tooltip]').click()
        //cy.contains('Refers to activities tailored to expand or transfer knowledge (e.g. access to higher education, presentations, workshops, etc.).')
        //Engagement Type 5
        cy.get('[data-cy="engagement-type"]').contains('td',this.data.engagement_type5)
            .parent().find('[data-cy=engagement-type-tooltip]').click()
        //cy.contains('A method of teaching that combines classroom instruction with meaningful, community-identified service. This form of engaged teaching and learning emphasizes critical thinking by using reflection to connect course context with real-world experiences. Service learning instructors partner with community organizations as co-teachers and encourage a heightened sense of community, civic engagement, and personal responsibility for students while building capacity and contributing real community impact.')
        //Engagement Type 6
        cy.get('[data-cy="engagement-type"]').contains('td',this.data.engagement_type6)
        .parent().find('[data-cy=engagement-type-tooltip]').click()
        //cy.contains('A non-curriculum, non-fee based community involvement that provides community or societal assistance, ultimately aiming towards community and societal improvement. Exemplary efforts may be recognized through scholarships, awards, recognition, and other rewards.')
    })
    it("Check conectivity to Community Partners report", function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Type').click()
        })
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
        cy.get('[data-cy="academic_year"]').select(this.data.select_all,{force:true})
        cy.get('table').contains('td',this.data.engagement_type5)
          .parent()
          .find('a[data-cy=community_count]').invoke('attr', 'target', '_self').click()
        cy.get('[data-cy="heading"]').should('contain.text', 'Community Partners Report')
        cy.url().should('contain', Cypress.env('baseUrl')+'community-public-report')
    })
    it("Check conectivity to Projects report", function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Type').click()
        })
        cy.get('#select2-id_academic_year-container > .select2-selection__placeholder').contains('Previous Academic Year')
        cy.get('[data-cy="academic_year"]').select(this.data.select_all,{force:true})
        cy.get('table').contains('td',this.data.engagement_type5)
            .parent()
            .find('a[data-cy=projectcount]').invoke('attr', 'target', '_self').click()
        cy.get('[data-cy="heading"]').should('contain.text', 'Projects Report')
        cy.url().should('contain', Cypress.env('baseUrl')+'projectspublicreport/')
    })
    it("Search in Engagement type Report", function() {
        cy.get('[data-cy=analytics]').contains('Analytics').click()
        cy.get('[data-cy=reports]').next('[data-cy=reportsdropdown]').then($el => {
            cy.wrap($el).invoke('show')
            cy.wrap($el).contains('Engagement Type').click()
        })
        cy.get('label > .form-control').type(this.data.engagement_type3).click()
        cy.get('[data-cy="engagement-type"]').should('contain', this.data.engagement_type3)
    })
})