# Security Fix: Insecure Randomness in Analytics

## Issue
The previous implementation used `Math.random()` to generate session IDs, which is not cryptographically secure. This made it easier for attackers to predict session IDs, potentially leading to session hijacking or other security vulnerabilities.

## Solution
We've replaced the insecure random number generation with cryptographically secure alternatives:

### Browser Environment
- Uses `window.crypto.getRandomValues()` from the Web Crypto API
- Generates 16 bytes (128 bits) of cryptographically secure random data
- Converts to hexadecimal string for the session ID

### Node.js Environment
- Uses `crypto.randomBytes()` from Node.js crypto module
- Falls back to `globalThis.crypto.getRandomValues()` for Node.js 15+
- Generates the same 16 bytes of secure random data

### Key Security Improvements
1. **Cryptographic Security**: Uses CSPRNG (Cryptographically Secure Pseudo-Random Number Generator)
2. **128-bit Entropy**: Provides sufficient randomness to prevent prediction
3. **Environment Detection**: Works seamlessly in both browser and Node.js environments
4. **Error Handling**: Throws clear errors if secure random generation is unavailable

## Migration Guide
If you have code that directly uses `generateSessionId()`, update it to use the secure version:

```typescript
// Old (insecure)
this.sessionId = this.generateSessionId();

// New (secure)
this.sessionId = this.generateSecureSessionId();
```

## Testing
Run the test suite to verify the secure implementation:
```bash
npm test src/lib/analytics.test.ts
```

## References
- [MDN: Crypto.getRandomValues()](https://developer.mozilla.org/en-US/docs/Web/API/Crypto/getRandomValues)
- [Node.js: crypto.randomBytes()](https://nodejs.org/api/crypto.html#cryptorandombytessize-callback)
- [OWASP: Insecure Randomness](https://owasp.org/www-community/vulnerabilities/Insecure_Randomness)
