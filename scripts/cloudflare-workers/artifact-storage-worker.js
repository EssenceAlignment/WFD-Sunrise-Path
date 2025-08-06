/**
 * Cloudflare Worker for QC Artifact Storage
 * Handles artifact uploads from GitHub Actions to R2 bucket
 * Generates signed URLs for GitHub release attachment
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // CORS headers for GitHub Actions
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      // Route handlers
      if (url.pathname === '/upload' && request.method === 'POST') {
        return await handleArtifactUpload(request, env, corsHeaders);
      }

      if (url.pathname.startsWith('/artifacts/') && request.method === 'GET') {
        return await handleArtifactDownload(request, env, corsHeaders);
      }

      if (url.pathname === '/pin-ipfs' && request.method === 'POST') {
        return await handleIPFSPinning(request, env, corsHeaders);
      }

      return new Response('Not Found', { status: 404, headers: corsHeaders });
    } catch (error) {
      console.error('Worker error:', error);
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }
  },
};

async function handleArtifactUpload(request, env, corsHeaders) {
  const formData = await request.formData();
  const file = formData.get('file');
  const runId = formData.get('runId');
  const artifactType = formData.get('type') || 'bundle';

  if (!file || !runId) {
    return new Response(JSON.stringify({ error: 'Missing required fields' }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  // Generate unique key
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const key = `artifacts/${runId}/${artifactType}_${timestamp}`;

  // Upload to R2
  await env.QC_ARTIFACTS.put(key, file.stream(), {
    httpMetadata: {
      contentType: file.type || 'application/octet-stream',
    },
    customMetadata: {
      runId,
      artifactType,
      uploadedAt: timestamp,
      fileName: file.name,
    },
  });

  // Generate signed URL (30-day expiry)
  const signedUrl = await generateSignedUrl(env, key, 30 * 24 * 60 * 60);

  // Store metadata in KV for quick lookups
  await env.ARTIFACT_METADATA.put(
    `run:${runId}`,
    JSON.stringify({
      key,
      signedUrl,
      uploadedAt: timestamp,
      expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
    }),
    { expirationTtl: 31 * 24 * 60 * 60 } // 31 days
  );

  return new Response(
    JSON.stringify({
      success: true,
      key,
      signedUrl,
      expiresIn: '30 days',
    }),
    {
      status: 200,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    }
  );
}

async function handleArtifactDownload(request, env, corsHeaders) {
  const url = new URL(request.url);
  const key = url.pathname.substring(1); // Remove leading slash

  const object = await env.QC_ARTIFACTS.get(key);

  if (!object) {
    return new Response('Artifact not found', {
      status: 404,
      headers: corsHeaders
    });
  }

  const headers = new Headers(object.httpMetadata || {});
  Object.entries(corsHeaders).forEach(([k, v]) => headers.set(k, v));

  return new Response(object.body, { headers });
}

async function handleIPFSPinning(request, env, corsHeaders) {
  const { key, runId } = await request.json();

  if (!key || !runId) {
    return new Response(JSON.stringify({ error: 'Missing key or runId' }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  // Get artifact from R2
  const object = await env.QC_ARTIFACTS.get(key);
  if (!object) {
    return new Response(JSON.stringify({ error: 'Artifact not found' }), {
      status: 404,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  // Pin to IPFS via Pinata or web3.storage
  const arrayBuffer = await object.arrayBuffer();
  const cid = await pinToIPFS(arrayBuffer, env);

  // Store CID in KV
  await env.ARTIFACT_METADATA.put(
    `ipfs:${runId}`,
    JSON.stringify({
      cid,
      key,
      pinnedAt: new Date().toISOString(),
    })
  );

  return new Response(
    JSON.stringify({
      success: true,
      cid,
      ipfsUrl: `https://ipfs.io/ipfs/${cid}`,
    }),
    {
      status: 200,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    }
  );
}

async function generateSignedUrl(env, key, expiresIn) {
  // For now, return a public URL
  // In production, implement proper signing
  const baseUrl = env.R2_PUBLIC_URL || 'https://qc-artifacts.recovery-compass.org';
  return `${baseUrl}/${key}`;
}

async function pinToIPFS(data, env) {
  // Implementation depends on your IPFS service
  // Example using web3.storage
  const formData = new FormData();
  formData.append('file', new Blob([data]));

  const response = await fetch('https://api.web3.storage/upload', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${env.WEB3_STORAGE_TOKEN}`,
    },
    body: formData,
  });

  const result = await response.json();
  return result.cid;
}
