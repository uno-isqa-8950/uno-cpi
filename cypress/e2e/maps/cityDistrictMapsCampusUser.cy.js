describe("City district maps test", () => {
  beforeEach(() => {
    cy.on("uncaught:exception", (err) => {
      if (
        err.message.includes("is not a function") ||
        err.message.includes("is not defined") ||
        err.message.includes("reading 'options'") ||
        err.message.includes("reading 'scrollTop'") ||
        err.message.includes("reading 'addEventListener'") ||
        err.message.includes("null (reading 'style')")
      ) {
        return false;
      }
    });
    cy.fixture("datareports").then(function (data) {
      this.data = data;
    });
    cy.loginCampusUser(); // Campus User is logged in before the test begins
    cy.visit(Cypress.env("baseUrl"));
  });

  // This test is expected to pass visiting community partners under maps as a public user.
  // Test is asserted on url, visibility of filters button, map canvas existence in the page loaded and existence of footer.
  it("City district page visit ", function () {
    const citydistrictsHref = '[data-cy="citydistricts"]',
      filtersButton = '[data-cy="filters"]',
      footerId = '[data-cy="footer"]',
      mapsDivId = '[data-cy="mapcanvas"]',
      mapsLink = '[data-cy="maps"]',
      noOfCommPartID = '[data-cy="totalnumber"]',
      navbar = '[data-cy="navbar"]';
    cy.get(mapsLink)
      .contains("Maps")
      .click()
      .get(citydistrictsHref)
      .click()
      .url()
      .should("be.equal", Cypress.env("baseUrl") + "city-District");
    // Asserting to check the page title
    cy.get(navbar)
      .should("exist")
      // Checking the number of community partners value is visible
      .get("div")
      .contains("label", "Number of Community Partners:")
      // Total numbers value  existence assertion
      .get(noOfCommPartID)
      .should("be.visible")
      .get(filtersButton)
      .should("be.visible")
      .get(mapsDivId)
      .should("exist")
      .get(footerId)
      .should("exist");
  });

  it("Test filter dropdown are clickable", function () {
    const citydistrictsHref = '[data-cy="citydistricts"]',
      filtersButton = '[data-cy="filters"]',
      footerId = '[data-cy="footer"]',
      mapsDivId = '[data-cy="mapcanvas"]',
      mapsLink = '[data-cy="maps"]',
      districtsDropdown = '[data-cy="selectdistrict"]',
      communityPartnerDropdown = '[data-cy="selectcommunitytype"]',
      selectCollegeDropdown = '[data-cy="selectcollege"]',
      selectCampusPartnerDropdown = '[data-cy="selectcampus"]',
      selectYearDropdown = '[data-cy="selectyear"]',
      reset = '[data-cy="reset"]';

    cy.get(mapsLink)
      .contains("Maps")
      .click()

      .get(citydistrictsHref)
      .click()

      .url()
      .should("be.equal", Cypress.env("baseUrl") + "city-District") // filter button clicking and asserting to check the button is not disabled

      .get(filtersButton)
      .click()
      .should("not.be.disabled") // select dropdown triggering click action to check it is clickable and asserting to check its not disabled

      .get(districtsDropdown)
      .trigger("click")
      .should("not.be.disabled")
      .select(this.data.All_City_Council_Districts);

    cy.get(communityPartnerDropdown)
      .trigger("click")
      .should("not.be.disabled")
      .get(communityPartnerDropdown)
      .select(this.data.community_type2)

      .get(selectCollegeDropdown)
      .trigger("click")
      .should("not.be.disabled")
      .get(selectCollegeDropdown)
      .select(this.data.All_Colleges_And_main_Units)

      .get(selectCampusPartnerDropdown)
      .trigger("click")
      .should("not.be.disabled")
      .get(selectCampusPartnerDropdown)
      .select(this.data.All_Campus_Partners)

      .get(selectYearDropdown)
      .trigger("click")
      .should("not.be.disabled")
      .get(selectYearDropdown)
      .select(this.data.All_Academic_Years)

      .get(mapsDivId)
      .should("exist")

      .get(footerId)
      .should("exist")

      .get(reset)
      .should("exist");
    cy.get("#map_canvas").then(($canvas) => {
      // South Carolina
      // Wrap the canvas with the Cypress API, scroll it into view, and click in the location!
      const Map_point =
          '[style="position: absolute; left: 0px; top: 0px; z-index: 106; width: 100%;"] > :nth-child(9) > img',
        Map_point_details1 = ".gm-style-iw-d > div > :nth-child(7)",
        Map_point_details4 = ".gm-style-iw-d > div > :nth-child(11)",
        Map_Zoom = '[aria-label="Zoom in"]';
      cy.wrap($canvas);
      cy.get(Map_Zoom).click();
      cy.get(Map_point).click({force: true});
      cy.wait(1000);
      cy.wrap($canvas);
      cy.get(Map_point).click();
      cy.wait(1000);
      cy.get(Map_point_details1)
        .contains(this.data.Focus_Areas)
        .should("be.visible");
      cy.get(Map_point_details4)
        .contains(this.data._comment7)
        .should("be.visible");
    });
  });
});
