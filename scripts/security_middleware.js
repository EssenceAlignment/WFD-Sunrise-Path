// Security Middleware for Runtime Protection
const crypto = require('crypto');

// Override Math.random with crypto.randomBytes for security
const originalRandom = Math.random;
Math.random = function() {
    const bytes = crypto.randomBytes(8);
    const value = parseInt(bytes.toString('hex'), 16) / 0xffffffffffffffff;
    return value;
};

// Input validation middleware
const securityMiddleware = (req, res, next) => {
    // Sanitize inputs
    const sanitize = (obj) => {
        if (typeof obj !== 'object' || obj === null) return obj;

        for (let key in obj) {
            if (obj.hasOwnProperty(key)) {
                // Remove potential injection patterns
                if (typeof obj[key] === 'string') {
                    obj[key] = obj[key]
                        .replace(/[<>]/g, '')
                        .replace(/javascript:/gi, '')
                        .replace(/on\w+=/gi, '');
                } else if (typeof obj[key] === 'object') {
                    sanitize(obj[key]);
                }
            }
        }
        return obj;
    };

    req.body = sanitize(req.body);
    req.query = sanitize(req.query);
    req.params = sanitize(req.params);

    next();
};

module.exports = { securityMiddleware };
