import user from "../../../../support/commands"

describe("Display snippets", () => {
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

        cy.loginAdminUser(user)
        cy.visit(Cypress.env('baseUrl'))
    })

    const cmsHref = `a[href="/cms/"]`,
        administratorLink = '[data-cy="administrator"]',
        cmsItemSnippets = '.sidebar-main-menu__list > :nth-child(4) > .sidebar-menu-item__link > .menuitem > .menuitem-label',
        saveSnippet = '.dropdown > .button',
        editSnippet = ':nth-child(1) > .title > .title-wrapper > a',
        deleteCms = ':nth-child(1) > .bulk-action-checkbox-cell > .bulk-action-checkbox',
        snippetDelete = '.bulk-action-btn',
        deleteButtonAll = '.serious',
        success = '.success',
        allProjectsPageSnippets = 'a[href="/cms/snippets/home/all_projects_snippet/"]',
        allInputTextSnippet = '#id_text',
        campusPartnerSnippet = 'a[href="/cms/snippets/home/campus_partner_snippet/"]',
        campusPartnerUserSnippet = 'a[href="/cms/snippets/home/campus_partner_user_snippet/"]',
        communityPartnerProjectSnippet = 'a[href="/cms/snippets/home/community_partner_project_snippet/"]',
        communityPartnerSnippet = 'a[href="/cms/snippets/home/community_partner_snippet/"]',
        communityPartnerUserSnippet = 'a[href="/cms/snippets/home/community_partner_user_snippet/"]',
        communityPrivateReportSnippet = 'a[href="/cms/snippets/home/community_private_report_snippet/"]',
        communityPublicReportSnippet = 'a[href="/cms/snippets/home/community_public_report_snippet/"]',
        createProjectsFormSnippet = 'a[href="/cms/snippets/home/create_projects_form_snippet/"]',
        createProjectsSearchPageSnippet = 'a[href="/cms/snippets/home/create_projects_snippet/"]',
        editProjectFormSnippet = 'a[href="/cms/snippets/home/edit_projects_form_snippet/"]'

    it('Can navigate to cms', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()
    })

    //Snippet for all projects page
    it('Can add a snippet for all projects page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(allProjectsPageSnippets).click()
            .url().should('include', '/cms/snippets/home/all_projects_snippet/')
        cy.contains('Add All Projects Page Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.all_project_snippet_text1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("All Projects Page Snippet 'Adding a project page snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for all projects page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(allProjectsPageSnippets).click()
            .url().should('include', '/cms/snippets/home/all_projects_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.all_project_snippet_text2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("All Projects Page Snippet 'Editing a project page snippet' updated.")
            .should('be.visible')
    })

    it('Can delete a snippet for all projects page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(allProjectsPageSnippets).click()
            .url().should('include', '/cms/snippets/home/all_projects_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("All Projects Page Snippet 'Editing a project page snippet' deleted")
            .should('be.visible')
    })

    //Snippet for campus partner
    it('Can add a snippet for campus partner', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(campusPartnerSnippet).click()
            .url().should('include', '/cms/snippets/home/campus_partner_snippet/')
        cy.contains('Add Campus Partner Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.campus_partner_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Campus Partner Snippet 'Adding a campus partner snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for campus partner', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(campusPartnerSnippet).click()
            .url().should('include', '/cms/snippets/home/campus_partner_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.campus_partner_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Campus Partner Snippet 'Editing a campus partner snippet' updated.")
            .should('be.visible')
    })

    it('Can delete a snippet for campus partner', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(campusPartnerSnippet).click()
            .url().should('include', '/cms/snippets/home/campus_partner_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Campus Partner Snippet 'Editing a campus partner snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for campus partner user
    it('Can add a snippet for campus partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(campusPartnerUserSnippet).click()
            .url().should('include', '/cms/snippets/home/campus_partner_user_snippet/')
        cy.contains('Add Campus Partner User Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.campus_partner_user_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Campus Partner User Snippet 'Adding a campus partner user snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for campus partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(campusPartnerUserSnippet).click()
            .url().should('include', '/cms/snippets/home/campus_partner_user_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.campus_partner_user_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Campus Partner User Snippet 'Editing a campus partner user snippet' updated.")
            .should('be.visible')
    })

    it('Can delete a snippet for campus partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(campusPartnerUserSnippet).click()
            .url().should('include', '/cms/snippets/home/campus_partner_user_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Campus Partner User Snippet 'Editing a campus partner user snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for community partner project
    it('Can add a snippet for community partner project', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(communityPartnerProjectSnippet).click()
            .url().should('include', '/cms/snippets/home/community_partner_project_snippet/')
        cy.contains('Add Community Partner Project Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.community_partner_project_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Community Partner Project Snippet 'Adding a community partner project snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for community partner project', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(communityPartnerProjectSnippet).click()
            .url().should('include', '/cms/snippets/home/community_partner_project_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.community_partner_project_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Community Partner Project Snippet 'Editing a community partner project snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for community partner project', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(communityPartnerProjectSnippet).click()
            .url().should('include', '/cms/snippets/home/community_partner_project_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Community Partner Project Snippet 'Editing a community partner project snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for community partner
    it('Can add a snippet for community partner', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(communityPartnerSnippet).click()
            .url().should('include', '/cms/snippets/home/community_partner_snippet/')
        cy.contains('Add Community Partner Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.community_partner_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Community Partner Snippet 'Adding a community partner snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for community partner', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(communityPartnerSnippet).click()
            .url().should('include', '/cms/snippets/home/community_partner_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.community_partner_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Community Partner Snippet 'Editing a community partner snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for community partner', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(communityPartnerSnippet).click()
            .url().should('include', '/cms/snippets/home/community_partner_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Community Partner Snippet 'Editing a community partner snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for community partner user
    it('Can add a snippet for community partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(communityPartnerUserSnippet).click()
            .url().should('include', '/cms/snippets/home/community_partner_user_snippet/')
        cy.contains('Add Community Partner User Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.community_partner_user_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Community Partner User Snippet 'Adding a community partner user snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for community partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(communityPartnerUserSnippet).click()
            .url().should('include', '/cms/snippets/home/community_partner_user_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.community_partner_user_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Community Partner User Snippet 'Editing a community partner user snippet' updated.")
            .should('be.visible')
    })

    it('Can delete a snippet for community partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(communityPartnerUserSnippet).click()
            .url().should('include', '/cms/snippets/home/community_partner_user_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Community Partner User Snippet 'Editing a community partner user snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for community private report
    it('Can add a snippet for community private report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(communityPrivateReportSnippet).click()
            .url().should('include', '/cms/snippets/home/community_private_report_snippet/')
        cy.contains('Add Community Private Report Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.community_private_report_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Community Private Report Snippet 'Adding a community private report snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for community private report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(communityPrivateReportSnippet).click()
            .url().should('include', '/cms/snippets/home/community_private_report_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.community_private_report_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Community Private Report Snippet 'Editing a community private report snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for community private report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(communityPrivateReportSnippet).click()
            .url().should('include', '/cms/snippets/home/community_private_report_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Community Private Report Snippet 'Editing a community private report snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for community public report
    it('Can add a snippet for community public report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(communityPublicReportSnippet).click()
            .url().should('include', '/cms/snippets/home/community_public_report_snippet/')
        cy.contains('Add Community Public Report Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.community_public_report_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Community Public Report Snippet 'Adding a community public report snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for community public report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(communityPublicReportSnippet).click()
            .url().should('include', '/cms/snippets/home/community_public_report_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.community_public_report_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Community Public Report Snippet 'Editing a community public report snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for community public report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(communityPublicReportSnippet).click()
            .url().should('include', '/cms/snippets/home/community_public_report_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Community Public Report Snippet 'Editing a community public report snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for creating a project form
    it('Can add a snippet for creating a project form', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(createProjectsFormSnippet).click()
            .url().should('include', '/cms/snippets/home/create_projects_form_snippet/')
        cy.contains('Add Create Projects Form Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.create_projects_form_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Create Projects Form Snippet 'Adding a create project form snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for creating a project form', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(createProjectsFormSnippet).click()
            .url().should('include', '/cms/snippets/home/create_projects_form_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.create_projects_form_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Create Projects Form Snippet 'Editing a create project form snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for creating a project form', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(createProjectsFormSnippet).click()
            .url().should('include', '/cms/snippets/home/create_projects_form_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Create Projects Form Snippet 'Editing a create project form snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for creating projects search page
    it('Can add a snippet for creating projects search page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(createProjectsSearchPageSnippet).click()
            .url().should('include', '/cms/snippets/home/create_projects_snippet/')
        cy.contains('Add Create Projects Search Page Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.create_projects_search_page_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Create Projects Search Page Snippet 'Adding a create project search page snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for creating a project search page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(createProjectsSearchPageSnippet).click()
            .url().should('include', '/cms/snippets/home/create_projects_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.create_projects_search_page_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Create Projects Search Page Snippet 'Editing a create project search page snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for creating a project search page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(createProjectsSearchPageSnippet).click()
            .url().should('include', '/cms/snippets/home/create_projects_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Create Projects Search Page Snippet 'Editing a create project search page snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for edit project form
    it('Can add a snippet for editing project form', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(editProjectFormSnippet).click()
            .url().should('include', '/cms/snippets/home/edit_projects_form_snippet/')
        cy.contains('Add Edit Projects Form Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.edit_project_form_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Edit Projects Form Snippet 'Adding an edit project form snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for editing project form', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(editProjectFormSnippet).click()
            .url().should('include', '/cms/snippets/home/edit_projects_form_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.edit_project_form_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Edit Projects Form Snippet 'Editing an edit project form snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for editing project form', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(editProjectFormSnippet).click()
            .url().should('include', '/cms/snippets/home/edit_projects_form_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Edit Projects Form Snippet 'Editing an edit project form snippet' deleted.")
            .should('be.visible')
    })


})


