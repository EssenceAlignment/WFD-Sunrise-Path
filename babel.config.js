/**
 * @type {import('@babel/core').ConfigFunction}
 *
 * This configuration is for Babel, which is used by Jest (via ts-jest)
 * to transpile modern JavaScript. Since your `package.json` includes
 * `@babel/preset-react`, it's included here for completeness.
 */
export default {
  presets: [['@babel/preset-env', { targets: { node: 'current' } }], '@babel/preset-react'],
};
