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
  })
  
  describe('my projects test', () => {
    beforeEach(function() {
      cy.fixture("datareports").then(function(data) {
        this.data = data
      cy.get('#login').click()
        .loginCampusUser(user)
      })
    })

    it('Test my projects page navigation bar', function(){
        const unoLogo = `img[alt="UNO Logo"]`,
          navigationList = '#navigationList',
          userInfo = '#accountinfo',
          projectsId = '#projectsnav',
          myProjectsHref = `a[href="/myProjects/"]`
        cy.get(projectsId).should('exist').click()
          .get(myProjectsHref).should('exist').click()
          .get(unoLogo).should('be.visible')
          .get(navigationList).should('be.visible').contains('Maps')
          .get(navigationList).contains('Analytics')
          .get(navigationList).contains('Projects')
          .get(navigationList).contains('Partners')
          .get(navigationList).contains('Resources')
          .get(userInfo).should('be.visible') 
      })
    
    it('Test my projects page navigation bar, title and footer', function(){
        const projectsId = '#projectsnav',
          myProjectsHref = `a[href="/myProjects/"]`,
          footerId = '#footer'
        cy.get(projectsId).should('exist').click()
          .get(myProjectsHref).should('exist').click()
          .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/myProjects/')
          .get('h3').contains("My Projects").should("be.visible")
          .get(footerId).should('exist')
      })
    
    it('Test my projects page excel, pdf button', function(){
        const projectsId = '#projectsnav',
          myProjectsHref = `a[href="/myProjects/"]`
        cy.get(projectsId).should('exist').click()
          .get(myProjectsHref).should('exist').click()
          .get('button').contains('Excel').should('be.visible').click()
          .get('button').contains('PDF').should('be.visible').click() 
      })

    it('Test my projects page show entries and pagination buttons functionality', function(){
        const projectsId = '#projectsnav',
          myProjectsHref = `a[href="/myProjects/"]`,
          searchField = `input[type="search"]`,
          showEntriesSelect = `select[name="example_length"]`
        cy.get(projectsId).should('exist').click()
          .get(myProjectsHref).should('exist').click()
          .get(showEntriesSelect).select('10').should('exist')
          .get(showEntriesSelect).select('25').should('exist')
          .get(showEntriesSelect).select('50').should('exist')
          .get(showEntriesSelect).select('100').should('exist') 
          .get(searchField).type('Arts')
          .get('a').contains('Previous').should('exist')
          .get('a').contains('Next').should('exist')
      })

    it('Test project creation to test project editing', function(){
        const projectsId = '#projectsnav',
          createProjectsHref = `a[href="/check-Project/"]`,
          academicYearsDropdown = '#select2-academicYear-container',
          academicYearsResultsId = '#select2-academicYear-results',
          communityPartners = '#select2-communityPartner-container',
          communityPartnerResultsId = '#select2-communityPartner-results',
          campusPartners = '#select2-campuspartner-container',
          campusPartnersResultsId = '#select2-campuspartner-results',
          projectNameSearchField = '#projectName',
          searchButton = `button[name="submit"]`,
          engagementTypeInputField = '#select2-id_engagement_type-container',
          engagementTypeResults = '#select2-id_engagement_type-results',
          saveDraftButton = `button[name="draft"]`
        cy.get(projectsId).should('exist').click()
          .get(createProjectsHref).should('exist').click()
          .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/check-Project/')
          .get(academicYearsDropdown).click()
          .get(academicYearsResultsId).contains(this.data.select_all).click()
          .get(communityPartners).click()
          .get(communityPartnerResultsId).contains(this.data.select_all).click()
          .get(campusPartners).click()
          .get(campusPartnersResultsId).contains(this.data.campus_partner2).click()
          .get(projectNameSearchField).should('exist').clear().type('testproject')
          .get(searchButton).click()
           // Partner Information
          .get('#lnk-create_project').should('be.visible').click()
          .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/create-Project/?p_name=testproject#step-1')
          
          .get(engagementTypeInputField).click()
          .get(engagementTypeResults).contains(this.data.engagement_type3).click()

          .get(saveDraftButton).should('be.visible').click()
          .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/draft-project-done/#step-1')
      })


      it('Test my projects saved in draft are editable and saved as draft again', function(){
        const projectsId = '#projectsnav',
          myProjectsHref = `a[href="/myProjects/"]`,
          projectNameInputField = '#id_project_name',
          saveDraftButton = `button[name="draft"]`
          cy.get(projectsId).should('exist').click()
            .get(myProjectsHref).should('exist').click()
            .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/myProjects/')
            .get('h3').contains("My Projects").should("be.visible")
            .get('td').contains('testproject').click()
            .get('a').contains('Edit').click({force: true})
            .get(projectNameInputField).clear().type('testprojectedited')
            .get(saveDraftButton).click({force: true})
            .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/draft-project-done/')
            .get('h3').contains('Thank You')          
      })

      it('Test my projects delete functionality', function(){
        const projectsId = '#projectsnav',
          myProjectsHref = `a[href="/myProjects/"]`
          cy.get(projectsId).should('exist').click()
            .get(myProjectsHref).should('exist').click()
            .url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/myProjects/')
            .get('h3').contains("My Projects").should("be.visible")
            .get('td').contains('testprojectedited').click()
            .get('a').contains('Delete').click({force: true})
          cy.on("window:confirm", (t) => {
                //verify text on pop-up
                expect(t).to.equal("Are you sure you want to delete this Project?");
             });
          cy.url().should('be.equal', 'https://uno-cpi-dev.herokuapp.com/myProjects/')    
      })
});