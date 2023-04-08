import user from "../../../../support/commands"

beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })
    cy.visit(Cypress.env('baseUrl'))
})


describe("Display snippets", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
            cy.get('#login').click().loginAdminUser(user)
        })
    })

    /*beforeEach(() => {
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
    })*/

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
        partnersOrganizationProfilePartnersAddSnippet =
            'a[href="/cms/snippets/home/partners_organizatiion_profile_partners_add_snippet/"]',
        partnersOrganizationProfilePartnersUpdateSnippet =
            'a[href="/cms/snippets/home/partners_organizatiion_profile_partners_update_snippet/"]',
        partnersOrganizationProfileSnippet = 'a[href="/cms/snippets/home/partners_organizatiion_profile_snippet/"]',
        partnersUserProfileSnippet = 'a[href="/cms/snippets/home/partners_user_profile_snippet/"]',
        partnersUserProfileUpdateSnippet = 'a[href="/cms/snippets/home/partners_user_profile_update_snippet/"]',
        partnershipIntensityAnalysisChartSnippet =
            'a[href="/cms/snippets/home/partnershipintensityanalysis_chart_snippet/"]',
        passwordResetDoneSnippet = 'a[href="/cms/snippets/home/password_reset_done_snippet/"]',
        passwordResetSnippet = 'a[href="/cms/snippets/home/password_reset_snippet/"]',
        privateProjectReportSnippet = 'a[href="/cms/snippets/home/private_project_report_snippet/"]',
        publicProjectReportSnippet = 'a[href="/cms/snippets/home/public_project_report_snippet/"]'

    it('Can navigate to cms', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()
    })

    //Snippet for partners organization profile partners add
    it('Can add a snippet for partners organization profile partners add', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersOrganizationProfilePartnersAddSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_organizatiion_profile_partners_add_snippet/')
        cy.contains('Add Partners Organization Profile Partners Add Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.partners_organization_profile_partners_add_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Partners Organization Profile Partners Add Snippet 'Adding partners organization " +
                "profile partners add snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for partners organization profile partners add', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersOrganizationProfilePartnersAddSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_organizatiion_profile_partners_add_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.partners_organization_profile_partners_add_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Partners Organization Profile Partners Add Snippet 'Editing partners organization " +
                "profile partners add snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for partners organization profile partners add', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersOrganizationProfilePartnersAddSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_organizatiion_profile_partners_add_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Partners Organization Profile Partners Add Snippet 'Editing partners organization " +
                "profile partners add snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for partners organization profile partners update
    it('Can add a snippet for partners organization profile partners update', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersOrganizationProfilePartnersUpdateSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_organizatiion_profile_partners_update_snippet/')
        cy.contains('Add Partners Organization Profile Partners Update Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.partners_organization_profile_partners_update_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Partners Organization Profile Partners Update Snippet 'Adding partners organization " +
                "profile partners update snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for partners organization profile partners update', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersOrganizationProfilePartnersUpdateSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_organizatiion_profile_partners_update_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.partners_organization_profile_partners_update_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Partners Organization Profile Partners Update Snippet 'Editing partners organization " +
                "profile partners update snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for partners organization profile partners update', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersOrganizationProfilePartnersUpdateSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_organizatiion_profile_partners_update_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Partners Organization Profile Partners Update Snippet 'Editing partners organization " +
                "profile partners update snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for partners organization profile
    it('Can add a snippet for partners organization profile', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersOrganizationProfileSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_organizatiion_profile_snippet/')
        cy.contains('Add Partners Organization Profile Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.partners_organization_profile_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Partners Organization Profile Snippet 'Adding partners organization profile snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for partners organization profile', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersOrganizationProfileSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_organizatiion_profile_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.partners_organization_profile_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Partners Organization Profile Snippet 'Editing partners organization profile snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for partners organization profile', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersOrganizationProfileSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_organizatiion_profile_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Partners Organization Profile Snippet 'Editing partners organization profile snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for partners user profile
    it('Can add a snippet for partners user profile', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersUserProfileSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_user_profile_snippet/')
        cy.contains('Add Partners User Profile Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.partners_user_profile_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Partners User Profile Snippet 'Adding partners user profile snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for partners user profile', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersUserProfileSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_user_profile_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.partners_user_profile_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Partners User Profile Snippet 'Editing partners user profile snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for partners user profile', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersUserProfileSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_user_profile_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Partners User Profile Snippet 'Editing partners user profile snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for partners user profile update
    it('Can add a snippet for partners user profile update', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersUserProfileUpdateSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_user_profile_update_snippet/')
        cy.contains('Add Partners User Profile Update Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.partners_user_profile_update_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Partners User Profile Update Snippet 'Adding partners user profile update snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for partners user profile update', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersUserProfileUpdateSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_user_profile_update_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.partners_user_profile_update_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Partners User Profile Update Snippet 'Editing partners user profile update snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for partners user profile update', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnersUserProfileUpdateSnippet).click()
            .url().should('include', '/cms/snippets/home/partners_user_profile_update_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Partners User Profile Update Snippet 'Editing partners user profile update snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for partnership intensity analysis chart
    it('Can add a snippet for partnership intensity analysis chart', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnershipIntensityAnalysisChartSnippet).click()
            .url().should('include', '/cms/snippets/home/partnershipintensityanalysis_chart_snippet/')
        cy.contains('Add Partnership Intensity Analysis Chart Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.partnership_intensity_analysis_chart_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success).should('be.visible')
    })

    it('Can edit a snippet for partnership intensity analysis chart', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnershipIntensityAnalysisChartSnippet).click()
            .url().should('include', '/cms/snippets/home/partnershipintensityanalysis_chart_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.partnership_intensity_analysis_chart_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success).should('be.visible')
    })

    it('Can delete a snippet for partnership intensity analysis chart', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(partnershipIntensityAnalysisChartSnippet).click()
            .url().should('include', '/cms/snippets/home/partnershipintensityanalysis_chart_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success).should('be.visible')
    })

    //Snippet for password reset done
    it('Can add a snippet for password reset done', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(passwordResetDoneSnippet).click()
            .url().should('include', '/cms/snippets/home/password_reset_done_snippet/')
        cy.contains('Add Password Reset Done_Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.password_reset_done_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success).should('be.visible')
    })

    it('Can edit a snippet for password reset done', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(passwordResetDoneSnippet).click()
            .url().should('include', '/cms/snippets/home/password_reset_done_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.password_reset_done_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Password Reset Done_Snippet 'Editing password reset done snippet' updated.")
            .should('be.visible')
    })

    it('Can delete a snippet for password reset done', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(passwordResetDoneSnippet).click()
            .url().should('include', '/cms/snippets/home/password_reset_done_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Password Reset Done_Snippet 'Editing password reset done snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for password reset
    it('Can add a snippet for password reset', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(passwordResetSnippet).click()
            .url().should('include', '/cms/snippets/home/password_reset_snippet/')
        cy.contains('Add Password Reset Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.password_reset_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Password Reset Snippet 'Adding password reset snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for password reset', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(passwordResetSnippet).click()
            .url().should('include', '/cms/snippets/home/password_reset_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.password_reset_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Password Reset Snippet 'Editing password reset snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for password reset', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(passwordResetSnippet).click()
            .url().should('include', '/cms/snippets/home/password_reset_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Password Reset Snippet 'Editing password reset snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for private project report
    it('Can add a snippet for private project report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(privateProjectReportSnippet).click()
            .url().should('include', '/cms/snippets/home/private_project_report_snippet/')
        cy.contains('Add Private Project Report Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.private_project_report_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Private Project Report Snippet 'Adding private project report snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for private project report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(privateProjectReportSnippet).click()
            .url().should('include', '/cms/snippets/home/private_project_report_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.private_project_report_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Private Project Report Snippet 'Editing private project report snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for private project report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(privateProjectReportSnippet).click()
            .url().should('include', '/cms/snippets/home/private_project_report_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Private Project Report Snippet 'Editing private project report snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for public project report
    it('Can add a snippet for public project report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(publicProjectReportSnippet).click()
            .url().should('include', '/cms/snippets/home/public_project_report_snippet/')
        cy.contains('Add Public Project Report Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.public_project_report_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Public Project Report Snippet 'Adding public project report snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for public project report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(publicProjectReportSnippet).click()
            .url().should('include', '/cms/snippets/home/public_project_report_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.public_project_report_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Public Project Report Snippet 'Editing public project report snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for public project report', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(publicProjectReportSnippet).click()
            .url().should('include', '/cms/snippets/home/public_project_report_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Public Project Report Snippet 'Editing public project report snippet' deleted.")
            .should('be.visible')
    })


})


