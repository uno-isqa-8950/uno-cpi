import user from "../../../support/commands"
beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'addEventListener\'') || err.message.includes('null (reading \'style\')'))
        {
            return false
        }
    })
    cy.visit(Cypress.env('baseUrl'))
    cy.get('#login').click().loginAdminUser(user)
})


describe("Display cms options", () => {
    beforeEach(function() {
        cy.fixture("datareports").then(function(data) {
            this.data = data
        })
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
        update = ':nth-child(4) > .button-longrunning',
        deleteImage = ':nth-child(1) > .image-choice > figure > .image > .show-transparency',
        deleteButton = '.w-hidden > .no',
        deleteButtonAll = '.serious',
        success = '.success',
        fileUpload = 'input[type="file"]',
        cmsItemDocuments = '.sidebar-main-menu__list > :nth-child(3) > .sidebar-menu-item__link > .menuitem > .menuitem-label',
        addDocument = '.actionbutton > .button',
        deleteCms = ':nth-child(1) > .bulk-action-checkbox-cell > .bulk-action-checkbox',
        deleteDocumentLink = 'a[href="/cms/bulk/wagtaildocs/document/delete/?next=%2Fcms%2Fdocuments%2F"]',
        cmsItemSnippets = '.sidebar-main-menu__list > :nth-child(4) > .sidebar-menu-item__link > .menuitem > .menuitem-label',
        allProjectsPageSnippets = 'a[href="/cms/snippets/home/all_projects_snippet/"]',
        allProjectsPageAdd = 'a[href="/cms/snippets/home/all_projects_snippet/add/"]',
        allInputTextSnippet = '#id_text',
        saveSnippet = '.dropdown > .button',
        editSnippet = ':nth-child(1) > .title > .title-wrapper > a',
        snippetDelete = '.bulk-action-btn',
        campusPartnerSnippet = 'a[href="/cms/snippets/home/campus_partner_snippet/"]',
        campusPartnerAdd = 'a[href="/cms/snippets/home/campus_partner_snippet/add/"]'


    it('Can navigate to cms dashboard', () => {
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

        cy.get('input[type=file]').selectFile('cypress/fixtures/school-building.webp', { force: true })
        cy.get('input[type=file]')
            .invoke('show')
            .should('exist')
            .selectFile('cypress/fixtures/school-building.webp', { force: true })

        cy.get('.drop-zone')
            .selectFile('cypress/fixtures/school-building.webp', { action: 'drag-drop' })

        cy.get(image_title).clear()
        cy.get(image_title).type(this.data.image_title)
                .should('be.empty').and('be.visible')
        cy.get(update).contains("Update").should('exist').click()
        cy.get(success).contains("Image updated")
        cy.get(cmsItemLink).contains('Images').click()
    })

    it('Deleting an image', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemLink).contains('Images').should('exist').click()
        cy.get(deleteImage).should('exist').click()

        cy.get(deleteButton).should('exist').click()
        cy.get(deleteButtonAll).should('exist').click()
    })


    it('Verify documents can be added', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemDocuments).contains('Documents').click()
        cy.get(addDocument).should('exist').click()

        cy.get('input[type=file]').selectFile('cypress/fixtures/Lorem Ipsum.pdf', { force: true })
        cy.get('input[type=file]')
            .invoke('show')
            .should('exist')
            .selectFile('cypress/fixtures/Lorem Ipsum.pdf', { force: true })

        cy.get('.drop-zone')
            .selectFile('cypress/fixtures/Lorem Ipsum.pdf', { action: 'drag-drop' })

        cy.get(update).contains("Update").should('exist').click()
        cy.get(success).contains("Document updated")
        cy.get(cmsItemDocuments).contains('Documents').click()
    })

    it('Verify documents can be deleted', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemDocuments).contains('Documents').click()
        cy.get(deleteCms).should('exist').click()

        cy.get(deleteDocumentLink).contains('Delete').should('be.visible').click()
        cy.get(deleteButtonAll).should('be.visible').click()
    })


    it('Can add a snippet for all projects page', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(allProjectsPageSnippets).click()
            .url().should('include', '/cms/snippets/home/all_projects_snippet/')
        cy.get(allProjectsPageAdd).click()
            .url().should('include', '/cms/snippets/home/all_projects_snippet/add/')
        cy.get(allInputTextSnippet).type(this.data.all_project_snippet_text1)

        cy.get(saveSnippet).should('exist').click()
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

        cy.get(saveSnippet).should('exist').click()
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
    })



    it('Can add a snippet for campus partner', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemSnippets).contains('Snippets').click()
        cy.get(campusPartnerSnippet).click()
            .url().should('include', '/cms/snippets/home/campus_partner_snippet/')
        cy.get(campusPartnerAdd).click()
            .url().should('include', '/cms/snippets/home/campus_partner_snippet/add/')
        cy.get(allInputTextSnippet).type(this.data.campus_partner_snippet1)

        cy.get(saveSnippet).should('exist').click()
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

        cy.get(saveSnippet).should('exist').click()
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
    })


})
