import user from "../../../../support/commands"

describe("Display resource page", () => {
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
        cmsResourcePage = '.sidebar-page-explorer-item > .sidebar-menu-item__link > .menuitem-label',
        homepageHeading = 'h3',
        resourceLink = 'a[href="/cms/pages/13/"]',
        title = '.title-wrapper',
        threeDotsButton = 'use[href="#icon-dots-horizontal"]',
        addSupbpage = '[href="/cms/pages/13/add_subpage/"]',
        pageTitle = '#id_title',
        pageSubtitle = '#id_subtitle',
        pageIntroduction = '#id_introduction',
        pageBodyAdd = '[href="#icon-plus"]',
        addPageBody = '.w-combobox__option-text',
        headingText = 'input[name="body-0-value-heading_text"]',
        headingSize = 'select[name="body-0-value-size"]',
        paragraph = '.notranslate',
        save = '.dropdown > .action-save',
        success = '.success',
        liveButton = ':nth-child(1) > .status > .status-tag',
        publishCheckbox = ':nth-child(1) > .bulk-action-checkbox-cell > .bulk-action-checkbox',
        publishButton = ':nth-child(3) > .bulk-action-btn',
        yesButton = '.button',
        unpublishButton = ':nth-child(4) > .bulk-action-btn',
        deleteButton = ':nth-child(2) > .bulk-action-btn'



    it('Can navigate to cms', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()
    })

    it('Can view resource page and verify pages exist', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsResourcePage).contains('Pages').should('exist').click()
        cy.get(homepageHeading).contains('UNO-CPI Homepage').should('exist').click()
        cy.get(resourceLink).click()
            .url().should('include', '/cms/pages/13/')

        cy.get(title).contains('Partnership Matchmakers').should('exist')
        cy.get(title).contains('Research and Leadership').should('exist')
    })

    it('Can add and publish a resource child page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsResourcePage).contains('Pages').should('exist').click()
        cy.get(homepageHeading).contains('UNO-CPI Homepage').should('exist').click()
        cy.get(resourceLink).click()
            .url().should('include', '/cms/pages/13/')

        cy.get(threeDotsButton).should('exist').click()
        cy.get(addSupbpage).should('exist').click()

        cy.get(pageTitle).type(this.data.resource_page_title1)
            .should('be.empty').and('be.visible')
        cy.get(pageSubtitle).type(this.data.resource_page_subtitle)
            .should('be.empty').and('be.visible')
        cy.get(pageIntroduction).type(this.data.page_introduction)
            .should('be.empty').and('be.visible')

        cy.get(pageBodyAdd).should('be.visible').click({ multiple: true })
        cy.get(addPageBody).contains('Heading block').click()

        cy.get(headingText).type(this.data.resource_heading_text)
            .should('be.empty').and('be.visible')
        cy.get(headingSize).should('be.visible').select(this.data.resource_heading_size, {force: true})

        cy.get(pageBodyAdd).should('be.visible').click({ multiple: true })
        cy.get(addPageBody).contains('Paragraph block').click()

        cy.get(paragraph).type(this.data.paragraph_block)
            .should('be.visible')

        cy.get(save).should('be.visible').click()
        cy.get(success).should('be.visible')
    })

    it('Can publish resource child page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsResourcePage).contains('Pages').should('exist').click()
        cy.get(homepageHeading).contains('UNO-CPI Homepage').should('exist').click()
        cy.get(resourceLink).click()
            .url().should('include', '/cms/pages/13/')

        cy.get(publishCheckbox).should('exist').click()
        cy.get(publishButton).contains('Publish').should('be.visible').click()
        cy.get(yesButton).contains('Yes, publish').click()
    })

    it('Verify resource page is live', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsResourcePage).contains('Pages').should('exist').click()
        cy.get(homepageHeading).contains('UNO-CPI Homepage').should('exist').click()
        cy.get(resourceLink).click()
            .url().should('include', '/cms/pages/13/')

        cy.get(liveButton).should('be.visible').invoke('removeAttr', 'target').click()
    })

    it('Can unpublish resource child page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsResourcePage).contains('Pages').should('exist').click()
        cy.get(homepageHeading).contains('UNO-CPI Homepage').should('exist').click()
        cy.get(resourceLink).click()
            .url().should('include', '/cms/pages/13/')

        cy.get(publishCheckbox).should('exist').click()
        cy.get(unpublishButton).contains('Unpublish').should('be.visible').click()
        cy.get(yesButton).contains('Yes, unpublish').click()
    })

    it('Can delete resource child page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsResourcePage).contains('Pages').should('exist').click()
        cy.get(homepageHeading).contains('UNO-CPI Homepage').should('exist').click()
        cy.get(resourceLink).click()
            .url().should('include', '/cms/pages/13/')

        cy.get(publishCheckbox).should('exist').click()
        cy.get(deleteButton).contains('Delete').should('be.visible').click()
        cy.get(yesButton).contains('Yes, delete').click()
    })


})
