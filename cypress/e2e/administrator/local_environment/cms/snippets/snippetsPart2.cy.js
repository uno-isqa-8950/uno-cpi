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
        allInputTextSnippet = '#id_text',
        engagementTypesChartSnippet = 'a[href="/cms/snippets/home/engagement_types_chart_snippet/"]',
        engagementTypesReportSnippet = 'a[href="/cms/snippets/home/engagement_types_report_snippet/"]',
        issueAddressAnalysisChartsSnippet = 'a[href="/cms/snippets/home/issue_address_chart_snippet/"]',
        loginSnippet = 'a[href="/cms/snippets/home/login_snippet/"]',
        logoutSnippet = 'a[href="/cms/snippets/home/logout_snippet/"]',
        missionAreasChartsSnippet = 'a[href="/cms/snippets/home/mission_areas_chart_snippet/"]',
        missionAreasReportSnippet = 'a[href="/cms/snippets/home/mission_areas_report_snippet/"]',
        myProjectsPageSnippet = 'a[href="/cms/snippets/home/my_projects_snippet/"]',
        networkAnalysisChartsSnippet = 'a[href="/cms/snippets/home/network_analysis_chart_snippet/"]',
        partnersOrganizationProfileContactsSnippet =
            'a[href="/cms/snippets/home/partners_organizatiion_profile_contacts_snippet/"]'

    it('Can navigate to cms', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()
    })

    //Snippet for engagement types chart
    it('Can add a snippet for engagement types chart', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(engagementTypesChartSnippet).click()
            .url().should('include', '/cms/snippets/home/engagement_types_chart_snippet/')
        cy.contains('Add Engagement Types Chart Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.engagement_types_chart_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Engagement Types Chart Snippet 'Adding an engagement types chart snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for engagement types chart', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(engagementTypesChartSnippet).click()
            .url().should('include', '/cms/snippets/home/engagement_types_chart_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.engagement_types_chart_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Engagement Types Chart Snippet 'Editing an engagement types chart snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for engagement types chart', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(engagementTypesChartSnippet).click()
            .url().should('include', '/cms/snippets/home/engagement_types_chart_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Engagement Types Chart Snippet 'Editing an engagement types chart snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for engagement types report
    it('Can add a snippet for engagement types report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(engagementTypesReportSnippet).click()
            .url().should('include', '/cms/snippets/home/engagement_types_report_snippet/')
        cy.contains('Add Engagement Types Report Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.engagement_types_report_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Engagement Types Report Snippet 'Adding an engagement types report snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for engagement types report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(engagementTypesReportSnippet).click()
            .url().should('include', '/cms/snippets/home/engagement_types_report_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.engagement_types_report_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Engagement Types Report Snippet 'Editing an engagement types report snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for engagement types report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(engagementTypesReportSnippet).click()
            .url().should('include', '/cms/snippets/home/engagement_types_report_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Engagement Types Report Snippet 'Editing an engagement types report snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for issue address analysis charts
    it('Can add a snippet for issue address analysis charts', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(issueAddressAnalysisChartsSnippet).click()
            .url().should('include', '/cms/snippets/home/issue_address_chart_snippet/')
        cy.contains('Add Issue Address Analysis Charts Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.issue_address_analysis_charts_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success).should('be.visible')
    })

    it('Can edit a snippet for issue address analysis charts', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(issueAddressAnalysisChartsSnippet).click()
            .url().should('include', '/cms/snippets/home/issue_address_chart_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.issue_address_analysis_charts_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success).should('be.visible')
    })

    it('Can delete a snippet for issue address analysis charts', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(issueAddressAnalysisChartsSnippet).click()
            .url().should('include', '/cms/snippets/home/issue_address_chart_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success).should('be.visible')
    })

    //Snippet for login
    it('Can add a snippet for login', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(loginSnippet).click()
            .url().should('include', '/cms/snippets/home/login_snippet/')
        cy.contains('Add Login Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.login_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Login Snippet 'Adding a login snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for login', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(loginSnippet).click()
            .url().should('include', '/cms/snippets/home/login_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.login_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Login Snippet 'Editing a login snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for login', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(loginSnippet).click()
            .url().should('include', '/cms/snippets/home/login_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Login Snippet 'Editing a login snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for logout
    it('Can add a snippet for logout', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(logoutSnippet).click()
            .url().should('include', '/cms/snippets/home/logout_snippet/')
        cy.contains('Add Logout Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.logout_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Logout Snippet 'Adding a logout snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for logout', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(logoutSnippet).click()
            .url().should('include', '/cms/snippets/home/logout_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.logout_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Logout Snippet 'Editing a logout snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for logout', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(logoutSnippet).click()
            .url().should('include', '/cms/snippets/home/logout_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Logout Snippet 'Editing a logout snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for mission areas charts
    it('Can add a snippet for mission areas charts', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(missionAreasChartsSnippet).click()
            .url().should('include', '/cms/snippets/home/mission_areas_chart_snippet/')
        cy.contains('Add Mission Areas Charts Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.mission_areas_charts_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Mission Areas Charts Snippet 'Adding a mission areas charts snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for mission areas charts', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(missionAreasChartsSnippet).click()
            .url().should('include', '/cms/snippets/home/mission_areas_chart_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.mission_areas_charts_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Mission Areas Charts Snippet 'Editing a mission areas charts snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for mission areas charts', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(missionAreasChartsSnippet).click()
            .url().should('include', '/cms/snippets/home/mission_areas_chart_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Mission Areas Charts Snippet 'Editing a mission areas charts snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for mission areas report
    it('Can add a snippet for mission areas report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(missionAreasReportSnippet).click()
            .url().should('include', '/cms/snippets/home/mission_areas_report_snippet/')
        cy.contains('Add Mission Areas Report Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.mission_areas_report_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Mission Areas Report Snippet 'Adding a mission areas report snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for mission areas report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(missionAreasReportSnippet).click()
            .url().should('include', '/cms/snippets/home/mission_areas_report_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.mission_areas_report_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Mission Areas Report Snippet 'Editing a mission areas report snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for mission areas report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(missionAreasReportSnippet).click()
            .url().should('include', '/cms/snippets/home/mission_areas_report_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Mission Areas Report Snippet 'Editing a mission areas report snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for my projects page
    it('Can add a snippet for my projects page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(myProjectsPageSnippet).click()
            .url().should('include', '/cms/snippets/home/my_projects_snippet/')
        cy.contains('Add My Projects Page Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.my_projects_page_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("My Projects Page Snippet 'Adding my projects page snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for my projects page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(myProjectsPageSnippet).click()
            .url().should('include', '/cms/snippets/home/my_projects_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.my_projects_page_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("My Projects Page Snippet 'Editing my projects page snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for my projects page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(myProjectsPageSnippet).click()
            .url().should('include', '/cms/snippets/home/my_projects_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("My Projects Page Snippet 'Editing my projects page snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for network analysis charts
    it('Can add a snippet for network analysis charts', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(networkAnalysisChartsSnippet).click()
            .url().should('include', '/cms/snippets/home/network_analysis_chart_snippet/')
        cy.contains('Add Network Analysis Charts Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.network_analysis_charts_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success).should('be.visible')
    })

    it('Can edit a snippet for network analysis charts', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(networkAnalysisChartsSnippet).click()
            .url().should('include', '/cms/snippets/home/network_analysis_chart_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.network_analysis_charts_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success).should('be.visible')
    })

    it('Can delete a snippet for network analysis charts', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(networkAnalysisChartsSnippet).click()
            .url().should('include', '/cms/snippets/home/network_analysis_chart_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success).should('be.visible')
    })

    //Snippet for partners organization profile contacts
    it('Can add a snippet for partners organization profile contacts', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersOrganizationProfileContactsSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_organizatiion_profile_contacts_snippet/')
        cy.contains('Add Partners Organization Profile Contacts Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.partners_organization_profile_contacts_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Partners Organization Profile Contacts Snippet 'Adding partners organization " +
                "profile contacts snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for partners organization profile contacts', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersOrganizationProfileContactsSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_organizatiion_profile_contacts_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.partners_organization_profile_contacts_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Partners Organization Profile Contacts Snippet 'Editing partners organization profile " +
                "contacts snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for partners organization profile contacts', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersOrganizationProfileContactsSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_organizatiion_profile_contacts_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Partners Organization Profile Contacts Snippet 'Editing partners organization " +
                "profile contacts snippet' deleted.")
            .should('be.visible')
    })

})


