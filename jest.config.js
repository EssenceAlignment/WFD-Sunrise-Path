/**
 * @type {import('ts-jest').JestConfigWithTsJest}
 *
 * Given your project's `package.json` has `"type": "module"`, Jest needs to be
 * configured to work with ES Modules (ESM). This configuration uses `ts-jest`
 * to handle both TypeScript and JavaScript files in an ESM-native way.
 */
export default {
  // The preset from ts-jest handles most of the boilerplate for ESM support.
  preset: 'ts-jest/presets/default-esm',

  // The environment in which the tests are run. Your project includes
  // `jest-environment-jsdom`, so you can switch to 'jsdom' for frontend tests.
  testEnvironment: 'node',

  // Automatically clear mock calls, instances, and results before every test
  clearMocks: true,

  // Collect coverage information
  collectCoverage: true,
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    '**/*.{js,jsx,ts,tsx}',
    '!**/node_modules/**',
    '!**/vendor/**',
    '!**/coverage/**',
    '!**/dist/**',
    '!**/build/**',
    '!jest.config.js',
    '!babel.config.js',
    '!**/qualtrics-api-project/**', // Ignoring the Qualtrics project as it seems separate
  ],

  // The glob patterns Jest uses to detect test files
  testMatch: [
    '**/__tests__/**/*.[jt]s?(x)', // Matches files in __tests__ folders
    '**/?(*.)+(spec|test).[jt]s?(x)', // Matches files with .test.js, .spec.ts, etc.
  ],

  // `ts-jest` will transform both TypeScript and JavaScript files for ESM.
  transform: {
    '^.+\\.m?[tj]sx?$': [
      'ts-jest',
      {
        useESM: true,
      },
    ],
  },

  // This mapper is needed for ESM to correctly resolve module paths with extensions.
  moduleNameMapper: {
    '^(\\.{1,2}/.*)\\.js$': '$1',
  },
};
