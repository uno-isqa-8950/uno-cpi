module.exports = {
  e2e: {
      experimentalRunAllSpecs:true,
       watchForFileChanges:false,
    setupNodeEvents(on, config) {
      // implement node event listeners here
        baseUrl: 'place the base URL under test'
    },
  },
};
