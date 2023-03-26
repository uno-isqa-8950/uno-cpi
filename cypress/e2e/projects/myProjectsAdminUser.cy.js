import user from "../../support/commands.js";

beforeEach(() => {
    cy.on('uncaught:exception', (err) => {
      if(err.message.includes('is not a function') 
          || err.message.includes('is not defined') 
          || err.message.includes('reading \'addEventListener\'') 
          || err.message.includes('null (reading \'style\')')
          || err.message.includes('null (reading \'options\')') 
          || err.message.includes('null (reading \'scrollTop'))  
      {
        return false;
      }
    })
    cy.visit(Cypress.env('baseUrl'))
    cy.get('#login').click()
      .loginAdminUser(user)
  })
  
  describe('my projects test', () => {
    beforeEach(function() {
      cy.fixture("datareports").then(function(data) {
        this.data = data
      })
    })

    it('Test my projects page navigation bar', function(){
        const unoLogo = `img[alt="UNO Logo"]`,
          navigationList = '[data-cy="navigationlist"]',
          userInfo = '[data-cy="accountinfo"]',
          projectsLink = '[data-cy="projectsnav"]',
          myProjectsLink = '[data-cy="myprojects"]'
        cy.get(projectsLink).should('exist').click()
          .get(myProjectsLink).should('exist').click()
          .get(unoLogo).should('be.visible')
          .get(navigationList).should('be.visible').contains('Maps')
          .get(navigationList).contains('Analytics')
          .get(navigationList).contains('Projects')
          .get(navigationList).contains('Partners')
          .get(navigationList).contains('Resources')
          .get(userInfo).should('be.visible') 
      })
    
    it('Test my projects page navigation bar, title and footer', function(){
        const projectsLink = '[data-cy="projectsnav"]',
          myProjectsLink = '[data-cy="myprojects"]',
          footer = '[data-cy="footer"]'
        cy.get(projectsLink).should('exist').click()
          .get(myProjectsLink).should('exist').click()
          .url().should('be.equal', this.data.baseUrl+'myProjects/')
          .get('h3').contains("My Projects").should("be.visible")
          .get(footer).should('exist')
      })
    
    it('Test my projects page excel, pdf button', function(){
        const projectsLink = '[data-cy="projectsnav"]',
          myProjectsLink = '[data-cy="myprojects"]'
        cy.get(projectsLink).should('exist').click()
          .get(myProjectsLink).should('exist').click()
          .get('button').contains('Excel').should('be.visible').click()
          .get('button').contains('PDF').should('be.visible').click() 
      })

    it('Test my projects page show entries and pagination buttons functionality', function(){
        const projectsLink = '[data-cy="projectsnav"]',
          myProjectsLink = '[data-cy="myprojects"]',
          searchField = `input[type="search"]`,
          showEntriesSelect = `select[name="example_length"]`
        cy.get(projectsLink).should('exist').click()
          .get(myProjectsLink).should('exist').click()
          .get(showEntriesSelect).select('10').should('exist')
          .get(showEntriesSelect).select('25').should('exist')
          .get(showEntriesSelect).select('50').should('exist')
          .get(showEntriesSelect).select('100').should('exist') 
          .get(searchField).type('Arts')
          .get('a').contains('Previous').should('exist')
          .get('a').contains('Next').should('exist')
      })

    it.only('Test project creation to test project editing', function(){
        const projectsLink = '[data-cy="projectsnav"]',
          createProjectsLink = '[data-cy="createproject"]',
          academicYearsDropdown = '#select2-academicYear-container',
          academicYearsResultsId = '#select2-academicYear-results',
          communityPartners = '#select2-communityPartner-container',
          communityPartnerResultsId = '#select2-communityPartner-results',
          campusPartners = '#select2-campuspartner-container',
          campusPartnersResultsId = '#select2-campuspartner-results',
          projectNameInputField = '[data-cy="projectnameinput"]',
          searchButton = '[data-cy="search"]',
          engagementTypeInputField = '#select2-id_engagement_type-container',
          engagementTypeResults = '#select2-id_engagement_type-results',
          submitButton =  '[data-cy="submit"]',
          createprojectButton = '#lnk-create_project',
          projectDescriptionField = '[data-cy="descriptioninput"]',
          projectDurationCollapse = '[data-cy="projectduration"]',
          campusPartAddButton = '[data-cy="clicktoadd"]',
          checkbox = '[data-cy="checkbox"]',
          campusPartnerCollapse = '[data-cy="campuspartnerinfo"]'
        cy.get(projectsLink).should('exist').click()
          .get(createProjectsLink).should('exist').click()
          .url().should('be.equal', this.data.baseUrl+'check-Project/')
          .get(academicYearsDropdown).click()
          .get(academicYearsResultsId).contains(this.data.select_all).click()
          .get(communityPartners).click()
          .get(communityPartnerResultsId).contains(this.data.select_all).click()
          .get(campusPartners).click()
          .get(campusPartnersResultsId).contains(this.data.campus_partner10).click()
          .get(projectNameInputField).should('exist').clear().type('testproject')
          .get(searchButton).click()
           // Partner Information
          .get(createprojectButton).click({force: true})
          .url().should('be.equal', this.data.baseUrl+'create-Project/?p_name=testproject#step-1')

          .get(projectDescriptionField).type('This is a test project')
          
          
          .get(engagementTypeInputField).click()
          .get(engagementTypeResults).contains(this.data.engagement_type3).click()

          .get(projectDurationCollapse).click()
          .get('#select2-id_semester-container').click()
          .get('#select2-id_semester-results').then(($li) => {
              cy.wrap($li).contains(this.data.semester1).click();
           })

          .get('#select2-id_academic_year-container').click()
          .get('#select2-id_academic_year-results').then(($li) => {
              cy.wrap($li).contains(this.data.academic_year4).click();
           })

          .get('button').contains('Next').click()
        //  .get('#id_community-0-community_partner').select(this.data.community_partner3)

          .get(campusPartnerCollapse).click({force: true}).wait(2000)
          .get('#id_campus-0-campus_partner').select(this.data.campus_partner10)
          .get(campusPartAddButton).click()

          .get('button').contains('Next').click()

          .get('#id_mission-0-mission').select(this.data.focus_area7)
          .get('button').contains('Next').click()

          .get(checkbox).click()

          .get(submitButton).click({force: true})
        //  .url().should('be.equal',this.data.baseUrl+'draft-project-done/#step-1')
      })


      it('Test my projects saved in draft are editable and saved as draft again', function(){
        const projectsLink = '[data-cy="projectsnav"]',
          myProjectsLink = '[data-cy="myprojects"]',
          projectNameInputField = '[data-cy="projectnameinput"]',
          saveDraftButton = '[data-cy="saveasdraft"]'
          cy.get(projectsLink).should('exist').click()
            .get(myProjectsLink).should('exist').click()
            .url().should('be.equal', this.data.baseUrl+'myProjects/')
            .get('h3').contains("My Projects").should("be.visible")
            .get('td').contains('testproject').click()
            .get('a').contains('Edit').click({force: true})
            .get(projectNameInputField).clear().type('testprojectedited')
            .get(saveDraftButton).click({force: true})
            .url().should('be.equal', this.data.baseUrl+'draft-project-done/')
            .get('h3').contains('Thank You')          
      })

      it('Test my projects delete functionality', function(){
        const projectsLink = '[data-cy="projectsnav"]',
        myProjectsLink = '[data-cy="myprojects"]'
          cy.get(projectsLink).should('exist').click()
            .get(myProjectsLink).should('exist').click()
            .url().should('be.equal', this.data.baseUrl+'myProjects/')
            .get('h3').contains("My Projects").should("be.visible")
            .get('td').contains('testprojectedited').click()
            .get('a').contains('Delete').click({force: true})
          cy.on("window:confirm", (t) => {
                //verify text on pop-up
                expect(t).to.equal("Are you sure you want to delete this Project?");
             });
          cy.url().should('be.equal', this.data.baseUrl+'myProjects/')    
      })
});