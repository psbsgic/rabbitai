/* eslint-disable global-require */
const loadModule = () => {
  let module;
  try {
    // @ts-ignore
    module = require('../../../rabbitai_text'); // eslint-disable-line import/no-unresolved
  } catch (e) {
    module = {};
  }
  return module;
};

const rabbitaiText = loadModule();

export default rabbitaiText;
