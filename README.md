# AI Kubernetes Agent

On-demand Kubernetes troubleshooting powered by AI.

## Architecture

```text
Frontend (Next.js)
    ↓
FastAPI Backend (Orchestrator)
    ↓
Kubernetes Investigation Layer
    ↓
AI Kubernetes Agent
    ↓
LLM Reasoning (Groq - Free, Fast LLM API)
    ↓
Root Cause + Suggested Fix
    ↓
Frontend Diagnosis
```

## Quick Start

### Prerequisites

- Docker & Docker Compose (for containerized deployment)
- OR Python 3.8+, Node.js 18+, kubectl (for local development)
- AWS CLI configured (for EKS cluster discovery)
- Groq API key (free from https://console.groq.com/keys)

### Run with Docker

```bash
docker compose up --build
```

Access:

- Frontend: http://localhost:3000
- Backend health: http://localhost:8000/health

### Local Development (Ubuntu with AWS CLI)

For detailed Ubuntu setup with AWS CLI, see [docs/UBUNTU_SETUP.md](docs/UBUNTU_SETUP.md)

**Backend:**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Groq API key
uvicorn main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

### Local Development (Windows)

**Backend:**

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## Project Structure

```text
ai-kubernetes-agent/
├── backend/          # FastAPI orchestrator
├── frontend/         # Next.js UI
├── docs/             # Documentation
├── prompts/          # AI prompt templates
├── docker-compose.yml
└── README.md
```

## Environment Variables

**Backend** (`backend/.env`):

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Groq API key (get free key from https://console.groq.com/keys) |
| `GROQ_MODEL` | LLM model ID (default: `llama-3.1-70b-versatile`) |
| `KUBECONFIG_PATH` | Path to kubeconfig file |

**Frontend** (`frontend/.env.local`):

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_BASE_URL` | Backend API URL |

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Service health check |
| GET | `/clusters` | List available clusters (kubeconfig + AWS EKS) |
| POST | `/investigate` | Investigate cluster and return AI diagnosis |

### Get Clusters

```bash
curl http://localhost:8000/clusters
```

Returns list of available clusters from kubeconfig and AWS EKS.

### Investigate

```bash
curl -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{"cluster_name": "my-cluster"}'
```

Returns Kubernetes evidence plus AI-powered diagnosis:

```json
{
  "status": "success",
  "investigation": { "pods": {}, "logs": {}, "events": {}, "deployments": {}, "network": {} },
  "diagnosis": {
    "root_cause": "DATABASE_URL missing",
    "explanation": "Application cannot connect to DB.",
    "fix": "Add missing environment variable.",
    "kubectl_command": "kubectl edit deployment payment-service",
    "prevention_recommendation": "Validate required env vars at deploy time.",
    "confidence": 92,
    "confidence_reasoning": "High confidence because pod is CrashLoopBackOff and logs show missing env var."
  }
}
```

**Requirements:**
- `kubectl` configured with cluster access
- `GROQ_API_KEY` set in `backend/.env` (get free key from https://console.groq.com/keys)

## Current Status

- FastAPI backend with `/health`, `/clusters`, and `/investigate` endpoints
- Kubernetes Investigation Layer (kubectl-based evidence gathering)
- AI Reasoning Layer (Groq - Free LLM API)
- Next.js frontend with cluster selection and investigation dashboard
- Multi-cluster support (kubeconfig + AWS EKS)
- Investigation history with localStorage
- Comprehensive error handling
- Docker & Docker Compose configuration

## Documentation

- [Ubuntu Setup Guide](docs/UBUNTU_SETUP.md) - Detailed setup for Ubuntu with AWS CLI
- [Demo Presentation Guide](docs/DEMO_PRESENTATION_GUIDE.md) - 1-hour demo presentation structure
- [Test Failure Scenarios](docs/TEST_FAILURE_SCENARIOS.md) - Common Kubernetes failure scenarios for testing
- [Gerrit Setup Guide](docs/GERRIT_SETUP.md) - Instructions for pushing to Gerrit

## Features

- **Multi-Cluster Support**: Discover and investigate clusters from kubeconfig and AWS EKS
- **AI-Powered Diagnosis**: Uses Groq LLM for intelligent root cause analysis
- **Real-time Progress**: Visual investigation progress with step-by-step updates
- **Actionable Fixes**: Provides kubectl commands to fix identified issues
- **Investigation History**: Tracks past investigations in localStorage
- **Error Handling**: Beginner-friendly error messages for common issues
- **Healthy Cluster Detection**: Shows clean state when no issues found

## License

MIT
