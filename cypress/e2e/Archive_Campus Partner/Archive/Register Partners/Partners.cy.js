function random_Text_Alpha_Numeric() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < 10; i++)
      text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}

beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined') || err.message.includes('reading \'document\''))
        {
            return false
        }
    })
})

describe('Partners', () => {
    var randomPartnerName = random_Text_Alpha_Numeric();
    it('visits the form', () => {
        cy.visit(Cypress.env('baseUrl'))
    })

    it('visits the login form', () => {
        cy.get('#partners').click()
        cy.wait(700)
    })

    // it('Register Community Partner', () => {
    //     cy.get('#btn_reg_community_partner').click()
    //     cy.wait(700)
    // })
    //
    // it('Search', () => {
    //     cy.get('#partner_name').type(randomPartnerName)
    //     cy.get('#next').click()
    // })
    //
    // it('Community Partner Registration link', () => {
    //     cy.get('#lnk-register_partner').click()
    // })
    //
    // it('Community Partner Information', () => {
    //     cy.get('#select2-id_community_type-container').click()
    //     cy.get('#select2-id_community_type-results').then(($li)=>{
    //          cy.wrap($li).contains("Nonprofit").click();
    //      })
    //     cy.get('#id_acronym').type("EHS")
    //     cy.wait(700)
    //     cy.get('#id_website_url').type("https://www.elkhornweb.org")
    //     cy.wait(700)
    //     cy.get('#id_online_only').click()
    //     cy.wait(700)
    //     cy.get('.sw-btn-next').click()
    // })
    //
    // it('Focus Area', () => {
    //     cy.get('#id_primary_mission-0-mission_area').select('Arts, Culture and Humanities')
    //     cy.wait(700)
    //     cy.get('#id_mission-0-mission_area').select('Arts, Culture and Humanities')
    //     cy.wait(700)
    //     cy.get('.add-mission-row').click()
    //     cy.wait(700)
    //     cy.get('#terms').click()
    //     cy.get('#submit').click()
    //     cy.wait(700)
    // })

    // it('visits the login form', () => {
    //     cy.get('#partners').click()
    //     cy.wait(700)
    // })

    it('Register Campus Partner', () => {
        cy.wait(700)
        cy.get('#btn_reg_campus_partner').click()
        cy.wait(700)
    })

    it('Add Campus Partner Name', () => {
        cy.get('#id_name').type(randomPartnerName)
        cy.get('#select2-id_college_name-container').click()
        cy.wait(700)
        cy.get('#select2-id_college_name-results').then(($li)=>{
             cy.wrap($li).contains("Academic Affairs").click();
         })
        cy.get(".sw-btn-next").click()
    })

    it('Contact Information', () => {
        cy.get('#id_form-0-first_name').type("Paul")
        cy.wait(700)
        cy.get('#id_form-0-last_name').type("Golden")
        cy.wait(700)
        cy.get('#id_form-0-email_id').type("PGolden@unomaha.edu")
        cy.wait(700)
        cy.get('.add-form-row').click();
        cy.get('#terms').click();
        cy.get('#submit').click();
    })

})


