#!/bin/bash

# Configuration
DROPLET_IP="159.223.196.97"
SSH_USER="root"
SSH_KEY_PATH="/tmp/do_ssh_key"

# Colors for output
GREEN='\033[0;32m'
NC='\033[0m'

# Save SSH key to temporary file
cat > $SSH_KEY_PATH << 'EOL'
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
EOL

chmod 600 $SSH_KEY_PATH

echo -e "${GREEN}🚀 Starting deployment...${NC}"

# Build frontend
echo -e "${GREEN}📦 Building frontend...${NC}"
cd ../frontend
npm install
npm run build

# Build backend
echo -e "${GREEN}📦 Building backend...${NC}"
cd ../backend
npm install
npm run build

# Create server directories
echo -e "${GREEN}📁 Creating server directories...${NC}"
ssh -i $SSH_KEY_PATH $SSH_USER@$DROPLET_IP "mkdir -p /var/www/autoreplyai/{frontend,backend}"

# Copy frontend files
echo -e "${GREEN}📤 Copying frontend files...${NC}"
rsync -avz -e "ssh -i $SSH_KEY_PATH" \
    --exclude 'node_modules' \
    --exclude '.next/cache' \
    .next \
    package.json \
    package-lock.json \
    public \
    $SSH_USER@$DROPLET_IP:/var/www/autoreplyai/frontend/

# Copy backend files
echo -e "${GREEN}📤 Copying backend files...${NC}"
cd ../backend
rsync -avz -e "ssh -i $SSH_KEY_PATH" \
    --exclude 'node_modules' \
    --exclude 'dist' \
    . \
    $SSH_USER@$DROPLET_IP:/var/www/autoreplyai/backend/

# Install dependencies and start services
echo -e "${GREEN}🔧 Installing dependencies and starting services...${NC}"
ssh -i $SSH_KEY_PATH $SSH_USER@$DROPLET_IP "cd /var/www/autoreplyai/frontend && \
    npm install --production && \
    cd ../backend && \
    npm install --production && \
    npx prisma generate && \
    pm2 delete all || true && \
    pm2 start 'npm start' --name 'frontend' --cwd /var/www/autoreplyai/frontend && \
    pm2 start 'npm start' --name 'backend' --cwd /var/www/autoreplyai/backend && \
    pm2 save"

# Cleanup
rm -f $SSH_KEY_PATH

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${GREEN}🌐 Your application is now live at: https://autoreplyai.io${NC}" 