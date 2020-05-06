module.exports = {
  collectCoverage: true,
  collectCoverageFrom: ['src/**/*.{js,jsx}'],
  coveragePathIgnorePatterns: [
    "src/index.js",
    "src/serviceWorker.js",
    "src/components/CustomNode/GraphView.js",
    "src/components/CustomNode/NodeConfig.js",
    "src/components/GlobalFlowMenu.js",
    "src/components/CustomNodeUpload.js"
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
