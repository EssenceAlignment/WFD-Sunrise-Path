#!/usr/bin/env node
/**
 * Environment Variable Checker
 * Ensures all required environment variables are set
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.join(__dirname, '..');

// Load .env.example to get required variables
const envExamplePath = path.join(rootDir, '.env.example');
const envPath = path.join(rootDir, '.env');

if (!fs.existsSync(envExamplePath)) {
  console.error('❌ Error: .env.example file not found!');
  process.exit(1);
}

// Parse .env.example to get required variables
const envExampleContent = fs.readFileSync(envExamplePath, 'utf8');
const requiredVars = [];

envExampleContent.split('\n').forEach(line => {
  line = line.trim();
  // Skip comments and empty lines
  if (line && !line.startsWith('#')) {
    const [key] = line.split('=');
    if (key) {
      requiredVars.push(key.trim());
    }
  }
});

// Check if .env exists
if (!fs.existsSync(envPath)) {
  console.error('❌ Error: .env file not found!');
  console.error('   Copy .env.example to .env and fill in your values.');
  process.exit(1);
}

// Load actual environment variables
const dotenv = await import('dotenv');
const result = dotenv.config();

if (result.error) {
  console.error('❌ Error loading .env file:', result.error);
  process.exit(1);
}

// Check for missing variables
const missingVars = [];
const emptyVars = [];

requiredVars.forEach(varName => {
  const value = process.env[varName];
  if (value === undefined) {
    missingVars.push(varName);
  } else if (value.trim() === '' || value.includes('your_') || value.includes('_here')) {
    emptyVars.push(varName);
  }
});

// Report results
if (missingVars.length > 0 || emptyVars.length > 0) {
  console.error('❌ Environment variable check failed!\n');

  if (missingVars.length > 0) {
    console.error('Missing variables:');
    missingVars.forEach(v => console.error(`  - ${v}`));
  }

  if (emptyVars.length > 0) {
    console.error('\nVariables with placeholder values:');
    emptyVars.forEach(v => console.error(`  - ${v}`));
  }

  console.error('\n📋 Check .env.example for required variables.');
  process.exit(1);
}

console.log('✅ All required environment variables are set!');
