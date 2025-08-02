# 🔒 Credential Inventory - CONFIDENTIAL
## Date: August 1, 2025

### Exposed Credentials (To Be Rotated)
1. **Supabase**
   - [ ] Service Role Key (CRITICAL)
   - [ ] Personal Token (sbp_*)

2. **AI Services**
   - [ ] OpenAI API Key (sk-proj-*)
   - [ ] Anthropic API Key (sk-ant-*)
   - [ ] Perplexity API Key (pplx-*)

3. **Infrastructure**
   - [ ] GitHub Personal Token (ghp_*)
   - [ ] GitHub MCP Token (github_pat_*)
   - [ ] Docker Token (dckr_pat_*)
   - [ ] Linear API Key (lin_api_*)
   - [ ] Airtable API Key (patMwDe*)

4. **Cloudflare**
   - [ ] API Token (already rotated)
   - [ ] Account ID (not secret, but noted)

5. **Firebase**
   - [ ] Service Account JSON (if exposed)

### Safe/Public Values
- Firebase Web API Key (public by design)
- Supabase URL (public)
- Supabase Anon Key (safe for client-side)
- Firebase Project ID
- Cloudflare Zone ID

### Storage Destinations
- **Cloudflare Secrets**: Application runtime secrets
- **macOS Keychain**: Admin/personal tokens
- **Local .env**: Development only (gitignored)

## DO NOT COMMIT THIS FILE
