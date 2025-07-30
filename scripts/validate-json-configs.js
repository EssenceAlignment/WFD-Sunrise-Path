const fs = require('fs');

function validateMarkdownlintConfig(configPath) {
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const errors = [];

  // Define expected types for each rule
  const booleanFields = [
    'code_blocks', 'tables', 'headings', 'headers',
    'strict', 'stern', 'html', 'indented'
  ];

  function checkObject(obj, path = '') {
    for (const [key, value] of Object.entries(obj)) {
      const currentPath = path ? `${path}.${key}` : key;

      // Check if this field should be boolean
      if (booleanFields.includes(key) && typeof value !== 'boolean') {
        errors.push({
          path: currentPath,
          expected: 'boolean',
          actual: typeof value,
          value: value
        });
      }

      // Recurse into nested objects
      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        checkObject(value, currentPath);
      }
    }
  }

  checkObject(config);
  return errors;
}

// Auto-fix function
function autoFixMarkdownlintConfig(configPath) {
  let config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

  const booleanFields = [
    'code_blocks', 'tables', 'headings', 'headers',
    'strict', 'stern', 'html', 'indented'
  ];

  function fixObject(obj) {
    for (const [key, value] of Object.entries(obj)) {
      if (booleanFields.includes(key)) {
        // Convert common false values to boolean false
        if (value === 'false' || value === 0 || value === null) {
          obj[key] = false;
        }
        // Convert common true values to boolean true
        else if (value === 'true' || value === 1) {
          obj[key] = true;
        }
      }

      // Recurse into nested objects
      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        fixObject(value);
      }
    }
  }

  fixObject(config);
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
}

module.exports = { validateMarkdownlintConfig, autoFixMarkdownlintConfig };
