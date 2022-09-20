function random_Text_Alpha_Numeric() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < 10; i++)
      text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

beforeEach(() => {
    cy.on('uncaught:exception', (err, runnable) => {
        if(err.message.includes('is not a function') || err.message.includes('is not defined'))
        {
            return false
        }
    })
})

describe('Partners', () => {
    it('visits the form', () => {
        cy.visit('http://127.0.0.1:8000/')
    })

    it('visits the login form', () => {
        cy.get('#partners').click()
    })

    it('Register Community Partner', () => {
        cy.get('#btn_reg_community_partner').click()
    })

    it('Search', () => {

        cy.get('#partner_name').type(random_Text_Alpha_Numeric())
        cy.get('#next').click()
    })

    it('Community Partner Registration link', () => {
        cy.get('#lnk-register_partner').click()
    })

    it('Community Partner Information', () => {
        cy.get('#select2-id_community_type-container').click()
        cy.get('#select2-id_community_type-results').then(($li)=>{
             cy.wrap($li).contains("Nonprofit").click();
         })
        cy.get('#id_acronym').type("EHS")
        cy.get('#id_website_url').type("https://www.elkhornweb.org")
        cy.get('#id_online_only').click()
        cy.get('.sw-btn-next').click()
    })

    it('Focus Area', () => {
        cy.get('#id_primary_mission-0-mission_area').select('Arts, Culture and Humanities')
        cy.get('#id_mission-0-mission_area').select('Arts, Culture and Humanities')
        cy.get('.add-mission-row').click()
        cy.get('#terms').click()
        cy.get('#submit').click()
    })
})


