
// This function is called when a project is opened or re-opened (e.g. due to
// the project's config changing)

module.exports = (on, config) => {
  require('@cypress/code-coverage/task')(on, config);
  return config;
};
