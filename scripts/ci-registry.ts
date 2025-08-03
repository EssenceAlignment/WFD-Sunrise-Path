#!/usr/bin/env bun

/**
 * CIA Registry CLI Tool
 * Generates and validates integration manifests for Recovery Compass components
 */

import { readdir, stat, writeFile, readFile, access } from 'fs/promises';
import { join, basename } from 'path';
import { parse as parseYaml, stringify as stringifyYaml } from 'yaml';

// Type-only import for Ajv to avoid runtime dependency for now
type Ajv = any;
const Ajv = {} as any; // Will be replaced when ajv is installed

// Load schema
const SCHEMA_PATH = join(process.cwd(), 'integrations', 'registry.schema.json');
const INTEGRATIONS_DIR = join(process.cwd(), 'integrations');

interface IntegrationManifest {
  component_id: string;
  domain: string;
  owner: string;
  inputs: string[];
  outputs: string[];
  docs: string;
  tags?: string[];
  version?: string;
  dependencies?: Array<{ component_id: string; version: string }>;
  metrics_namespace?: string;
  data_classification?: 'public' | 'internal' | 'pii' | 'secret';
  status?: 'planning' | 'development' | 'alpha' | 'beta' | 'stable' | 'deprecated';
}

const DOMAIN_MAPPING: Record<string, string> = {
  'mobile': 'mobile',
  'mcp': 'mcp',
  'ai': 'ai-orchestration',
  'funding': 'funding',
  'metrics': 'observability',
  'security': 'security',
  'scripts': 'infrastructure',
  'src': 'frontend',
  'app': 'backend',
  'data': 'data'
};

async function loadSchema() {
  const schemaContent = await readFile(SCHEMA_PATH, 'utf-8');
  return JSON.parse(schemaContent);
}

async function validateManifest(manifest: any, schema: any): Promise<{ valid: boolean; errors?: any[] }> {
  const ajv = new Ajv({ allErrors: true });
  const validate = ajv.compile(schema);
  const valid = validate(manifest);

  return {
    valid: !!valid,
    errors: validate.errors || []
  };
}

async function generateManifestForComponent(componentPath: string): Promise<IntegrationManifest | null> {
  const componentName = basename(componentPath);
  const manifestPath = join(INTEGRATIONS_DIR, `${componentName}.yaml`);

  // Skip if manifest already exists
  try {
    await access(manifestPath);
    console.log(`✓ Manifest already exists for ${componentName}`);
    return null;
  } catch {
    // File doesn't exist, continue
  }

  // Determine domain based on path
  const pathParts = componentPath.split('/');
  let domain = 'infrastructure'; // default

  for (const part of pathParts) {
    if (DOMAIN_MAPPING[part]) {
      domain = DOMAIN_MAPPING[part];
      break;
    }
  }

  // Check for common file patterns to determine inputs/outputs
  const inputs: string[] = [];
  const outputs: string[] = [];

  try {
    const files = await readdir(componentPath);

    // Common patterns
    if (files.some(f => f.includes('api') || f.includes('server'))) {
      inputs.push('http_requests');
      outputs.push('api_responses');
    }

    if (files.some(f => f.includes('dashboard') || f.includes('ui'))) {
      outputs.push('ui_components');
    }

    if (files.some(f => f.includes('worker') || f.includes('processor'))) {
      inputs.push('task_queue');
      outputs.push('processed_data');
    }

    if (files.some(f => f.includes('test'))) {
      inputs.push('test_data');
      outputs.push('test_results');
    }
  } catch (e) {
    // Not a directory, skip
  }

  const manifest: IntegrationManifest = {
    component_id: componentName.toLowerCase().replace(/[^a-z0-9-]/g, '-'),
    domain: domain as any,
    owner: '@platform-team', // Default owner
    inputs: inputs.length > 0 ? inputs : ['configuration'],
    outputs: outputs.length > 0 ? outputs : ['logs'],
    docs: `docs/${componentName.toLowerCase()}.md`,
    tags: ['v0.1', 'auto-generated'],
    version: '0.1.0',
    data_classification: 'internal',
    status: 'development'
  };

  return manifest;
}

async function scanForNewComponents() {
  console.log('🔍 Scanning for new components...\n');

  const dirsToScan = ['src', 'app', 'scripts', 'mobile', 'mcp-launcher', 'cline-ai-orchestration'];
  const newManifests: Array<{ path: string; manifest: IntegrationManifest }> = [];

  for (const dir of dirsToScan) {
    const dirPath = join(process.cwd(), dir);

    try {
      const stats = await stat(dirPath);
      if (!stats.isDirectory()) continue;

      const manifest = await generateManifestForComponent(dirPath);
      if (manifest) {
        newManifests.push({ path: dirPath, manifest });
      }
    } catch (e) {
      // Directory doesn't exist, skip
    }
  }

  return newManifests;
}

async function validateAllManifests() {
  console.log('🔍 Validating all manifests...\n');

  const schema = await loadSchema();
  const files = await readdir(INTEGRATIONS_DIR);
  const yamlFiles = files.filter(f => f.endsWith('.yaml') || f.endsWith('.yml'));

  let allValid = true;

  for (const file of yamlFiles) {
    const filePath = join(INTEGRATIONS_DIR, file);
    const content = await readFile(filePath, 'utf-8');

    try {
      const manifest = parseYaml(content);
      const { valid, errors } = await validateManifest(manifest, schema);

      if (valid) {
        console.log(`✅ ${file} - Valid`);
      } else {
        console.log(`❌ ${file} - Invalid`);
        console.log('   Errors:', JSON.stringify(errors, null, 2));
        allValid = false;
      }
    } catch (e: any) {
      console.log(`❌ ${file} - Parse error: ${e.message}`);
      allValid = false;
    }
  }

  return allValid;
}

async function writeManifest(componentId: string, manifest: IntegrationManifest) {
  const filePath = join(INTEGRATIONS_DIR, `${componentId}.yaml`);
  const yamlContent = stringifyYaml(manifest, { lineWidth: 0 });

  await writeFile(filePath, yamlContent);
  console.log(`📝 Created manifest: ${filePath}`);
}

// CLI Commands
const commands = {
  async scan() {
    const newManifests = await scanForNewComponents();

    if (newManifests.length === 0) {
      console.log('✨ No new components found that need manifests');
      return;
    }

    console.log(`\nFound ${newManifests.length} components without manifests:\n`);

    for (const { path, manifest } of newManifests) {
      console.log(`Component: ${manifest.component_id}`);
      console.log(`  Path: ${path}`);
      console.log(`  Domain: ${manifest.domain}`);
      console.log(`  Inputs: ${manifest.inputs.join(', ')}`);
      console.log(`  Outputs: ${manifest.outputs.join(', ')}`);
      console.log('');
    }

    // In CI mode, auto-create manifests
    if (process.env.CI === 'true' || process.argv.includes('--auto')) {
      console.log('📝 Auto-creating manifests...\n');

      for (const { manifest } of newManifests) {
        await writeManifest(manifest.component_id, manifest);
      }
    }
  },

  async validate() {
    const allValid = await validateAllManifests();

    if (!allValid) {
      console.log('\n❌ Validation failed');
      process.exit(1);
    }

    console.log('\n✅ All manifests valid');
  },

  async generate(componentId: string) {
    if (!componentId) {
      console.error('❌ Component ID required');
      process.exit(1);
    }

    const manifest: IntegrationManifest = {
      component_id: componentId,
      domain: 'infrastructure',
      owner: '@platform-team',
      inputs: ['configuration'],
      outputs: ['logs'],
      docs: `docs/${componentId}.md`,
      version: '0.1.0',
      status: 'development'
    };

    await writeManifest(componentId, manifest);
  }
};

// Main CLI
async function main() {
  const command = process.argv[2];
  const args = process.argv.slice(3);

  try {
    switch (command) {
      case 'scan':
        await commands.scan();
        break;

      case 'validate':
        await commands.validate();
        break;

      case 'generate':
        await commands.generate(args[0]);
        break;

      default:
        console.log(`
Recovery Compass CIA Registry CLI

Commands:
  scan              Scan for components without manifests
  validate          Validate all existing manifests
  generate <id>     Generate a new manifest for component

Options:
  --auto           Auto-create manifests in scan mode

Examples:
  bun scripts/ci-registry.ts scan
  bun scripts/ci-registry.ts validate
  bun scripts/ci-registry.ts generate my-new-component
        `);
    }
  } catch (error: any) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

// Run if called directly
if (process.argv[1] === __filename || require.main === module) {
  main();
}
