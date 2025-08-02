#!/usr/bin/env node

// Test script for Cloudflare MCP Server
const { spawn } = require('child_process');
const path = require('path');

console.log('🔧 Testing Cloudflare MCP Server...\n');

// Server configuration
const serverPath = '/Users/ericjones/Documents/Cline/MCP/cloudflare-server/build/index.js';
const apiToken = process.env.CLOUDFLARE_API_TOKEN || 'uKwkN2WHsPYi79oNJ-71U7n9Hq0HquZ4Bmhu7wjY';
const accountId = process.env.CLOUDFLARE_ACCOUNT_ID || '8147f0100bb7ce99a5c143b6cf6976da';

console.log(`📍 Server Path: ${serverPath}`);
console.log(`🔑 API Token: ${apiToken.substring(0, 10)}...${apiToken.substring(apiToken.length - 5)}\n`);

// Set up environment
const env = {
  ...process.env,
  CLOUDFLARE_API_TOKEN: apiToken,
  CLOUDFLARE_ACCOUNT_ID: accountId
};

// Start the server
const server = spawn('node', [serverPath], { env });

let serverStarted = false;
let timeout;

server.stdout.on('data', (data) => {
  console.log(`✅ Server Output: ${data.toString().trim()}`);
  if (!serverStarted) {
    serverStarted = true;
    console.log('\n🎉 Server started successfully!');
    console.log('✨ The Cloudflare MCP server is now available in Claude Desktop.');
    console.log('\n📝 Next steps:');
    console.log('1. Restart Claude Desktop app');
    console.log('2. The "cloudflare-analyzer" server should now be available');
    console.log('3. You can use tools like analyze_zones, analyze_dns_records, etc.');

    clearTimeout(timeout);
    setTimeout(() => {
      console.log('\n🛑 Stopping test server...');
      server.kill();
      process.exit(0);
    }, 3000);
  }
});

server.stderr.on('data', (data) => {
  const message = data.toString().trim();
  if (message.includes('Cloudflare MCP server running')) {
    console.log(`✅ ${message}`);
    if (!serverStarted) {
      serverStarted = true;
      console.log('\n🎉 Server started successfully!');
      console.log('✨ The Cloudflare MCP server is now available in Claude Desktop.');
      console.log('\n📝 Next steps:');
      console.log('1. Restart Claude Desktop app');
      console.log('2. The "cloudflare-analyzer" server should now be available');
      console.log('3. You can use tools like analyze_zones, analyze_dns_records, etc.');

      clearTimeout(timeout);
      setTimeout(() => {
        console.log('\n🛑 Stopping test server...');
        server.kill();
        process.exit(0);
      }, 3000);
    }
  } else {
    console.error(`❌ Server Error: ${message}`);
  }
});

server.on('error', (error) => {
  console.error(`❌ Failed to start server: ${error.message}`);
  process.exit(1);
});

server.on('close', (code) => {
  if (code !== 0 && !serverStarted) {
    console.error(`❌ Server exited with code ${code}`);
    process.exit(code);
  }
});

// Timeout after 10 seconds
timeout = setTimeout(() => {
  if (!serverStarted) {
    console.error('❌ Server failed to start within 10 seconds');
    server.kill();
    process.exit(1);
  }
}, 10000);

console.log('⏳ Starting Cloudflare MCP server...\n');
