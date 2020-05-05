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
      "functions": 60,
      "lines": 60,
      "statements": 60
    }
  },
  moduleNameMapper: {
    "\\.(css|less)$": "<rootDir>/__mocks__/css/styleMock.js"
  },
  setupFilesAfterEnv: [
    "./setupTests.js"
  ],
  testPathIgnorePatterns: [
  ]
};
