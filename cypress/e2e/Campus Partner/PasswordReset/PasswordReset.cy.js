beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined'))
        {
            return false
        }
    })
})

beforeEach(() => {
    Cypress.Cookies.preserveOnce('csrftoken');
});

describe('Password Reset', () => {
    it('visits the form', () => {
        cy.visit(Cypress.env('baseUrl'))
    })

    it('visits the login form', () => {
        cy.get('#login').click()
    })

    it('requires email', () => {
        cy.get('#email_input').type('campususer123@gmail.com{enter}')
    })

    it('forgot password', () => {
        cy.get('#nonUnoForgotPwd').click()
    })

    it('require email', () => {
        cy.get('#id_email').type('campususer123@gmail.com')
    })

    it('send email', () => {
        cy.get('#passwordReset').submit()
        cy.get('div').should('contain', 'Check your email')
    })
})