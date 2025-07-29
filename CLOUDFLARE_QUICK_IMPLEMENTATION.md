# Cloudflare Quick Implementation Guide (Without MCP)

## 🚀 Direct Implementation of Key Features

Since the MCP server is having issues, here's how to implement the three key Cloudflare features directly:

## 1. Secrets Store Implementation

### Using Wrangler CLI

```bash
# Install Wrangler if not already installed
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Add secrets for Recovery Compass
wrangler secret put SUPABASE_SERVICE_KEY
# (Enter the key when prompted)

wrangler secret put QUALTRICS_TOKEN
# (Enter the token when prompted)

wrangler secret put OPENAI_API_KEY
# (Enter the key when prompted)

wrangler secret put STRIPE_SECRET_KEY
# (Enter the key when prompted)
```

### In Your Worker Code

```javascript
// Access secrets in your Worker
export default {
  async fetch(request, env) {
    // Secrets are available on the env object
    const supabaseKey = env.SUPABASE_SERVICE_KEY;
    const qualtricsToken = env.QUALTRICS_TOKEN;
    const openaiKey = env.OPENAI_API_KEY;
    
    // Use them in your code
    const supabase = createClient(supabaseUrl, supabaseKey);
    
    // Never log or return secrets in responses!
  }
}
```

## 2. Turnstile Implementation

### Step 1: Get Your Site Key

1. Go to: https://dash.cloudflare.com/?to=/:account/turnstile
2. Click "Add site"
3. Enter site name: "Recovery Compass"
4. Add your domains:
   - recovery-compass.org
   - localhost (for testing)
5. Choose widget mode: "Managed"
6. Copy your Site Key

### Step 2: Add to Your HTML

```html
<!-- Add to your funding form page -->
<!DOCTYPE html>
<html>
<head>
  <!-- Turnstile script -->
  <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
</head>
<body>
  <form id="funding-form">
    <!-- Your form fields -->
    <input type="text" name="name" placeholder="Your Name" required>
    <input type="email" name="email" placeholder="Email" required>
    
    <!-- Turnstile widget -->
    <div class="cf-turnstile" 
         data-sitekey="YOUR_SITE_KEY_HERE"
         data-callback="onTurnstileSuccess"
         data-error-callback="onTurnstileError">
    </div>
    
    <button type="submit">Submit Application</button>
  </form>

  <script>
    function onTurnstileSuccess(token) {
      // Token received, enable form submission
      document.querySelector('button[type="submit"]').disabled = false;
    }
    
    function onTurnstileError() {
      // Handle error
      alert('Please complete the security check');
    }
    
    // Initially disable submit button
    document.querySelector('button[type="submit"]').disabled = true;
  </script>
</body>
</html>
```

### Step 3: Verify on Backend

```javascript
// In your Worker or server
async function verifyTurnstile(token, ip) {
  const response = await fetch(
    'https://challenges.cloudflare.com/turnstile/v0/siteverify',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        secret: env.TURNSTILE_SECRET_KEY, // Add this as a secret
        response: token,
        remoteip: ip, // Optional
      }),
    }
  );
  
  const data = await response.json();
  return data.success;
}
```

## 3. AI Gateway Implementation

### Step 1: Create AI Gateway

1. Go to: https://dash.cloudflare.com/?to=/:account/ai/ai-gateway
2. Click "Create Gateway"
3. Name: "recovery-compass-ai"
4. Copy your Gateway URL

### Step 2: Update Your Code

```javascript
// Instead of calling OpenAI directly
// OLD:
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// NEW: Route through AI Gateway
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: "https://gateway.ai.cloudflare.com/v1/{account_id}/recovery-compass-ai/openai"
});

// Everything else stays the same!
const completion = await openai.chat.completions.create({
  messages: [{ role: "user", content: "Analyze this recovery story..." }],
  model: "gpt-4",
});
```

### Step 3: View Analytics

- Visit your AI Gateway dashboard to see:
  - Request counts
  - Token usage
  - Cost tracking
  - Response times
  - Error rates

## 📋 Implementation Checklist

### Today:
- [ ] Install Wrangler: `npm install -g wrangler`
- [ ] Login to Cloudflare: `wrangler login`
- [ ] Add first secret: `wrangler secret put SUPABASE_SERVICE_KEY`

### Tomorrow:
- [ ] Create Turnstile site in dashboard
- [ ] Add Turnstile to one form
- [ ] Test with localhost

### This Week:
- [ ] Migrate all API keys to Secrets Store
- [ ] Implement Turnstile on all public forms
- [ ] Create AI Gateway and update OpenAI calls

## 🎯 Quick Wins

1. **Secrets Store** improves security immediately
2. **Turnstile** removes Google dependency
3. **AI Gateway** provides instant cost visibility

## 🔧 Testing Commands

```bash
# List your secrets (names only, not values)
wrangler secret list

# Deploy with secrets
wrangler deploy

# Tail logs to debug
wrangler tail

# Check AI Gateway stats
curl https://api.cloudflare.com/client/v4/accounts/{account_id}/ai-gateway/gateways \
  -H "Authorization: Bearer {api_token}"
```

## 💡 Pro Tips

1. **Secrets**: Never commit secrets to Git, always use Wrangler
2. **Turnstile**: Test thoroughly on localhost before production
3. **AI Gateway**: Set up alerts for unusual usage patterns

## 🚨 If You Get Stuck

1. **Wrangler Issues**: Try `npm install -g wrangler@latest`
2. **Login Problems**: Use `wrangler login` in terminal, not VS Code
3. **Secret Issues**: Ensure you're in the correct project directory
4. **Turnstile**: Check that your domain is added in the dashboard

---

**Remember**: These features work independently of the MCP server. You can implement them right now without any blockers!

The MCP server is just a convenience tool - all Cloudflare features are accessible through:
- Wrangler CLI
- Cloudflare Dashboard
- Direct API calls

Your Recovery Compass infrastructure remains fully functional! 🚀
