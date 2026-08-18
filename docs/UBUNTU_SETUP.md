# Ubuntu Setup Guide with AWS CLI

This guide explains how to set up and run the AI Kubernetes Agent on an Ubuntu machine with AWS CLI configured.

## Prerequisites

- Ubuntu 20.04 or later
- AWS CLI installed and configured with your AWS credentials
- kubectl installed
- Python 3.8 or later
- Node.js 18 or later
- Docker (optional, for containerized deployment)

## Verify AWS CLI Configuration

Before starting, verify your AWS CLI is properly configured:

```bash
# Check AWS CLI version
aws --version

# Verify AWS credentials
aws configure list

# Test AWS access by listing EKS clusters
aws eks list-clusters
```

If you see your EKS clusters listed, your AWS CLI is properly configured.

## Step 1: Clone the Repository

```bash
git clone <gerrit-repo-url>
cd ai-tagent
```

## Step 2: Backend Setup

### Install Python Dependencies

```bash
cd backend

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env file with your settings
nano .env
```

Add your Groq API key (get free key from https://console.groq.com/keys):

```bash
GROQ_API_KEY=gsk_your_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile
KUBECONFIG_PATH=~/.kube/config
```

### Verify kubectl Access

```bash
# Check kubectl version
kubectl version --client

# List available contexts (clusters)
kubectl config get-contexts

# Test cluster access
kubectl get nodes
```

### Start Backend Server

```bash
# From backend directory
python -m uvicorn main:app --reload --port 8000
```

Backend will start on http://localhost:8000

Verify it's working:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","service":"ai-kubernetes-agent"}
```

## Step 3: Frontend Setup

### Install Node.js Dependencies

```bash
cd ../frontend

# Install dependencies
npm install
```

### Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env.local

# Edit .env.local if needed (default should work)
nano .env.local
```

Default configuration:
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Start Frontend Development Server

```bash
npm run dev
```

Frontend will start on http://localhost:3000

## Step 4: Access the Application

1. Open your browser and navigate to http://localhost:3000
2. You should see the AI Kubernetes Agent dashboard
3. The cluster selector will show:
   - Clusters from your kubeconfig file
   - EKS clusters from your AWS account (via AWS CLI)
4. Select a cluster and click "Investigate Cluster"

## Step 5: Docker Deployment (Optional)

If you prefer to run with Docker:

```bash
# From project root
docker compose up --build
```

This will:
- Build and start the backend on port 8000
- Build and start the frontend on port 3000
- Use your configured environment variables

## Troubleshooting

### AWS CLI Not Working

If AWS CLI commands fail in the application:

```bash
# Verify AWS CLI is in PATH
which aws

# Test AWS CLI manually
aws eks list-clusters

# Reconfigure AWS CLI if needed
aws configure
```

### kubectl Not Working

If kubectl commands fail:

```bash
# Verify kubectl is installed
which kubectl

# Check kubeconfig
kubectl config view

# Test cluster access
kubectl get nodes
```

### Backend Fails to Start

```bash
# Check if port 8000 is already in use
lsof -i :8000

# Kill existing process if needed
kill -9 <pid>

# Try a different port
python -m uvicorn main:app --reload --port 8001
```

### Frontend Fails to Start

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check if port 3000 is in use
lsof -i :3000
```

## AWS-Specific Notes

### EKS Cluster Access

For EKS clusters, you may need to update kubeconfig:

```bash
# Update kubeconfig for a specific EKS cluster
aws eks update-kubeconfig --name <cluster-name> --region <region>

# Verify context is added
kubectl config get-contexts
```

### IAM Permissions

Ensure your AWS credentials have permissions to:
- `eks:ListClusters`
- `eks:DescribeCluster`
- `eks:UpdateKubeconfig`

### Multiple AWS Profiles

If you use multiple AWS profiles:

```bash
# List available profiles
aws configure list-profiles

# Use specific profile
export AWS_PROFILE=<profile-name>

# Verify
aws whoami
```

## Production Deployment

For production deployment on Ubuntu:

1. **Use systemd** to manage services
2. **Configure nginx** as reverse proxy
3. **Use environment variables** for secrets
4. **Enable HTTPS** with SSL certificates
5. **Set up monitoring** and logging

Example systemd service for backend:

```bash
sudo nano /etc/systemd/system/ai-kubernetes-agent.service
```

```ini
[Unit]
Description=AI Kubernetes Agent Backend
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/ai-tagent/backend
Environment="PATH=/path/to/ai-tagent/backend/.venv/bin"
ExecStart=/path/to/ai-tagent/backend/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable ai-kubernetes-agent
sudo systemctl start ai-kubernetes-agent
sudo systemctl status ai-kubernetes-agent
```

## Next Steps

After setup:
1. Test with a healthy cluster
2. Create test failure scenarios (see TEST_FAILURE_SCENARIOS.md)
3. Verify investigation history works
4. Test with multiple clusters

## Support

For issues:
- Check backend logs: `backend/.logs/` or systemd journal
- Check frontend browser console
- Verify AWS CLI and kubectl access
- Review environment variables
