import http from 'http';

const { CF_API_TOKEN, PORT = 8787 } = process.env;

if (!CF_API_TOKEN) {
  console.error('NO TOKEN – refuse OAuth fallback');      // hard‑fail
  process.exit(40);                                       // unique exit code
}

// Simple metrics tracking
let mcp_hits_total = 0;
let mcp_health_checks = 0;

http.createServer((req, res) => {
  // Add CORS headers for all responses
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.url === '/healthz') {
    mcp_health_checks++;
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('ok');
    return;
  }

  if (req.url === '/metrics') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end(`# HELP mcp_up MCP server is running
# TYPE mcp_up gauge
mcp_up 1

# HELP mcp_hits_total Total requests
# TYPE mcp_hits_total counter
mcp_hits_total ${mcp_hits_total}

# HELP mcp_health_checks_total Total health checks
# TYPE mcp_health_checks_total counter
mcp_health_checks_total ${mcp_health_checks}

# HELP mcp_oauth_fallback_total OAuth fallback attempts
# TYPE mcp_oauth_fallback_total counter
mcp_oauth_fallback_total 0
`);
    return;
  }

  // Count all other requests
  mcp_hits_total++;
  res.writeHead(404).end();
}).listen(PORT, () => {
  console.log(JSON.stringify({ boot: 'started', ts: Date.now(), port: PORT }));
});
