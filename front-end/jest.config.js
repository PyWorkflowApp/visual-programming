module.exports = {
  collectCoverage: true,
  collectCoverageFrom: ['src/**/*.{js,jsx}'],
  coverageThreshold: {
    "global": {
      "branches": 80,
      "functions": 80,
      "lines": 80,
      "statements": 80
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
