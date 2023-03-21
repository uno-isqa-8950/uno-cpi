import user from "../../support/commands.js";
import * as data from "../../fixtures/datareports.json";
beforeEach(() => {
  cy.on('uncaught:exception', (err, runnable) => {
    if(err.message.includes('is not a function') ||err.message.includes('Cannot read properties of null') ||err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
    {
      return false
    }
  })
  cy.visit(Cypress.env('baseUrl'))

})

describe ('Create projects for campus partner user', () => {
  beforeEach(function () {
    cy.fixture("datareports").then(function (data) {
      this.data = data
    cy.get('#login').click()
      .loginCampusUser(user)
    })
  })
  //Verify campus user login landed in My projects
  it ('Login as campus partner and lands in My projects page', function () {
    cy.get('.heading').should('contain.text', 'My Projects')

  })
  //Visit Projects and create project
  it ('Visit Projects and create project', function () {
    cy.checkProjectName()
    cy.get('#projectName').type(this.data.createproject_name1)
    cy.get('.btn-secondary').click();
    cy.get('#lnk-create_project').click()
    cy.get('#select2-id_engagement_type-container').click()
    cy.get('#select2-id_engagement_type-results').then(($li)=> {
      cy.wrap($li).contains(this.data.engagement_type3).click();
    })
    //cy.get('#select2-id_populate_activity-container').click().wait(3000)
    //cy.get('#select2-id_populate_activity-results').then(($li)=> {
     // cy.wrap($li).contains(this.data.activity_type1).click();
    //})
    cy.get('#id_description').type(this.data._comment7)
    cy.get('#projectdurationnav').click()
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
    cy.get('#participantinfonav').click()
    cy.get('#id_total_uno_students').type(this.data.total_UNO_student1)
    cy.get('#id_total_uno_hours').type(this.data.total_UNO_student_hour1)
    cy.get('#id_total_other_community_members').type(this.data.total_other_participants)
    cy.get('#id_k12_flag').click()
    cy.get('#id_total_k12_students').type(this.data.total_UNO_student1)
    cy.get('#id_total_k12_hours').type(this.data.total_UNO_student_hour1)
    cy.get('.sw-btn-next').click()
    cy.get('#id_community-0-community_partner').select(this.data.community_partner1)
    cy.get('.add-community-row').click()
    cy.get('#campuspartnerinfonav').click()
    cy.get('#id_campus-0-campus_partner').select(this.data.campus_partner3)
    cy.get('.add-campus-row').click()
    cy.get('[href="#leadstaffinfo"]').click()
    cy.get('#firstname').type(this.data.campuspartner1_firstname)
    cy.get('#lastname').type(this.data.campuspartner1_lastname)
    cy.get('#submitname').click()
    cy.get('.sw-btn-next').click()
    cy.get('#id_mission-0-mission').select(this.data.focus_area1)
    cy.get('#id_sub_category-0-sub_category').select(this.data.topic1)
    cy.get('.add-sub_category-row').click()
    cy.get('.sw-btn-next').click()
    cy.get('#id_address_line1').type(this.data.addressline)
    cy.get('#id_city').type(this.data.city)
    cy.get('#id_country').type(this.data.country)
    cy.get('#id_state').type(this.data.province)
    cy.get('#id_zip').type(this.data.zipcode)
    cy.get('#terms').click()
    cy.get('#submit').click()
  })
  //Verify created project is displaying under My projects
  it ('Verify created project under my projects', function () {
    cy.get('#projectsnav').contains('Projects').click()
    cy.contains('My Projects').click()
    cy.get('.heading').should('contain.text', 'My Projects')
    cy.get('#example_filter > label > .form-control').type(this.data.createproject_name1)
    cy.get('table').contains('td', this.data.createproject_name1).should('be.visible')
  })

  //Verify existing project name cannot be used
  it ('Existing project name cannot be used for project creation', function () {
    cy.checkProjectName()
    cy.get('#projectName').type(this.data.createproject_name1)
    cy.get('.btn-secondary').click();
    cy.get('.btn-secondary').click();
    cy.get('.class1').should('have.text', this.data.createproject_name1)
    cy.get('#projectName').clear()
    cy.get('#projectName').type(this.data.createproject_name2)
    cy.get('.btn-secondary').click();
    cy.get('.btn-secondary').click();
    cy.get('#lnk-create_project').click()
    cy.get('.heading').should('contain.text', 'Project Registration')
  })
  //Verify project name is mandatory
  it ('check Project name is a mandatory field', function () {
    cy.checkProjectName()
    cy.get('#projectName').type(this.data.createproject_name2)
    cy.get('.btn-secondary').click();
    cy.get('#lnk-create_project').click()
    cy.get('#id_project_name').clear()
    cy.get('.sw-btn-next').click()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('Project Name Required');
    })
  })
  //Verify Engagement type is mandatory
  it ('check Engagement type is a mandatory field', function () {
    cy.checkProjectName()
    cy.get('#projectName').type(this.data.createproject_name2)
    cy.get('.btn-secondary').click();
    cy.get('#lnk-create_project').click()
    cy.get('.sw-btn-next').click()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('Engagement Type Required');
    })
  })
  //Verify description of project is mandatory
  it ('check Description is a mandatory field', function () {
    cy.checkProjectName()
    cy.get('#projectName').type(this.data.createproject_name2)
    cy.get('.btn-secondary').click();
    cy.get('#lnk-create_project').click()
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
  it ('check start semester is a mandatory field', function () {
    cy.checkProjectName()
    cy.get('#projectName').type(this.data.createproject_name2)
    cy.get('.btn-secondary').click();
    cy.get('#lnk-create_project').click()
    cy.get('#select2-id_engagement_type-container').click()
    cy.get('#select2-id_engagement_type-results').then(($li)=> {
      cy.wrap($li).contains(this.data.engagement_type3).click();
    })
    cy.get('#id_description').type(this.data._comment7)
    cy.get('.sw-btn-next').click()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('Project Start Semester Required');
    })
  })
  //Verify Start academic year is mandatory
  it ('check start academic year is a mandatory field', function () {
    cy.checkProjectName()
    cy.get('#projectName').type(this.data.createproject_name2)
    cy.get('.btn-secondary').click();
    cy.get('#lnk-create_project').click()
    cy.get('#select2-id_engagement_type-container').click()
    cy.get('#select2-id_engagement_type-results').then(($li)=> {
      cy.wrap($li).contains(this.data.engagement_type3).click();
    })
    cy.get('#id_description').type(this.data._comment7)
    cy.get('#projectdurationnav').click()
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
  it ('check campus partner is a mandatory field', function () {
    cy.checkProjectName()
    cy.get('#projectName').type(this.data.createproject_name2)
    cy.get('.btn-secondary').click();
    cy.get('#lnk-create_project').click()
    cy.projectInformation()
    cy.get('.sw-btn-next').click()
    cy.get('.sw-btn-next').click()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('Campus Partner Required');
    })
  })
  //Verify focus area is mandatory
  it ('check focus area is a mandatory field', function () {
    cy.checkProjectName()
    cy.get('#projectName').type(this.data.createproject_name2)
    cy.get('.btn-secondary').click();
    cy.get('#lnk-create_project').click()
    cy.projectInformation()
    cy.get('.sw-btn-next').click()
    cy.get('#campuspartnerinfonav').click()
    cy.get('#id_campus-0-campus_partner').select(this.data.campus_partner3)
    cy.get('.add-campus-row').click()
    cy.get('.sw-btn-next').click()
    cy.get('.sw-btn-next').click()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('Primary Focus Area Required');
    })
  })
  //Verify alert when academic start year is greater than end year
  it ('Check for an alert when end academic year is greater than start year', function () {
    cy.checkProjectName()
    cy.get('#projectName').type(this.data.createproject_name2)
    cy.get('.btn-secondary').click();
    cy.get('#lnk-create_project').click()
    cy.get('#select2-id_engagement_type-container').click()
    cy.get('#select2-id_engagement_type-results').then(($li) => {
      cy.wrap($li).contains(this.data.engagement_type3).click();
    })
    cy.get('#id_description').type(this.data._comment7)
    cy.get('#projectdurationnav').click()
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
  it ('check added community partner/campus partner/topic can be removed and empty value addition', function () {
    cy.checkProjectName()
    cy.get('#projectName').type(this.data.createproject_name2)
    cy.get('.btn-secondary').click();
    cy.get('#lnk-create_project').click()
    cy.projectInformation()
    cy.get('.sw-btn-next').click()
    cy.get('#id_community-0-community_partner').select(this.data.community_partner1)
    cy.get('.add-community-row').click()
    cy.get('#id_community-1-community_partner').select(this.data.community_partner2)
    cy.get('.add-community-row').click()

    //remove added community partner
    cy.get(':nth-child(2) > .remove-community-row').click()
    cy.get('#community-fields').contains(this.data.community_partner2).should('not.exist')
    cy.get('#campuspartnerinfonav').click()
    cy.get('#id_campus-0-campus_partner').select(this.data.campus_partner3)
    cy.get('.add-campus-row').click()
    cy.get('#id_campus-1-campus_partner').select(this.data.campus_partner6)
    cy.get('.add-campus-row').click()

    //remove added campus partner
    cy.get(':nth-child(2) > .remove-campus-row').click()
    cy.get('#campus-fields').contains(this.data.campus_partner6).should('not.exist')
    cy.get('.sw-btn-next').click()
    cy.get('#id_sub_category-0-sub_category').select(this.data.topic1)
    cy.get('.add-sub_category-row').click()
    cy.get('#id_sub_category-1-sub_category').select(this.data.topic2)
    cy.get('.add-sub_category-row').click()

    //remove added topic
    cy.get(':nth-child(2) > .remove-sub_category-row').click()
    cy.get('#sub_category-fields').contains(this.data.topic2).should('not.exist')

    //verify error when an empty value is added in topic
    cy.get('.add-sub_category-row').click()
    cy.on('window:alert',(txt)=>{
      expect(txt).to.contains('you cannot add empty value');
    })
  })
  //Verify pop up when selected topic is not added
  it ('check for pop up when selected topic is not added ', function () {
    cy.checkProjectName()
    cy.get('#projectName').type(this.data.createproject_name2)
    cy.get('.btn-secondary').click();
    cy.get('#lnk-create_project').click()
    cy.projectInformation()
    cy.get('.sw-btn-next').click()
    cy.partnersInformation()
    cy.get('#id_sub_category-0-sub_category').select(this.data.topic1)
    cy.get('.add-sub_category-row').click()
    cy.get('#id_sub_category-1-sub_category').select(this.data.topic3)
    cy.get('.sw-btn-next').click()
    cy.on('window:alert', (txt) => {
      expect(txt).to.contains('Add selected Topic or clear selection');
    })
  })
  //Verify register community partner link is accessible
  it.skip('check register community partner link ', function () {
    cy.checkProjectName()
    cy.get('#projectName').type(this.data.createproject_name2)
    cy.get('.btn-secondary').click();
    //cy.get('.btn-secondary').click();
    cy.get('#lnk-create_project').click()
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
  it.skip ('check register campus partner link ', function () {
    cy.checkProjectName()
    cy.get('#projectName').type(this.data.createproject_name3)
    cy.get('.btn-secondary').click();
    cy.get('#lnk-create_project').click()
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

  it ('data cleanup', function() {
    cy.url().should('be.equal', this.data.CEPI_site+'myProjects/')
    cy.get('#uno').click()
    cy.get('#projectsnav').click()
    cy.contains('My Projects').click()
    cy.get('#example_filter > label > .form-control').type(this.data.createproject_name1+'{enter}')
    cy.get('.sorting_1').should('contain',this.data.createproject_name1).click()
    cy.get('.dtr-data > .btn-cancel').click()
    cy.get('#example_filter > label > .form-control').clear()
    cy.get('#example_filter > label > .form-control').type(this.data.createproject_name1+'{enter}')
    cy.get('#example_info').should('contain','Showing 0 to 0 of 0 entries')
    cy.get('#example_filter > label > .form-control').clear()
    /*cy.get('#example_filter > label > .form-control').type(this.data.createproject_name2+'{enter}')
    cy.get('.sorting_1').should('contain',this.data.createproject_name2).click()
    cy.get('.dtr-data > .btn-cancel').click()
    cy.get('#example_filter > label > .form-control').clear()
    cy.get('#example_filter > label > .form-control').type(this.data.createproject_name2+'{enter}')
    cy.get('#example_info').should('contain','Showing 0 to 0 of 0 entries')
    cy.get('#example_filter > label > .form-control').clear()
    cy.get('#example_filter > label > .form-control').type(this.data.createproject_name3+'{enter}')
    cy.get('.sorting_1').should('contain',this.data.createproject_name3).click()
    cy.get('.dtr-data > .btn-cancel').click()
    cy.get('#example_filter > label > .form-control').clear()
    cy.get('#example_filter > label > .form-control').type(this.data.createproject_name3+'{enter}')
    cy.get('#example_info').should('contain','Showing 0 to 0 of 0 entries')*/
  })
})