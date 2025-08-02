import http from 'http';
const { CF_API_TOKEN, PORT = 8787 } = process.env;

if (!CF_API_TOKEN) {
  console.error('NO TOKEN – refuse OAuth fallback');      // hard‑fail
  process.exit(40);                                       // unique exit code
}

http.createServer((req, res) => {
  if (req.url === '/healthz') {
    res.writeHead(200).end('ok');
    return;
  }
  res.writeHead(404).end();
}).listen(PORT, () => {
  console.log(JSON.stringify({ boot: 'started', ts: Date.now() }));
});
