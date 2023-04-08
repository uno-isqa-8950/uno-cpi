import user from "../../support/commands.js";
describe('my projects admin user test', () => {
beforeEach(() => {
    cy.on('uncaught:exception', (err) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'options\'') || err.message.includes('reading \'scrollTop\'') || err.message.includes('reading \'addEventListener\'')|| err.message.includes('null (reading \'style\')'))
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

      it('Visit Projects and create project', function () {
        cy.checkProjectName()
        cy.get('[data-cy="projectnameinput"]').type(this.data.createproject_name1)
        cy.get('[data-cy="search"]').click();
        cy.get('[data-cy="button-id"]').should('contain','The project that you are searching for does not exist, to proceed with the creation of a new project, click on the above button.')
        cy.get('[data-cy="createprojectbutton"]').should('be.visible').click()
        cy.get('#select2-id_engagement_type-container').click()
        cy.get('#select2-id_engagement_type-results').then(($li)=> {
          cy.wrap($li).contains(this.data.engagement_type3).click();
        })
        //cy.get('#select2-id_populate_activity-container').click().wait(3000)
        //cy.get('#select2-id_populate_activity-results').then(($li)=> {
         // cy.wrap($li).contains(this.data.activity_type1).click();
        //})
        cy.get('[data-cy="descriptioninput"]').type("This is a description of a project.")
        cy.get('[data-cy="projectduration"] > .fa').click()
        cy.get('#select2-id_project_type-container').click()
        cy.get('#select2-id_project_type-results').then(($li) => {
            cy.wrap($li).contains('Project').click();
        })
        cy.get('#select2-id_semester-container').click()
        cy.get('#select2-id_semester-results').then(($li)=> {
          cy.wrap($li).contains(this.data.semester1).click();
        })
        cy.get('#select2-id_end_semester-container').click()
        cy.get('#select2-id_end_semester-results').then(($li)=> {
          cy.wrap($li).contains(this.data.semester1).click();
        })
        cy.get('#select2-id_academic_year-container').click()
        cy.get('#select2-id_academic_year-results').then(($li)=> {
          cy.wrap($li).contains(this.data.academic_year1).click();
        })
        cy.get('#select2-id_end_academic_year-container').click()
        cy.get('#select2-id_end_academic_year-results').then(($li)=> {
          cy.wrap($li).contains(this.data.academic_year4).click();
        })
        cy.get('[data-cy="participantinformation"]').click()
        cy.get('#id_total_uno_students').type(this.data.total_UNO_student1)
        cy.get('#id_total_uno_hours').type(this.data.total_UNO_student_hour1)
        cy.get('#id_total_other_community_members').type(this.data.total_other_participants)
        cy.get('#id_k12_flag').click()
        cy.get('#id_total_k12_students').type(this.data.total_UNO_student1)
        cy.get('#id_total_k12_hours').type(this.data.total_UNO_student_hour1)
        cy.get('.sw-btn-next').click()
        cy.get('#id_community-0-community_partner').select(this.data.community_partner1)
        cy.get('[data-cy="clicktoaddselectedcommunitypartnervalue"]').click()
        cy.get('[data-cy="campuspartnerinfo"]').click()
        cy.get('#id_campus-0-campus_partner').select(this.data.campus_partner3)
        cy.get('[data-cy="add-campus-row"]').click()
        cy.get('[data-cy="campusstaffandorfacultylead"]').click()
        cy.get('[data-cy="firstname"]').type(this.data.campuspartner1_firstname)
        cy.get('[data-cy="lastname"]').type(this.data.campuspartner1_lastname)
        cy.get('[data-cy="clicktoaddgivenvalue"]').click()
        cy.get('.sw-btn-next').click()
        cy.get('#id_mission-0-mission').select(this.data.focus_area1)
        cy.get('#id_sub_category-0-sub_category').select(this.data.topic1)
        cy.get('[data-cy="add-sub_category_row"]').click()
        cy.get('.sw-btn-next').click()
        cy.get('[data-cy="projectaddress"]').type(this.data.addressline)
        cy.get('[data-cy="projectcity"]').type(this.data.city)
        cy.get('[data-cy="projectcountry"]').type(this.data.country)
        cy.get('[data-cy="projectstate"]').type(this.data.province)
        cy.get('[data-cy="projectzip"]').type(this.data.zipcode)
        cy.get('#termsdiv > p').should('contain', "I agree to the Terms")
        cy.get('[data-cy="checkbox"]').click()
        cy.get('[data-cy="submit"]').click()
      })

       it('Test projects in my projects page are editable', function(){
        const projectsLink = '[data-cy="projectsnav"]',
          myProjectsLink = '[data-cy="myprojects"]',
          projectNameInputField = '[data-cy="projectnameinput"]',
          step4 = '[data-cy="step4"]',
          termsCheck =  '[data-cy="terms"]',
          updateButton = '[data-cy="update"]'
          cy.get(projectsLink).should('exist').click()
            .get(myProjectsLink).should('exist').click()
            .url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
            .get('h3').contains("My Projects").should("be.visible")
            .get('td').contains(this.data.createproject_name1).click()
            .get('a').contains('Edit').click({force: true})
            .get('[data-cy="projectnameinput"]').type('edited')
            .get('button').contains('Next').dblclick()
            .get('button').contains('Next').dblclick()
            .get('button').contains('Next').dblclick()
            .get('button').contains('Next').dblclick()
            .get(step4).click()
            .get(termsCheck).eq(0).click()
            .get(updateButton).click({force:true})
            .url().should('be.equal', Cypress.env('baseUrl')+'adminsubmit_project_done/')
            .get('h3').contains('Thank You')
       })

      it('Test my projects delete functionality', function(){
        const projectsLink = '[data-cy="projectsnav"]',
        myProjectsLink = '[data-cy="myprojects"]'
          cy.get(projectsLink).should('exist').click()
            .get(myProjectsLink).should('exist').click()
            .url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')
            .get('h3').contains("My Projects").should("be.visible")
            .get('td').contains('edited').click()
            .get('a').contains('Delete').click({force: true})
          cy.on("window:confirm", (t) => {
                //verify text on pop-up
                expect(t).to.equal("Are you sure you want to delete this Project?");
             });
          cy.url().should('be.equal', Cypress.env('baseUrl')+'myProjects/')    
      })
});
