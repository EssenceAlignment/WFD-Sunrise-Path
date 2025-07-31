#!/usr/bin/env node

/**
 * Setup script for Taskmaster AI MCP Server
 * This script provides instructions for configuring Taskmaster AI in Cline
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

console.log('\n🤖 Taskmaster AI (Astrotask) MCP Server Setup\n');

// Configuration to add
const astrotaskConfig = {
  "astrotask": {
    "command": "npx",
    "args": ["@astrotask/mcp"],
    "env": {
      "DATABASE_URI": "./data/astrotask.db",
      "LOG_LEVEL": "info",
      "NODE_ENV": "production"
    }
  }
};

console.log('📋 Instructions for adding Taskmaster AI to Cline:\n');

console.log('OPTION 1: Manual Configuration in VSCode');
console.log('1. Open VSCode Command Palette (Cmd/Ctrl + Shift + P)');
console.log('2. Search for "Cline: Edit MCP Server Configurations"');
console.log('3. Add the following configuration:\n');
console.log(JSON.stringify(astrotaskConfig, null, 2));

console.log('\n\nOPTION 2: Direct File Edit');
console.log('1. Open the Cline MCP settings file:');

// Determine the likely path based on OS
const platform = os.platform();
let configPath;

if (platform === 'darwin') {
  // macOS
  configPath = path.join(os.homedir(), 'Library', 'Application Support', 'Code', 'User', 'globalStorage', 'cline', 'settings', 'cline_mcp_settings.json');
} else if (platform === 'win32') {
  // Windows
  configPath = path.join(process.env.APPDATA, 'Code', 'User', 'globalStorage', 'cline', 'settings', 'cline_mcp_settings.json');
} else {
  // Linux
  configPath = path.join(os.homedir(), '.config', 'Code', 'User', 'globalStorage', 'cline', 'settings', 'cline_mcp_settings.json');
}

console.log(`   ${configPath}`);
console.log('\n2. Add the Astrotask configuration to the "mcpServers" object');
console.log('3. Save the file and restart VSCode');

console.log('\n\n✨ After Configuration:');
console.log('- Cline will have access to task management tools');
console.log('- You can ask Cline to create, update, and manage tasks');
console.log('- Tasks will be stored in ./data/astrotask.db');

console.log('\n📚 Example Commands:');
console.log('- "Create a task to implement user authentication"');
console.log('- "List all pending tasks"');
console.log('- "Mark task A as complete"');
console.log('- "Show me the next high-priority task"');

console.log('\n📄 Documentation:');
console.log('- Full setup guide: TASKMASTER_AI_SETUP.md');
console.log('- Sample config: mcp-config/astrotask-config.json');

console.log('\n🔧 Troubleshooting:');
console.log('- Ensure npx is available in your PATH');
console.log('- Restart VSCode after configuration changes');
console.log('- Check Cline\'s MCP server status in the UI');

console.log('\n✅ Setup instructions complete!\n');
