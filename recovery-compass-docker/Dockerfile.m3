# Multi-stage Dockerfile optimized for Apple M3 Pro
# Leverages ARM64 architecture and parallel processing

# Stage 1: Dependencies
FROM --platform=linux/arm64 node:20-alpine AS deps
WORKDIR /app

# Install dependencies in parallel
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# Stage 2: Development dependencies
FROM --platform=linux/arm64 node:20-alpine AS dev-deps
WORKDIR /app

COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Stage 3: Build stage (if needed)
FROM --platform=linux/arm64 node:20-alpine AS builder
WORKDIR /app

# Copy dependencies from previous stages
COPY --from=dev-deps /app/node_modules ./node_modules
COPY . .

# Build with M3 optimizations
ENV NODE_OPTIONS="--max-old-space-size=4096"
RUN npm run build || true

# Stage 4: Production runtime
FROM --platform=linux/arm64 node:20-alpine AS runtime
WORKDIR /app

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy production dependencies
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules

# Copy built application
COPY --chown=nodejs:nodejs . .

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Start with Node.js optimizations for M3
CMD ["node", "--max-old-space-size=4096", "--experimental-specifier-resolution=node", "server.js"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (res) => { process.exit(res.statusCode === 200 ? 0 : 1); })"
