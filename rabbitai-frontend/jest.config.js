module.exports = {
  testRegex: '(\\/spec|\\/src)\\/.*(_spec|\\.test)\\.(j|t)sx?$',
  moduleNameMapper: {
    '\\.(css|less)$': '<rootDir>/spec/__mocks__/styleMock.js',
    '\\.(gif|ttf|eot|png|jpg)$': '<rootDir>/spec/__mocks__/fileMock.js',
    '\\.svg$': '<rootDir>/spec/__mocks__/svgrMock.tsx',
    '^src/(.*)$': '<rootDir>/src/$1',
    '^spec/(.*)$': '<rootDir>/spec/$1',
  },
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/spec/helpers/setup.ts'],
  testURL: 'http://localhost',
  collectCoverageFrom: ['src/**/*.{js,jsx,ts,tsx}', '!**/*.stories.*'],
  coverageDirectory: '<rootDir>/coverage/',
  transform: {
    '^.+\\.jsx?$': 'babel-jest',
    '^.+\\.tsx?$': 'ts-jest',
  },
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],
  snapshotSerializers: ['@emotion/jest/enzyme-serializer'],
  globals: {
    'ts-jest': {
      babelConfig: true,
      diagnostics: {
        warnOnly: true,
      },
    },
  },
};
