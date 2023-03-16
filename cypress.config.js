module.exports = {
  e2e: {
      experimentalRunAllSpecs:true,
    setupNodeEvents(on, config) {
      // implement node event listeners here
        baseUrl: 'https://uno-cpi-dev.herokuapp.com/'
    },
  },
};