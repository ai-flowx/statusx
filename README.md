# statusx

ai status that checks the health and availability of llm models.

## Features

- Check health of multiple OpenAI models concurrently
- Support for different model types (chat, image generation, text-to-speech)
- Configurable timeouts
- Detailed response with latency measurements
- Easy to deploy and use

## Installation

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

## Configuration

Create a `.env` file in the project root:

```
DRIVEX_URL=https://api.drivex.com/v1
DRIVEX_KEY=your_drivex_api_key
DRIVEX_TIMEOUT=30
```

## Usage

### Running with Docker Compose

```bash
# Create .env file from example
cp .env.example .env

# Edit .env with your API credentials
# Then start the service
docker-compose up -d
```

The server will be available at `http://localhost:8000`

### Running the server locally

```bash
# Start the server
uvicorn src.statusx.main:app --reload
```

The server will be available at `http://localhost:8000`

### API Endpoints

- `GET /`: Root endpoint with service information
- `GET /api/health`: Service health check
- `POST /api/models/health`: Check health of multiple models
- `GET /api/models/{model_id}/health`: Check health of a specific model

### Example Requests

Check default models:
```bash
curl -X POST http://localhost:8000/api/models/health
```

Check specific models:
```bash
curl -X POST http://localhost:8000/api/models/health \
  -H "Content-Type: application/json" \
  -d '{"models": ["gpt-4o", "gpt-3.5-turbo"], "timeout": 15}'
```

Check a single model:
```bash
curl http://localhost:8000/api/models/gpt-4o/health
```

## Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
