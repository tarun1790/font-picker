# --- Stage 1: Build static assets ---
FROM node:22-slim AS builder

WORKDIR /app

# Copy package descriptors
COPY package*.json ./

# Install packages
RUN npm ci

# Copy application files
COPY . .

# Build production bundle
RUN npm run build

# --- Stage 2: Serve with Nginx ---
FROM nginx:alpine

# Copy built HTML/JS assets to Nginx default folder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy a lightweight custom Nginx configuration if routing is used
# (Fall back to index.html for SPA routers)
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html index.htm; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
