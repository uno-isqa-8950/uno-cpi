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
          navigationList = '[data-cy="navbar"]',
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
          .url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
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

    it('Test project creation to test project editing', function(){
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
          checkbox = '[data-cy="checkbox"]'     
        cy.get(projectsLink).should('exist').click()
          .get(createProjectsLink).should('exist').click()
          .url().should('be.equal', Cypress.env('baseUrl')+'check-Project/')
          .get(academicYearsDropdown).click()
          .get(academicYearsResultsId).contains(this.data.select_all).click()
          .get(communityPartners).click()
          .get(communityPartnerResultsId).contains(this.data.select_all).click()
          .get(campusPartners).click()
          .get(campusPartnersResultsId).contains(this.data.campus_partner10).click()
          .get(projectNameInputField).should('exist').clear()
          .get(projectNameInputField).type('testprojects')
          .get(searchButton).click()
           // Partner Information
          .get(createprojectButton).click({force: true})
          .url().should('be.equal', Cypress.env('baseUrl')+'create-Project/?p_name=testprojects#step-1')
          .get(projectDescriptionField).type('This is a test project')
          
        //.get(projectNameInputField).clear().type('testprojects')
        //.get('.btn-secondary').click()
          .get(engagementTypeInputField).click()
          .get(engagementTypeResults).contains(this.data.engagement_type3).click()

          .get(projectDurationCollapse).click()
          .get('#select2-id_semester-container').click()
          .get('#select2-id_semester-results').then(($li) => {
              cy.wrap($li).contains(this.data.semester1).click();
           })
           .get(projectNameInputField).should('exist').clear().type('testprojects')
          .wait(2000)
          .get('#select2-id_academic_year-container').click()
          .get('#select2-id_academic_year-results').then(($li) => {
              cy.wrap($li).contains(this.data.academic_year4).click();
           })
         //  .get(projectNameInputField).should('exist').clear().type('testproject')
           .get('button').contains('Next').dblclick().wait(3000)
        //  .get('#id_community-0-community_partner').select(this.data.community_partner3)

          .get('#campuspartnerinfonav').click({force: true}).wait(2000)
          .get('#id_campus-0-campus_partner').select(this.data.campus_partner3,{force: true})
          .get(campusPartAddButton).click()

          .get('button').contains('Next').dblclick()

          .get('#id_mission-0-mission').select(this.data.focus_area7)
          .get('button').contains('Next').click()

        cy.get('#id_address_line1').type(this.data.addressline)
        cy.get('#id_city').type(this.data.city)
        cy.get('#id_country').type(this.data.country)
        cy.get('#id_state').type(this.data.province)
        cy.get('#id_zip').type(this.data.zipcode)

          .get(checkbox).click()
       // .get(projectNameInputField).should('exist').type('testproject')
          .get('#submit').click({force: true})
          .url().should('be.equal',Cypress.env('baseUrl')+'adminsubmit_project_done/#step-4')
      })


      // it('Test projects in my projects page are editable', function(){
      //   const projectsLink = '[data-cy="projectsnav"]',
      //     myProjectsLink = '[data-cy="myprojects"]',
      //     projectNameInputField = '[data-cy="projectnameinput"]',
      //     step4 = '[data-cy="step4"]',
      //     termsCheck =  '[data-cy="terms"]',
      //     updateButton = '[data-cy="update"]'
      //     cy.get(projectsLink).should('exist').click()
      //       .get(myProjectsLink).should('exist').click()
      //       .url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
      //       .get('h3').contains("My Projects").should("be.visible")
      //       .get('td').contains('testprojects').click()
      //       .get('a').contains('Edit').click({force: true})
      //       .get(projectNameInputField).type('edited')
      //       .get('button').contains('Next').dblclick()
      //       .get('button').contains('Next').dblclick()
      //       .get('button').contains('Next').dblclick()
      //       .get('button').contains('Next').dblclick()
      //       .get(step4).click()
      //       .get(termsCheck).eq(0).click()
      //       .get(updateButton).click({force:true})
      //       //.url().should('be.equal', Cypress.env('baseUrl')+'adminsubmit_project_done/')
      //
      //       //.url().should('be.equal', Cypress.env('baseUrl')+'draft-project-done/')
      //       //.get('h3').contains('Thank You')
      // })

      it('Test my projects delete functionality', function(){
        const projectsLink = '[data-cy="projectsnav"]',
        myProjectsLink = '[data-cy="myprojects"]'
          cy.get(projectsLink).should('exist').click()
            .get(myProjectsLink).should('exist').click()
            .url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
            .get('h3').contains("My Projects").should("be.visible")
            .get('td').contains('testprojects').click()
            .get('a').contains('Delete').click({force: true})
          cy.on("window:confirm", (t) => {
                //verify text on pop-up
                expect(t).to.equal("Are you sure you want to delete this Project?");
             });
          cy.url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')    
      })
});
