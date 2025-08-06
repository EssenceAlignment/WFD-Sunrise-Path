#!/usr/bin/env bun

/**
 * CIA Registry CLI Tool
 * Generates and validates integration manifests for Recovery Compass components
 */

import { readdir, stat, writeFile, readFile, access, mkdir } from 'fs/promises';
import { join, basename, dirname } from 'path';
import { parse as parseYaml, stringify as stringifyYaml } from 'yaml';

// Type-only import for Ajv to avoid runtime dependency for now
type Ajv = any;
const Ajv = {} as any; // Will be replaced when ajv is installed

// Load schema
const SCHEMA_PATH = join(process.cwd(), 'integrations', 'registry.schema.json');
const INTEGRATIONS_DIR = join(process.cwd(), 'integrations');
const EXPORTERS_DIR = join(process.cwd(), 'packages', 'obs-exporters');

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
  metrics_port?: number;
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
  },

  async exporters() {
    console.log('🚀 Generating Prometheus exporters...\n');

    // Ensure exporters directory exists
    await mkdir(EXPORTERS_DIR, { recursive: true });

    const files = await readdir(INTEGRATIONS_DIR);
    const yamlFiles = files.filter(f => f.endsWith('.yaml') || f.endsWith('.yml'));
    let generatedCount = 0;

    for (const file of yamlFiles) {
      const filePath = join(INTEGRATIONS_DIR, file);
      const content = await readFile(filePath, 'utf-8');

      try {
        const manifest = parseYaml(content) as IntegrationManifest;

        if (manifest.metrics_namespace) {
          const exporterPath = join(EXPORTERS_DIR, `exporter_${manifest.component_id}.ts`);

          // Check if exporter already exists
          try {
            await access(exporterPath);
            console.log(`✓ Exporter already exists for ${manifest.component_id}`);
            continue;
          } catch {
            // File doesn't exist, generate it
          }

          const exporterContent = generatePrometheusExporter(manifest);
          await writeFile(exporterPath, exporterContent);
          console.log(`📊 Generated exporter: ${exporterPath}`);
          generatedCount++;
        }
      } catch (e: any) {
        console.log(`❌ Error processing ${file}: ${e.message}`);
      }
    }

    if (generatedCount === 0) {
      console.log('✨ No new exporters needed');
    } else {
      console.log(`\n✅ Generated ${generatedCount} Prometheus exporters`);
    }
  },

  async doc() {
    const outputDir = process.argv.includes('--out')
      ? process.argv[process.argv.indexOf('--out') + 1]
      : 'docs/integrations';

    console.log(`📚 Generating documentation to ${outputDir}...\n`);

    // Ensure output directory exists
    await mkdir(outputDir, { recursive: true });

    const files = await readdir(INTEGRATIONS_DIR);
    const yamlFiles = files.filter(f => f.endsWith('.yaml') || f.endsWith('.yml'));
    const manifests: IntegrationManifest[] = [];

    // Load all manifests
    for (const file of yamlFiles) {
      const filePath = join(INTEGRATIONS_DIR, file);
      const content = await readFile(filePath, 'utf-8');

      try {
        const manifest = parseYaml(content) as IntegrationManifest;
        manifests.push(manifest);
      } catch (e: any) {
        console.log(`❌ Error loading ${file}: ${e.message}`);
      }
    }

    // Generate dependency graph
    const depGraph = generateDependencyGraph(manifests);

    // Generate docs for each component
    for (const manifest of manifests) {
      const docPath = join(outputDir, `${manifest.component_id}.md`);
      const docContent = generateComponentDoc(manifest, depGraph);

      await writeFile(docPath, docContent);
      console.log(`📝 Generated: ${docPath}`);
    }

    // Generate index page
    const indexPath = join(outputDir, 'index.md');
    const indexContent = generateIndexDoc(manifests, depGraph);
    await writeFile(indexPath, indexContent);
    console.log(`📝 Generated: ${indexPath}`);

    console.log(`\n✅ Generated documentation for ${manifests.length} components`);
  }
};

function generateDependencyGraph(manifests: IntegrationManifest[]): Map<string, Set<string>> {
  const graph = new Map<string, Set<string>>();

  for (const manifest of manifests) {
    if (!graph.has(manifest.component_id)) {
      graph.set(manifest.component_id, new Set());
    }

    if (manifest.dependencies) {
      for (const dep of manifest.dependencies) {
        graph.get(manifest.component_id)!.add(dep.component_id);
      }
    }
  }

  return graph;
}

function generateComponentDoc(manifest: IntegrationManifest, depGraph: Map<string, Set<string>>): string {
  const deps = depGraph.get(manifest.component_id) || new Set();
  const reverseDeps = new Set<string>();

  // Find components that depend on this one
  for (const [comp, compDeps] of depGraph.entries()) {
    if (compDeps.has(manifest.component_id)) {
      reverseDeps.add(comp);
    }
  }

  return `# ${manifest.component_id}

## Overview

**Domain**: ${manifest.domain}
**Owner**: ${manifest.owner}
**Version**: ${manifest.version || 'N/A'}
**Status**: ${manifest.status || 'N/A'}
**Data Classification**: ${manifest.data_classification || 'N/A'}

## Inputs/Outputs

### Inputs
${manifest.inputs.map(i => `- ${i}`).join('\n')}

### Outputs
${manifest.outputs.map(o => `- ${o}`).join('\n')}

## Dependencies

${deps.size > 0 ? '### Direct Dependencies' : '*No direct dependencies*'}
${Array.from(deps).map(d => `- ${d}`).join('\n')}

${reverseDeps.size > 0 ? '### Used By' : ''}
${Array.from(reverseDeps).map(d => `- ${d}`).join('\n')}

## Dependency Graph

\`\`\`mermaid
graph TD
    ${manifest.component_id}[${manifest.component_id}]
    ${Array.from(deps).map(d => `${d}[${d}] --> ${manifest.component_id}`).join('\n    ')}
    ${Array.from(reverseDeps).map(d => `${manifest.component_id} --> ${d}[${d}]`).join('\n    ')}
\`\`\`

## Metrics

${manifest.metrics_namespace ? `
- **Namespace**: ${manifest.metrics_namespace}
- **Port**: ${manifest.metrics_port || 'N/A'}
- **Endpoint**: http://localhost:${manifest.metrics_port || 9100}/metrics
` : '*No metrics configured*'}

## Tags

${manifest.tags ? manifest.tags.map(t => `\`${t}\``).join(' ') : '*No tags*'}

---
*Generated by CIA Registry*
`;
}

function generateIndexDoc(manifests: IntegrationManifest[], depGraph: Map<string, Set<string>>): string {
  const byDomain = new Map<string, IntegrationManifest[]>();

  // Group by domain
  for (const manifest of manifests) {
    if (!byDomain.has(manifest.domain)) {
      byDomain.set(manifest.domain, []);
    }
    byDomain.get(manifest.domain)!.push(manifest);
  }

  return `# Recovery Compass Integration Registry

## Overview

Total Components: **${manifests.length}**

## Components by Domain

${Array.from(byDomain.entries()).map(([domain, components]) => `
### ${domain} (${components.length})
${components.map(c => `- [${c.component_id}](./${c.component_id}.md) - ${c.status || 'development'}`).join('\n')}
`).join('\n')}

## Full Dependency Graph

\`\`\`mermaid
graph TD
${manifests.map(m => {
  const deps = depGraph.get(m.component_id) || new Set();
  return Array.from(deps).map(d => `    ${d} --> ${m.component_id}`).join('\n');
}).filter(Boolean).join('\n')}
\`\`\`

## Metrics Overview

| Component | Namespace | Port |
|-----------|-----------|------|
${manifests.filter(m => m.metrics_namespace).map(m =>
  `| ${m.component_id} | ${m.metrics_namespace} | ${m.metrics_port || 'N/A'} |`
).join('\n')}

---
*Generated by CIA Registry*
`;
}

function generatePrometheusExporter(manifest: IntegrationManifest): string {
  const port = manifest.metrics_port || 9100;
  const namespace = manifest.metrics_namespace || manifest.component_id.replace(/-/g, '_');

  return `/**
 * Prometheus Exporter for ${manifest.component_id}
 * Auto-generated by CIA Registry
 */

import express from 'express';
import { register, Counter, Histogram, Gauge } from 'prom-client';

// Component metadata
const COMPONENT_ID = '${manifest.component_id}';
const METRICS_PORT = ${port};
const NAMESPACE = '${namespace}';

// Default metrics
const httpRequestsTotal = new Counter({
  name: \`\${NAMESPACE}_http_requests_total\`,
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'path', 'status']
});

const requestDuration = new Histogram({
  name: \`\${NAMESPACE}_http_request_duration_seconds\`,
  help: 'HTTP request latency',
  labelNames: ['method', 'path'],
  buckets: [0.1, 0.5, 1, 2.5, 5, 10]
});

const activeConnections = new Gauge({
  name: \`\${NAMESPACE}_active_connections\`,
  help: 'Number of active connections'
});

const componentInfo = new Gauge({
  name: \`\${NAMESPACE}_info\`,
  help: 'Component information',
  labelNames: ['version', 'status', 'domain']
});

// Set component info
componentInfo.set({
  version: '${manifest.version || '0.1.0'}',
  status: '${manifest.status || 'development'}',
  domain: '${manifest.domain}'
}, 1);

// Express server for metrics endpoint
const app = express();

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.get('/healthz', (req, res) => {
  res.json({
    status: 'healthy',
    component: COMPONENT_ID,
    uptime: process.uptime()
  });
});

// Start server
app.listen(METRICS_PORT, () => {
  console.log(\`🚀 Prometheus exporter for \${COMPONENT_ID} running on port \${METRICS_PORT}\`);
  console.log(\`📊 Metrics available at http://localhost:\${METRICS_PORT}/metrics\`);
});

// Export metrics for use in application
export {
  httpRequestsTotal,
  requestDuration,
  activeConnections,
  componentInfo
};
`;
}

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

      case 'exporters':
        await commands.exporters();
        break;

      case 'doc':
        await commands.doc();
        break;

      default:
        console.log(`
Recovery Compass CIA Registry CLI

Commands:
  scan              Scan for components without manifests
  validate          Validate all existing manifests
  generate <id>     Generate a new manifest for component
  exporters         Generate Prometheus exporters for components with metrics
  doc               Generate documentation from manifests

Options:
  --auto           Auto-create manifests in scan mode
  --out <dir>      Output directory for doc command

Examples:
  bun scripts/ci-registry.ts scan
  bun scripts/ci-registry.ts validate
  bun scripts/ci-registry.ts generate my-new-component
  bun scripts/ci-registry.ts exporters
  bun scripts/ci-registry.ts doc --out docs/integrations
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
