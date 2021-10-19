// always use absolute directory
const workspaceDirectory = process.env.GITHUB_WORKSPACE;
const homeDirectory = process.env.HOME;

const assetsConfig = {
  path: [`${workspaceDirectory}/rabbitai/static/assets`],
  hashFiles: [
    `${workspaceDirectory}/rabbitai-frontend/src/**/*`,
    `${workspaceDirectory}/rabbitai-frontend/*.js`,
    `${workspaceDirectory}/rabbitai-frontend/*.json`,
  ],
  // dont use restore keys as it may give an invalid older build
  restoreKeys: '',
};

// Multi-layer cache definition
module.exports = {
  pip: {
    path: [`${homeDirectory}/.cache/pip`],
    hashFiles: [`${workspaceDirectory}/requirements/*.txt`],
  },
  npm: {
    path: [`${homeDirectory}/.npm`],
    hashFiles: [`${workspaceDirectory}/rabbitai-frontend/package-lock.json`],
  },
  assets: assetsConfig,
  // use separate cache for instrumented JS files and regular assets
  // one is built with `npm run build`,
  // another is built with `npm run build-instrumented`
  'instrumented-assets': assetsConfig,
  cypress: {
    path: [`${homeDirectory}/.cache/Cypress`],
    hashFiles: [
      `${workspaceDirectory}/rabbitai-frontend/cypress-base/package-lock.json`,
    ],
  },
};
