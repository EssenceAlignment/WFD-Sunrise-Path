#!/usr/bin/env node

/**
 * IPFS Artifact Pinning Script
 * Pins mobile test artifacts to IPFS for tamper-proof evidence
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { spawn } = require('child_process');

// Configuration
const PINATA_API_KEY = process.env.PINATA_API_KEY;
const PINATA_SECRET_KEY = process.env.PINATA_SECRET_KEY;
const WEB3_STORAGE_TOKEN = process.env.WEB3_STORAGE_TOKEN;

// Artifact paths
const ARTIFACTS = {
  performanceMetrics: 'performance-metrics.json',
  edgeLatency: 'edge-storage-latency.json',
  securityMetrics: 'security-metrics.json',
  testResults: 'test-results/summary.json',
  screenshots: 'screenshots/',
  videos: 'videos/',
  report: 'playwright-report/'
};

// Provenance record
const provenanceRecord = {
  timestamp: new Date().toISOString(),
  runId: process.env.GITHUB_RUN_ID || `local-${Date.now()}`,
  artifacts: {},
  hashes: {},
  ipfs: {}
};

async function calculateHash(filePath) {
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash('sha256');
    const stream = fs.createReadStream(filePath);

    stream.on('data', data => hash.update(data));
    stream.on('end', () => resolve(hash.digest('hex')));
    stream.on('error', reject);
  });
}

async function pinToIPFS(filePath, fileName) {
  if (WEB3_STORAGE_TOKEN) {
    return pinViaWeb3Storage(filePath, fileName);
  } else if (PINATA_API_KEY && PINATA_SECRET_KEY) {
    return pinViaPinata(filePath, fileName);
  } else {
    console.warn('⚠️  No IPFS service configured, skipping pin');
    return null;
  }
}

async function pinViaWeb3Storage(filePath, fileName) {
  const FormData = require('form-data');
  const fetch = require('node-fetch');

  const form = new FormData();
  form.append('file', fs.createReadStream(filePath), fileName);

  const response = await fetch('https://api.web3.storage/upload', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${WEB3_STORAGE_TOKEN}`
    },
    body: form
  });

  if (!response.ok) {
    throw new Error(`Web3.storage error: ${response.statusText}`);
  }

  const result = await response.json();
  return result.cid;
}

async function pinViaPinata(filePath, fileName) {
  const FormData = require('form-data');
  const fetch = require('node-fetch');

  const form = new FormData();
  form.append('file', fs.createReadStream(filePath), fileName);

  const metadata = JSON.stringify({
    name: fileName,
    keyvalues: {
      type: 'recovery-compass-test-artifact',
      runId: provenanceRecord.runId,
      timestamp: provenanceRecord.timestamp
    }
  });

  form.append('pinataMetadata', metadata);

  const response = await fetch('https://api.pinata.cloud/pinning/pinFileToIPFS', {
    method: 'POST',
    headers: {
      'pinata_api_key': PINATA_API_KEY,
      'pinata_secret_api_key': PINATA_SECRET_KEY,
      ...form.getHeaders()
    },
    body: form
  });

  if (!response.ok) {
    throw new Error(`Pinata error: ${response.statusText}`);
  }

  const result = await response.json();
  return result.IpfsHash;
}

async function createArtifactBundle() {
  console.log('📦 Creating artifact bundle...');

  // Create temporary directory for bundle
  const bundleDir = path.join(process.cwd(), '.artifact-bundle');
  if (!fs.existsSync(bundleDir)) {
    fs.mkdirSync(bundleDir);
  }

  // Copy all artifacts to bundle
  for (const [name, artifactPath] of Object.entries(ARTIFACTS)) {
    const fullPath = path.join(process.cwd(), artifactPath);

    if (fs.existsSync(fullPath)) {
      const destPath = path.join(bundleDir, name);

      if (fs.statSync(fullPath).isDirectory()) {
        // Copy directory
        copyDirectory(fullPath, destPath);
      } else {
        // Copy file
        fs.copyFileSync(fullPath, destPath);

        // Calculate hash
        const hash = await calculateHash(fullPath);
        provenanceRecord.hashes[name] = hash;
      }

      provenanceRecord.artifacts[name] = true;
    } else {
      console.warn(`⚠️  Artifact not found: ${artifactPath}`);
      provenanceRecord.artifacts[name] = false;
    }
  }

  // Add provenance record to bundle
  fs.writeFileSync(
    path.join(bundleDir, 'provenance.json'),
    JSON.stringify(provenanceRecord, null, 2)
  );

  return bundleDir;
}

function copyDirectory(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDirectory(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

async function createTarball(sourceDir) {
  const tarballPath = `${sourceDir}.tar.gz`;

  return new Promise((resolve, reject) => {
    const tar = spawn('tar', ['-czf', tarballPath, '-C', sourceDir, '.']);

    tar.on('close', (code) => {
      if (code === 0) {
        resolve(tarballPath);
      } else {
        reject(new Error(`Tar failed with code ${code}`));
      }
    });
  });
}

async function main() {
  console.log('🌐 IPFS Artifact Pinning');
  console.log('========================');

  try {
    // Create artifact bundle
    const bundleDir = await createArtifactBundle();

    // Create tarball
    const tarballPath = await createTarball(bundleDir);
    console.log(`📦 Created bundle: ${tarballPath}`);

    // Calculate bundle hash
    const bundleHash = await calculateHash(tarballPath);
    provenanceRecord.hashes.bundle = bundleHash;
    console.log(`🔐 Bundle hash: ${bundleHash}`);

    // Pin to IPFS
    const cid = await pinToIPFS(tarballPath, `recovery-compass-artifacts-${provenanceRecord.runId}.tar.gz`);

    if (cid) {
      provenanceRecord.ipfs.cid = cid;
      provenanceRecord.ipfs.url = `https://ipfs.io/ipfs/${cid}`;
      provenanceRecord.ipfs.gateway = `https://gateway.pinata.cloud/ipfs/${cid}`;

      console.log(`✅ Pinned to IPFS: ${cid}`);
      console.log(`🌐 IPFS URL: ${provenanceRecord.ipfs.url}`);
    }

    // Save final provenance record
    fs.writeFileSync(
      'artifact-provenance.json',
      JSON.stringify(provenanceRecord, null, 2)
    );

    console.log('📄 Provenance record saved to artifact-provenance.json');

    // Cleanup
    fs.rmSync(bundleDir, { recursive: true, force: true });
    fs.unlinkSync(tarballPath);

    // Output for CI
    if (process.env.CI) {
      console.log(`::set-output name=ipfs_cid::${cid}`);
      console.log(`::set-output name=bundle_hash::${bundleHash}`);
    }

  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { calculateHash, pinToIPFS, createArtifactBundle };
