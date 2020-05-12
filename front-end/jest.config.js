module.exports = {
  collectCoverage: true,
  collectCoverageFrom: ['src/**/*.{js,jsx}'],
  coveragePathIgnorePatterns: [
    "src/index.js",
    "src/serviceWorker.js"
  ],
  coverageThreshold: {
    "global": {
      "branches": 10,
      "functions": 10,
      "lines": 10,
      "statements": 10
    }
  },
  moduleNameMapper: {
    "\\.(css|less)$": "<rootDir>/__mocks__/css/styleMock.js"
  },
  setupFiles: [
     'jest-canvas-mock'
  ],
  setupFilesAfterEnv: [
    "./setupTests.js"
  ],
  testPathIgnorePatterns: [
  ],
  transform: {
  '^.+\\.(js|jsx)?$': 'babel-jest'
  },

};
