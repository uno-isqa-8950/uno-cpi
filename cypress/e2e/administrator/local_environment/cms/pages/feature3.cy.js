import user from "../../../../support/commands"

describe("Display feature3 page", () => {
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
        homepageLink = 'a[href="/cms/pages/4/"]',
        title = '.title-wrapper',
        threeDotsButton = 'use[href="#icon-dots-horizontal"]',
        addSupbpage = '[href="/cms/pages/4/add_subpage/"]',
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

    it('Can view feature3 page and verify pages exist', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsResourcePage).contains('Pages').should('exist').click()
        cy.get(homepageHeading).contains('UNO-CPI Homepage').should('exist').click()
        cy.get(homepageLink).click()
            .url().should('include', '/cms/pages/4/')

        cy.get(title).contains('ARTS, CULTURE & HUMANITIES').should('exist')
        cy.get(title).contains('EDUCATIONAL SUPPORT').should('exist')
        cy.get(title).contains('INTERNATIONAL SERVICE').should('exist')
        cy.get(title).contains('ENVIRONMENTAL STEWARDSHIP').should('exist')
        cy.get(title).contains('HEALTH AND WELLNESS').should('exist')
        cy.get(title).contains('ECONOMIC IMPACT').should('exist')
        cy.get(title).contains('SOCIAL JUSTICE').should('exist')
    })

    it('Can add a feature3 child page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsResourcePage).contains('Pages').should('exist').click()
        cy.get(homepageHeading).contains('UNO-CPI Homepage').should('exist').click()
        cy.get(homepageLink).click()
            .url().should('include', '/cms/pages/4/')

        cy.get(threeDotsButton).should('exist').click()
        cy.get(addSupbpage).should('exist').click()

        cy.get(pageTitle).type(this.data.feature3_page_title1)
            .should('be.empty').and('be.visible')
        cy.get(pageSubtitle).type(this.data.feature3_page_subtitle)
            .should('be.empty').and('be.visible')
        cy.get(pageIntroduction).type(this.data.page_introduction)
            .should('be.empty').and('be.visible')

        cy.get(pageBodyAdd).should('be.visible').click({ multiple: true })
        cy.get(addPageBody).contains('Heading block').click()

        cy.get(headingText).type(this.data.feature3_heading_text)
            .should('be.empty').and('be.visible')
        cy.get(headingSize).should('be.visible').select(this.data.feature3_heading_size, {force: true})

        cy.get(pageBodyAdd).should('be.visible').click({ multiple: true })
        cy.get(addPageBody).contains('Paragraph block').click()

        cy.get(paragraph).type(this.data.paragraph_block)
            .should('be.visible')

        cy.get(save).should('be.visible').click()
        cy.get(success).should('be.visible')
    })

    it('Can publish feature 3 child page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsResourcePage).contains('Pages').should('exist').click()
        cy.get(homepageHeading).contains('UNO-CPI Homepage').should('exist').click()
        cy.get(homepageLink).click()
            .url().should('include', '/cms/pages/4/')

        cy.get(publishCheckbox).should('exist').click()
        cy.get(publishButton).contains('Publish').should('be.visible').click()
        cy.get(yesButton).contains('Yes, publish').click()
    })

    it('Verify feature3 page is live', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsResourcePage).contains('Pages').should('exist').click()
        cy.get(homepageHeading).contains('UNO-CPI Homepage').should('exist').click()
        cy.get(homepageLink).click()
            .url().should('include', '/cms/pages/4/')

        cy.get(liveButton).should('be.visible').invoke('removeAttr', 'target').click()
    })

    it('Can unpublish feature3 child page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsResourcePage).contains('Pages').should('exist').click()
        cy.get(homepageHeading).contains('UNO-CPI Homepage').should('exist').click()
        cy.get(homepageLink).click()
            .url().should('include', '/cms/pages/4/')

        cy.get(publishCheckbox).should('exist').click()
        cy.get(unpublishButton).contains('Unpublish').should('be.visible').click()
        cy.get(yesButton).contains('Yes, unpublish').click()
    })

    it('Can delete feature3 child page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsResourcePage).contains('Pages').should('exist').click()
        cy.get(homepageHeading).contains('UNO-CPI Homepage').should('exist').click()
        cy.get(homepageLink).click()
            .url().should('include', '/cms/pages/4/')

        cy.get(publishCheckbox).should('exist').click()
        cy.get(deleteButton).contains('Delete').should('be.visible').click()
        cy.get(yesButton).contains('Yes, delete').click()
    })


})
