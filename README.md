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
| `GROQ_MODEL` | LLM model ID (default: `gemma2-9b-it`) |
| `KUBECONFIG_PATH` | Path to kubeconfig file |

**Frontend** (`frontend/.env.local`):

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_BASE_URL` | Backend API URL |

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Service health check |
| GET | `/clusters` | List available contexts from kubeconfig |
| POST | `/investigate` | Investigate cluster and return AI diagnosis |

### Get Clusters

```bash
curl http://localhost:8000/clusters
```

Returns list of available clusters from kubeconfig.

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

- **Multi-Cluster Support**: Discover and investigate clusters from kubeconfig
- **AI-Powered Diagnosis**: Uses Groq LLM for intelligent root cause analysis
- **Real-time Progress**: Visual investigation progress with step-by-step updates
- **Actionable Fixes**: Provides kubectl commands to fix identified issues
- **Investigation History**: Tracks past investigations in localStorage
- **Error Handling**: Beginner-friendly error messages for common issues
- **Healthy Cluster Detection**: Shows clean state when no issues found

## License

MIT

## Changelog

### 2026-08-19

**Problems Solved:**

1. **AWS CLI dependency removed**
   - **Problem**: Application required AWS CLI installation and configuration for EKS cluster discovery, adding complexity to deployment
   - **Solution**: Removed AWS EKS cluster discovery, now only uses kubeconfig for cluster management
   - **Impact**: Simplified deployment, reduced dependencies, easier setup

2. **Zero confidence on healthy clusters**
   - **Problem**: When cluster had no issues, confidence score was 0%, confusing users about system reliability
   - **Solution**: Added healthy cluster detection to return 100% confidence with appropriate message when no issues found
   - **Impact**: Clear indication of healthy cluster state, improved user trust

3. **Poor cluster selection UX**
   - **Problem**: Cluster selector had minimal visual feedback, making it hard to identify selected cluster
   - **Solution**: Enhanced cluster selector with gradient backgrounds, icons, checkmarks, and clear selected state
   - **Impact**: Better user experience, easier cluster identification, professional UI

4. **No LLM visibility**
   - **Problem**: Users couldn't tell when LLM was processing or how long it took
   - **Solution**: Added comprehensive LLM monitoring with backend logging, timing metrics, and UI indicators
   - **Impact**: Transparency in AI processing, performance monitoring, better debugging

5. **No way to hide investigation items**
   - **Problem**: Users couldn't remove items from investigation history without deleting all
   - **Solution**: Added delete button to hide individual items from UI without removing from localStorage
   - **Impact**: Better history management, cleaner UI, user control

**Technical Changes:**

- **Backend**:
  - Removed AWS EKS cluster discovery from `ClusterManager`
  - Added `is_cluster_healthy()` function for health detection
  - Added LLM timing to diagnosis response (`llm_duration_seconds`)
  - Added backend logging for LLM calls with timing

- **Frontend**:
  - Enhanced `ClusterSelector` with gradient backgrounds, icons, and selected state
  - Added purple theme and animation for AI Reasoning step in `InvestigationProgress`
  - Added LLM timing badge in `RootCauseCard`
  - Added delete button to `InvestigationHistory` items
  - Updated TypeScript interfaces for LLM timing

- **Documentation**:
  - Updated README to remove AWS CLI requirements
  - Updated API documentation for kubeconfig-only clusters

**Additional Fixes (2026-08-19):**

6. **Deprecated Groq model causing 400 errors**
   - **Problem**: Application used decommissioned Groq model `llama-3.1-70b-versatile`, causing 400 errors during diagnosis
   - **Solution**: Updated to current model `llama-3.3-70b-versatile` in config, LLM client, and documentation
   - **Impact**: Fixed diagnosis functionality, updated to supported Groq model

7. **Cluster context switching failure**
   - **Problem**: Cluster discovery returned cluster names but context switching required context names, causing failures
   - **Solution**: Changed cluster discovery to return context names instead of cluster names from kubeconfig
   - **Impact**: Fixed multi-cluster context switching, improved cluster selection accuracy

**Technical Changes:**

- **Backend**:
  - Updated `groq_model` default from `llama-3.1-70b-versatile` to `llama-3.3-70b-versatile` in config
  - Updated fallback model in LLM client to `llama-3.3-70b-versatile`
  - Modified `ClusterManager.get_clusters()` to return context names instead of cluster names
  - Updated API documentation to reflect context-based cluster selection

- **Frontend**:
  - Updated UI labels from "Select Cluster" to "Select Context" for accuracy
  - Updated empty state message from "No clusters found" to "No contexts found"

- **Documentation**:
  - Updated README with new Groq model default
  - Updated API endpoint descriptions to reflect context-based operation
