<div align="center">

# 🚀 StatusX

**AI-powered status monitoring for LLM model health and availability**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00C7B7.svg)](https://fastapi.tiangolo.com/)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API Documentation](#-api-endpoints) • [Examples](#-example-requests)

</div>

---

## ✨ Features

- 🔄 **Concurrent Health Checks** - Monitor multiple models simultaneously
- 🎯 **Multi-Model Support** - Chat, Embedding, Image generation, and Reranker models
- ⚙️ **Configurable Timeouts** - Customize request timeouts per check
- 📊 **Detailed Metrics** - Real-time latency measurements and status reporting
- 🎨 **Beautiful Dashboard** - Modern, responsive web UI with real-time updates
- 🐳 **Easy Deployment** - Docker Compose ready with minimal configuration
- 📚 **Auto-Generated API Docs** - Interactive Swagger UI and ReDoc documentation

## 📦 Installation

### Option 1: Local Installation

```bash
# Clone the repository
git clone https://github.com/ai-flowx/statusx.git
cd statusx

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install .
```

### Option 2: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/ai-flowx/statusx.git
cd statusx

# Create .env file from example
cp .env.example .env

# Edit .env with your API credentials
# Start the service
docker-compose up -d
```

## ⚙️ Configuration

Create a `.env` file in the project root with the following variables:

```env
DRIVEX_URL=https://api.drivex.com/v1
DRIVEX_KEY=your_drivex_api_key
DRIVEX_TIMEOUT=30
```

| Variable | Description | Default |
|----------|-------------|---------|
| `DRIVEX_URL` | DriveX API base URL | `http://127.0.0.1` |
| `DRIVEX_KEY` | Your DriveX API key | Required |
| `DRIVEX_TIMEOUT` | Request timeout in seconds | `30` |

## 🚀 Usage

### Running with Docker Compose

```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

The server will be available at **`http://localhost:8000`**

### Running the server locally

```bash
# Start the development server
uvicorn src.statusx.main:app --reload

# Or use the run script
./script/run.sh
```

The server will be available at **`http://localhost:8000`**

### 🎨 Web Dashboard

Visit **`http://localhost:8000`** to access the beautiful, real-time monitoring dashboard featuring:

- ✅ System-wide health status
- 📊 Individual model status cards
- ⚡ Response latency metrics
- 🔄 Auto-refresh capability
- 🎯 Color-coded status indicators

## 📚 API Endpoints

### Health & Status

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Root endpoint with service information |
| `GET` | `/api` | API endpoint listing |
| `GET` | `/api/health` | Service health check |

### Chat Models 💬

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/models/health` | Check health of multiple chat models |
| `GET` | `/api/models/{model_id}/health` | Check health of a specific chat model |

### Embedding Models 🔍

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/embeddings/health` | Check health of multiple embedding models |
| `GET` | `/api/embeddings/{model_id}/health` | Check health of a specific embedding model |

### Image Models 🎨

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/images/health` | Check health of multiple image models |
| `GET` | `/api/images/{model_id}/health` | Check health of a specific image model |

### Reranker Models ⚡

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/rerankers/health` | Check health of multiple reranker models |
| `GET` | `/api/rerankers/{model_id}/health` | Check health of a specific reranker model |

## 💡 Example Requests

### Check Chat Models

```bash
curl -X POST http://localhost:8000/api/models/health
```

<details>
<summary>Response Example</summary>

```json
{
  "healthy": true,
  "models": [
    {
      "model": "gpt-4o",
      "status": "healthy",
      "latency_ms": 234.56,
      "error": null
    },
    {
      "model": "gpt-3.5-turbo",
      "status": "healthy",
      "latency_ms": 156.78,
      "error": null
    }
  ],
  "timestamp": 1704326400.0
}
```
</details>

### Check Embedding Models

```bash
curl -X POST http://localhost:8000/api/embeddings/health
```

### Check Image Models

```bash
curl -X POST http://localhost:8000/api/images/health
```

### Check Reranker Models

```bash
curl -X POST http://localhost:8000/api/rerankers/health
```

### Check Specific Model

```bash
# Check a specific chat model
curl http://localhost:8000/api/models/gpt-4o/health

# Check a specific reranker model
curl http://localhost:8000/api/rerankers/rerank-1/health
```

### Custom Timeout

```bash
curl -X POST http://localhost:8000/api/models/health \
  -H "Content-Type: application/json" \
  -d '{"timeout": 15}'
```

## 📖 Documentation

StatusX provides automatically generated interactive API documentation:

- **Swagger UI**: [`http://localhost:8000/docs`](http://localhost:8000/docs) - Interactive API explorer
- **ReDoc**: [`http://localhost:8000/redoc`](http://localhost:8000/redoc) - Clean API reference documentation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [DriveX API](https://drivex.com/) - LLM model provider

---

<div align="center">

Made with ❤️ by the StatusX Team

[Report Bug](https://github.com/ai-flowx/statusx/issues) · [Request Feature](https://github.com/ai-flowx/statusx/issues)

</div>
