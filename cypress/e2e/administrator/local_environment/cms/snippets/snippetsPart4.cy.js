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
        registerCampusPartnerSnippet = 'a[href="/cms/snippets/home/register_campus_partner_snippet/"]',
        registerCampusPartnerUserSnippet = 'a[href="/cms/snippets/home/register_campus_partner_user_snippet/"]',
        registerCommunityPartnerFormSnippet = 'a[href="/cms/snippets/home/register_community_partner_form_snippet/"]',
        registerCommunityPartnerSearchSnippet = 'a[href="/cms/snippets/home/register_community_partner_snippet/"]',
        registerCommunityPartnerUserSnippet = 'a[href="/cms/snippets/home/register_community_partner_user_snippet/"]',
        trendReportChartSnippet = 'a[href="/cms/snippets/home/trendreport_chart_snippet/"]'

    it('Can navigate to cms', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()
    })

    //Snippet for register campus partner
    it('Can add a snippet for register campus partner', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(registerCampusPartnerSnippet).click()
            .url().should('include', '/cms/snippets/home/register_campus_partner_snippet/')
        cy.contains('Add Register Campus Partner Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.register_campus_partner_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Register Campus Partner Snippet 'Adding register campus partner snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for register campus partner', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(registerCampusPartnerSnippet).click()
            .url().should('include', '/cms/snippets/home/register_campus_partner_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.register_campus_partner_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Register Campus Partner Snippet 'Editing register campus partner snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for register campus partner', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(registerCampusPartnerSnippet).click()
            .url().should('include', '/cms/snippets/home/register_campus_partner_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Register Campus Partner Snippet 'Editing register campus partner snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for register campus partner user
    it('Can add a snippet for register campus partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(registerCampusPartnerUserSnippet).click()
            .url().should('include', '/cms/snippets/home/register_campus_partner_user_snippet/')
        cy.contains('Add Register Campus Partner User Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.register_campus_partner_user_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Register Campus Partner User Snippet 'Adding register campus partner user snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for register campus partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(registerCampusPartnerUserSnippet).click()
            .url().should('include', '/cms/snippets/home/register_campus_partner_user_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.register_campus_partner_user_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Register Campus Partner User Snippet 'Editing register campus partner user snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for register campus partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(registerCampusPartnerUserSnippet).click()
            .url().should('include', '/cms/snippets/home/register_campus_partner_user_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Register Campus Partner User Snippet 'Editing register campus partner user snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for register community partner form
    it('Can add a snippet for register community partner form', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(registerCommunityPartnerFormSnippet).click()
            .url().should('include', '/cms/snippets/home/register_community_partner_form_snippet/')
        cy.contains('Add Register Community Partner Form Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.register_community_partner_form_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Register Community Partner Form Snippet 'Adding register community partner form snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for register community partner form', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(registerCommunityPartnerFormSnippet).click()
            .url().should('include', '/cms/snippets/home/register_community_partner_form_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.register_community_partner_form_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Register Community Partner Form Snippet 'Editing register community partner form snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for register community partner form', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(registerCommunityPartnerFormSnippet).click()
            .url().should('include', '/cms/snippets/home/register_community_partner_form_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Register Community Partner Form Snippet 'Editing register community partner form snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for register community partner search
    it('Can add a snippet for register community partner search', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(registerCommunityPartnerSearchSnippet).click()
            .url().should('include', '/cms/snippets/home/register_community_partner_snippet/')
        cy.contains('Add Register Community Partner Search Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.register_community_partner_search_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Register Community Partner Search Snippet 'Adding register community partner search snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for register community partner search', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(registerCommunityPartnerSearchSnippet).click()
            .url().should('include', '/cms/snippets/home/register_community_partner_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.register_community_partner_search_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Register Community Partner Search Snippet 'Editing register community partner search snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for register community partner search', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(registerCommunityPartnerSearchSnippet).click()
            .url().should('include', '/cms/snippets/home/register_community_partner_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Register Community Partner Search Snippet 'Editing register community partner search snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for register community partner user
    it('Can add a snippet for register community partner search', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(registerCommunityPartnerUserSnippet).click()
            .url().should('include', '/cms/snippets/home/register_community_partner_user_snippet/')
        cy.contains('Add Register Community Partner User Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.register_community_partner_user_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Register Community Partner User Snippet 'Adding register community partner user snippet' created.")
            .should('be.visible')
    })

    it('Can edit a snippet for register community partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(registerCommunityPartnerUserSnippet).click()
            .url().should('include', '/cms/snippets/home/register_community_partner_user_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.register_community_partner_user_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success)
            .contains("Register Community Partner User Snippet 'Editing register community partner user snippet' updated")
            .should('be.visible')
    })

    it('Can delete a snippet for register community partner user', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(registerCommunityPartnerUserSnippet).click()
            .url().should('include', '/cms/snippets/home/register_community_partner_user_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success)
            .contains("Register Community Partner User Snippet 'Editing register community partner user snippet' deleted.")
            .should('be.visible')
    })

    //Snippet for trend report chart
    it('Can add a snippet for trend report chart', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(trendReportChartSnippet).click()
            .url().should('include', '/cms/snippets/home/trendreport_chart_snippet/')
        cy.contains('Add Trend Report Chart Snippet').click().should('exist')
        cy.get(allInputTextSnippet).type(this.data.trend_report_chart_snippet1)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success).should('be.visible')
    })

    it('Can edit a snippet for trend report chart', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(trendReportChartSnippet).click()
            .url().should('include', '/cms/snippets/home/trendreport_chart_snippet/')
        cy.get(editSnippet).should('exist').click()
        cy.get(allInputTextSnippet).clear()
        cy.get(allInputTextSnippet).type(this.data.trend_report_chart_snippet2)
            .should('be.empty').and('be.visible')

        cy.get(saveSnippet).should('exist').click()
        cy.get(success).should('be.visible')
    })

    it('Can delete a snippet for trend report chart', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(trendReportChartSnippet).click()
            .url().should('include', '/cms/snippets/home/trendreport_chart_snippet/')
        cy.get(deleteCms).should('exist').click()

        cy.get(snippetDelete).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
        cy.get(success).should('be.visible')
    })


})


