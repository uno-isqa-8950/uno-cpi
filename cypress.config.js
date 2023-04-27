module.exports = {
  e2e: {
    experimentalRunAllSpecs: false,
    "retries": 1,
    experimentalMemoryManagement: false,
    "numTestsKeptInMemory": 0,
    setupNodeEvents(on, config) {
      // implement node event listeners here
      config.baseUrl = 'place the base URL under test';
    },
    testingType: 'e2e',
    specPattern: [
      'cypress/e2e/cepiProject/cepiTestPriority1.cy.js',
      'cypress/e2e/cepiProject/cepiTestPriority2.cy.js',
      'cypress/e2e/cepiProject/cepiTestPriority3.cy.js',
      'cypress/e2e/cepiProject/cepiTestPriority4.cy.js',
    ],
  },
};
