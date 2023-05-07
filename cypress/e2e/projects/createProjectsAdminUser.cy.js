import user from "../../support/commands.js";
import * as data from "../../fixtures/datareports.json";

describe('create projects admin user', () => {
beforeEach(() => {
    cy.on('uncaught:exception', (err) => {
      if(err.message.includes('is not a function') || err.message.includes('is not defined') ||  err.message.includes('scrollTop')
          || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
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
     
  //Verify the user is logged is as administrator

  it('Login as admin user and lands in My projects page', function () {
    cy.get('[data-cy="administrator"]').should('contain.text', 'Administrator')

  })
  //Visit Projects and create project
  it('Visit Projects and create project', function () {
    cy.checkProjectName()
    cy.get('[data-cy="projectnameinput"]').type(this.data.createproject_name6)
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
  //Verify created project is displaying under My projects
  it ('Verify created project under my projects', function () {
    cy.get('[data-cy="projectsnav"]').click()
    cy.contains('My Projects').click()
    cy.get('[data-cy="My projects"]').should('contain.text', 'My Projects')
    cy.get('#example_filter > label > .form-control').type(this.data.createproject_name6)
    cy.get('table').contains('td', this.data.createproject_name6).should('be.visible')
  })

  //Verify existing project name cannot be used
  it('Existing project name cannot be used for project creation', function () {
    cy.checkProjectName()
    cy.get('[data-cy="projectnameinput"]').type(this.data.createproject_name6)
    cy.get('.btn-secondary').dblclick()
    cy.get('.class1').should('have.text', this.data.createproject_name6)
    cy.get('[data-cy="projectnameinput"]').clear()
    cy.get('[data-cy="projectnameinput"]').type(this.data.createproject_name7)
    cy.get('.btn-secondary').dblclick();
    cy.get('[data-cy="createprojectbutton"]').click()
    cy.get('[data-cy="projectregistration"]').should('contain.text', 'Project Registration')
  })
  //Verify project name is mandatory
  it.skip('check Project name is a mandatory field', function () {
    cy.checkProjectName()
    cy.get('[data-cy="projectnameinput"]').type(this.data.createproject_name7)
    cy.get('.btn-secondary').click();
    cy.get('[data-cy="createprojectbutton"]').click()
    cy.get('#id_project_name').clear()
    cy.get('.sw-btn-next').click()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('Project Name Required');
    })
  })
  //Verify Engagement type is mandatory
  it('check Engagement type is a mandatory field', function () {
    cy.checkProjectName()
    cy.get('[data-cy="projectnameinput"]').type(this.data.createproject_name7)
    cy.get('.btn-secondary').click();
    cy.get('[data-cy="createprojectbutton"]').click()
    cy.get('.sw-btn-next').click()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('Engagement Type Required');
    })
  })
  //Verify description of project is mandatory
  it('check Description is a mandatory field', function () {
    cy.checkProjectName()
    cy.get('[data-cy="projectnameinput"]').type(this.data.createproject_name7)
    cy.get('.btn-secondary').click();
    cy.get('[data-cy="createprojectbutton"]').click()
    cy.get('#select2-id_engagement_type-container').click()
    cy.get('#select2-id_engagement_type-results').then(($li)=> {
      cy.wrap($li).contains(this.data.engagement_type3).click();
    })
    cy.get('.sw-btn-next').click()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('Project Description Required');
    })
  })
  //Verify Start semester is mandatory
  it('check start semester is a mandatory field', function () {
    cy.checkProjectName()
    cy.get('[data-cy="projectnameinput"]').type(this.data.createproject_name7)
    cy.get('.btn-secondary').click();
    cy.get('[data-cy="createprojectbutton"]').click()
    cy.get('#select2-id_engagement_type-container').click()
    cy.get('#select2-id_engagement_type-results').then(($li)=> {
      cy.wrap($li).contains(this.data.engagement_type3).click();
    })
    cy.get('[data-cy="descriptioninput"]').type(this.data._comment7)
    cy.get('.sw-btn-next').click()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('Project Start Semester Required');
    })
  })
  //Verify Start academic year is mandatory
  it('check start academic year is a mandatory field', function () {
    cy.checkProjectName()
    cy.get('[data-cy="projectnameinput"]').type(this.data.createproject_name7)
    cy.get('.btn-secondary').click();
    cy.get('[data-cy="createprojectbutton"]').click()
    cy.get('#select2-id_engagement_type-container').click()
    cy.get('#select2-id_engagement_type-results').then(($li)=> {
      cy.wrap($li).contains(this.data.engagement_type3).click();
    })
    cy.get('[data-cy="descriptioninput"]').type(this.data._comment7)
    cy.get('[data-cy="projectduration"] > .fa').click()
    cy.get('#select2-id_semester-container').click()
    cy.get('#select2-id_semester-results').then(($li)=> {
      cy.wrap($li).contains(this.data.semester1).click();
    })
    cy.get('.sw-btn-next').click()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('Project Start academic year Required');
    })
  })
  //Verify campus partner is mandatory
  it('check campus partner is a mandatory field', function () {
    cy.checkProjectName()
    cy.get('[data-cy="projectnameinput"]').type(this.data.createproject_name7)
    cy.get('.btn-secondary').click();
    cy.get('[data-cy="createprojectbutton"]').click()
    cy.projectInformation()
    cy.get('.sw-btn-next').dblclick()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('Campus Partner Required');
    })
  })
  //Verify focus area is mandatory
  it('check focus area is a mandatory field', function () {
    cy.checkProjectName()
    cy.get('[data-cy="projectnameinput"]').type(this.data.createproject_name7)
    cy.get('.btn-secondary').click();
    cy.get('[data-cy="createprojectbutton"]').click()
    cy.projectInformation()
    cy.get('.sw-btn-next').click()
    cy.get('[data-cy="campuspartnerinfo"]').click()
    cy.get('#id_campus-0-campus_partner').select(this.data.campus_partner3)
    cy.get('[data-cy="add-campus-row"]').click()
    cy.get('.sw-btn-next').dblclick()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('Primary Focus Area Required');
    })
  })
  //Verify alert when academic start year is greater than end year
  it('Check for an alert when end academic year is greater than start year', function () {
    cy.checkProjectName()
    cy.get('[data-cy="projectnameinput"]').type(this.data.createproject_name7)
    cy.get('.btn-secondary').click();
    cy.get('[data-cy="createprojectbutton"]').click()
    cy.get('#select2-id_engagement_type-container').click()
    cy.get('#select2-id_engagement_type-results').then(($li) => {
      cy.wrap($li).contains(this.data.engagement_type3).click();
    })
    cy.get('[data-cy="descriptioninput"]').type(this.data._comment7)
    cy.get('[data-cy="projectduration"]').click()
    cy.get('#select2-id_semester-container').click()
    cy.get('#select2-id_semester-results').then(($li) => {
      cy.wrap($li).contains(this.data.semester1).click();
    })
    cy.get('#select2-id_academic_year-container').click()
    cy.get('#select2-id_academic_year-results').then(($li) => {
      cy.wrap($li).contains(this.data.academic_year4).click();
    })
    cy.get('#select2-id_end_academic_year-container').click()
    cy.get('#select2-id_end_academic_year-results').then(($li) => {
      cy.wrap($li).contains(this.data.academic_year1).click();
    })
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('Project End Academic Year is before Project Start Academic Year');
    })
  })
  //Remove added community partner, campus partner and topic. Also check empty value cannot be added for topic
  it('check added community partner/campus partner/topic can be removed and empty value addition', function () {
    cy.checkProjectName()
    cy.get('[data-cy="projectnameinput"]').type(this.data.createproject_name7)
    cy.get('.btn-secondary').click();
    cy.get('[data-cy="createprojectbutton"]').click()
    cy.projectInformation()
    cy.get('.sw-btn-next').click()
    cy.get('#id_community-0-community_partner').select(this.data.community_partner1)
    cy.get('.add-community-row').click()
    cy.get('#id_community-1-community_partner').select(this.data.community_partner2)
    cy.get('.add-community-row').click()

    //remove added community partner
    cy.get(':nth-child(2) > .remove-community-row').click()
    cy.get('[data-cy="community-fields"]').contains(this.data.community_partner2).should('not.exist')
    cy.get('[data-cy="campuspartnerinfo"]').click()
    cy.get('#id_campus-0-campus_partner').select(data.campus_partner3)
    cy.get('.add-campus-row').click()
    cy.get('#id_campus-1-campus_partner').select(this.data.campus_partner6)
    cy.get('.add-campus-row').click()

    //remove added campus partner
    cy.get(':nth-child(2) > .remove-campus-row').click()
    cy.get('[data-cy="campus-fields"]').contains(this.data.campus_partner6).should('not.exist')
    cy.get('.sw-btn-next').click()
    cy.get('#id_sub_category-0-sub_category').select(this.data.topic1)
    cy.get('.add-sub_category-row').click()
    cy.get('#id_sub_category-1-sub_category').select(this.data.topic2)
    cy.get('.add-sub_category-row').click()

    //remove added topic
    cy.get(':nth-child(2) > .remove-sub_category-row').click()
    cy.get('[data-cy="sub_category-fields"]').contains(this.data.topic2).should('not.exist')

    //verify error when an empty value is added in topic
    cy.get('.add-sub_category-row').click()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('you cannot add empty value');
    })
  })
  //Verify pop up when selected topic is not added
  it('check for pop up when selected topic is not added ', function () {
    cy.checkProjectName()
    cy.get('[data-cy="projectnameinput"]').type(this.data.createproject_name7)
    cy.get('.btn-secondary').click();
    cy.get('[data-cy="createprojectbutton"]').click()
    cy.projectInformation()
    cy.get('.sw-btn-next').click()
    cy.partnersInformation()
    cy.get('#id_sub_category-0-sub_category').select(this.data.topic1)
    cy.get('[data-cy="add-sub_category_row"]').click()
    cy.get('#id_sub_category-1-sub_category').select(this.data.topic3)
    cy.get('.sw-btn-next').click()
    cy.on('window:alert', (txt) => {
      expect(txt).to.contains('Add selected Topic or clear selection');
    })
  })
  //Verify register community partner link is accessible
  it('check register community partner link ', function () {
    cy.checkProjectName()
    cy.get('[data-cy="projectnameinput"]').type(this.data.createproject_name7)
    cy.get('.btn-secondary').click();
    cy.get('[data-cy="createprojectbutton"]').click()
    cy.projectInformation()
    cy.get('.sw-btn-next').click()
    cy.get('#id_registerCommAndSave').click({force:true})
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('You will be redirected to Register Community Partner page. ' +
          'Upon Submission of the registration form, you will be redirected back to this page to ' +
          'finish creating a project. Are you sure you want to register a New Community Partner?');
    })
    cy.get('.heading').should('contain.text', 'Community Partner Registration')
  })
  //Verify register campus partner link is accessible
  it('check register campus partner link ', function () {
    cy.checkProjectName()
    cy.get('[data-cy="projectnameinput"]').type(this.data.createproject_name8)
    cy.get('.btn-secondary').click();
    cy.get('[data-cy="createprojectbutton"]').click()
    cy.projectInformation()
    cy.get('.sw-btn-next').click()
    cy.get('#campuspartnerinfonav').click()
    cy.get('#id_registerCampusAndSave').click()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('You will be redirected to Register Campus Partner page. ' +
          'Upon Submission of the registration form, you will be redirected back to this page to ' +
          'finish creating a project. Are you sure you want to register a New Campus Partner?');
    })
    cy.get('.heading').should('contain.text', 'Campus Partner Registration')
  })
  // Data cleanup script
  it('data cleanup', function() {
    cy.get('[data-cy="cpi"]').click()
    cy.get('[data-cy="projectsnav"]').click()
    cy.contains('My Projects').click()
    cy.get('#example_filter > label > .form-control').type(this.data.createproject_name6+'{enter}')
    cy.get('.sorting_1').should('contain',this.data.createproject_name6).click()
    cy.get('.dtr-data > .btn-cancel').click()
    cy.get('#example_filter > label > .form-control').clear()
    cy.get('#example_filter > label > .form-control').type(this.data.createproject_name6+'{enter}')
    cy.get('#example_info').should('contain','Showing 0 to 0 of 0 entries')
    cy.get('#example_filter > label > .form-control').clear()
    cy.get('[data-cy="cpi"]').click()
    cy.get('[data-cy="projectsnav"]').click()
    cy.contains('My Drafts').click()
    cy.get('#example_filter > label > .form-control').type(this.data.createproject_name7+'{enter}')
    cy.get('.sorting_1').should('contain',this.data.createproject_name7).click()
    cy.get('.dtr-data > .btn-cancel').click()
    cy.get('#example_filter > label > .form-control').clear()
    cy.get('#example_filter > label > .form-control').type(this.data.createproject_name7+'{enter}')
    cy.get('#example_info').should('contain','Showing 0 to 0 of 0 entries')
    cy.get('#example_filter > label > .form-control').clear()
    cy.get('#example_filter > label > .form-control').type(this.data.createproject_name8+'{enter}')
    cy.get('.sorting_1').should('contain',this.data.createproject_name8).click()
    cy.get('.dtr-data > .btn-cancel').click()
    cy.get('#example_filter > label > .form-control').clear()
    cy.get('#example_filter > label > .form-control').type(this.data.createproject_name8+'{enter}')
    cy.get('#example_info').should('contain','Showing 0 to 0 of 0 entries')
  })
})