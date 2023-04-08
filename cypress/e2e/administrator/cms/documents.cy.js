import user from "../../../support/commands"

describe("Display documents", () => {
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
        title = '.title-wrapper',
        update = ':nth-child(4) > .button-longrunning',
        deleteButtonAll = '.serious',
        success = '.success',
        fileUpload = 'input[type="file"]',
        cmsItemDocuments = '.sidebar-main-menu__list > :nth-child(3) > .sidebar-menu-item__link > .menuitem > .menuitem-label',
        addDocument = '.actionbutton > .button',
        deleteCms = ':nth-child(1) > .bulk-action-checkbox-cell > .bulk-action-checkbox',
        deleteDocumentLink = 'a[href="/cms/bulk/wagtaildocs/document/delete/?next=%2Fcms%2Fdocuments%2F"]'


    it('Can navigate to cms', () => {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()
    })

    it('Verify documents can be added', function() {
        cy.get(administratorLink).contains('Administrator').click()
            .get(cmsHref).invoke('removeAttr', 'target').click()

        cy.get(cmsItemDocuments).contains('Documents').click()
        cy.get(addDocument).should('exist').click()

        cy.get(fileUpload).selectFile('cypress/fixtures/loremIpsum.pdf', { force: true })
        cy.get(fileUpload)
            .invoke('show')
            .should('exist')
            .selectFile('cypress/fixtures/loremIpsum.pdf', { force: true })

        cy.get('.drop-zone')
            .selectFile('cypress/fixtures/loremIpsum.pdf', { action: 'drag-drop' })

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


})
