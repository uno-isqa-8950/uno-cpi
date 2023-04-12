import user from "../../../support/commands"

describe("Display images", () => {
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
        cmsItemImages = '.sidebar-main-menu__list > :nth-child(2) > .sidebar-menu-item__link > .menuitem > .menuitem-label',
        sortBy = 'select[name="ordering"]',
        entriesPerPage = 'select[name="entries_per_page"]',
        add = `a[href="/cms/images/multiple/add/"]`,
        search = '#menu-search-q',
        searchbar = '#id_q',
        searchPageType = '#page-types-title',
        searchAll = '.w-bg-grey-100',
        searchBlogPage = 'a[href="/cms/pages/search/?q=&content_type=home.blogpage"]',
        searchBlogIndexPage = 'a[href="/cms/pages/search/?q=&content_type=home.blogindexpage"]',
        searchPage = 'a[href="/cms/pages/search/?q=&content_type=wagtailcore.page"]',
        searchHomepage = 'a[href="/cms/pages/search/?q=&content_type=home.homepage"]',
        image_title = 'input[type="text"]',
        update = '.button',
        deleteImage = ':nth-child(1) > .image-choice > figure > .image > .show-transparency',
        deleteButton = '.w-hidden > .no',
        deleteButtonAll = '.serious',
        success = '.success',
        fileUpload = 'input[type="file"]'


    it('Can navigate to cms', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()
    })

    it('Can search', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(search).type('{enter}')
        cy.get(searchbar).should('exist').focus().type(this.data.cms_search)
    })


    it('Verify search matching pages', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(search).type('{enter}')
        cy.get(searchPageType).should('be.visible').and('have.text', 'Page types')
            .click()
        cy.get(searchAll).should('be.visible').and('have.text', 'All (14)').click()
        cy.get(searchBlogPage).should('be.visible').and('have.text', 'Blog page (9)').click()
        cy.get(searchBlogIndexPage).should('be.visible').and('have.text', 'Blog index page (3)').click()
        cy.get(searchPage).should('be.visible').and('have.text', 'Page (1)').click()
        cy.get(searchHomepage).should('be.visible').and('have.text', 'Homepage (1)').click()
    })

    it('Sort images and add entries per page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemImages).contains('Images').should('exist').click()
        cy.get(sortBy).should('be.visible')
            .select(this.data.images_sort_by, {force: true})

        cy.get(entriesPerPage).should('be.visible')
            .select(this.data.images_entries, {force: true})
    })

    it('Adding an image', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemImages).contains('Images').should('exist').click()
        cy.get(add).contains('Add an image').should('exist').click()

        cy.get(fileUpload).selectFile('cypress/fixtures/school-building.webp', { force: true })
        cy.get(fileUpload)
            .invoke('show')
            .should('exist')
            .selectFile('cypress/fixtures/school-building.webp', { force: true })

        cy.get('.drop-zone')
            .selectFile('cypress/fixtures/school-building.webp', { action: 'drag-drop' })

        cy.get(image_title).clear()
        cy.get(image_title).type(this.data.image_title)
                .should('be.empty').and('be.visible')
        /*cy.get(update).contains("Update").click()
        cy.get(success).contains("Image updated")*/
        cy.get(cmsItemImages).contains('Images').click()
    })

    it('Deleting an image', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemImages).contains('Images').should('exist').click()
        cy.get(deleteImage).should('exist').click()

        cy.get(deleteButton).should('exist').click()
        cy.get(deleteButtonAll).should('exist').click()
    })

})
