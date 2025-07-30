const fs = require('fs');

// Define expected types for each rule
const booleanFields = [
  'code_blocks', 'tables', 'headings', 'headers',
  'strict', 'stern', 'html', 'indented'
];

// Use function expression instead of declaration to avoid Sourcery warning
const checkObject = (obj, path, errors, booleanFields) => {
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
      checkObject(value, currentPath, errors, booleanFields);
    }
  }
};

function validateMarkdownlintConfig(configPath) {
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const errors = [];

  checkObject(config, '', errors, booleanFields);
  return errors;
}

// Use function expression for fixObject to avoid Sourcery warning
const fixObject = (obj, booleanFields) => {
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
      fixObject(value, booleanFields);
    }
  }
};

// Auto-fix function
function autoFixMarkdownlintConfig(configPath) {
  let config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

  const booleanFieldsForFix = [
    'code_blocks', 'tables', 'headings', 'headers',
    'strict', 'stern', 'html', 'indented'
  ];

  fixObject(config, booleanFieldsForFix);
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
}

module.exports = { validateMarkdownlintConfig, autoFixMarkdownlintConfig };
