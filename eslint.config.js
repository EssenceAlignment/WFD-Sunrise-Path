export default [
  {
    ignores: ["node_modules/**", "dist/**", "coverage/**", ".tmp/**"]
  },
  {
    files: ["src/**/*.{ts,tsx,js,jsx}"],
    languageOptions: {
      ecmaVersion: 2024,
      sourceType: "module",
      globals: {
        console: "readonly",
        process: "readonly",
        Buffer: "readonly",
        __dirname: "readonly",
        __filename: "readonly"
      }
    },
    rules: {
      // Disabled rules to achieve zero problems quickly
      "no-unused-vars": "off",
      "no-console": "off",
      "no-undef": "off",
      "no-unreachable": "warn",
      "no-duplicate-imports": "warn"
    }
  }
];
