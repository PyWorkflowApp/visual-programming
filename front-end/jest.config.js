module.exports = {
  collectCoverage: true,
  collectCoverageFrom: ['src/**/*.{js,jsx}'],
  coveragePathIgnorePatterns: [
    "src/index.js",
    "src/serviceWorker.js"
  ],
  coverageThreshold: {
    "global": {
      "branches": 60,
      "functions": 70,
      "lines": 70,
      "statements": 80
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
