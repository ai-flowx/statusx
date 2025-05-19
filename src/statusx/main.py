import asyncio
import os
import requests
import time
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv()

app = FastAPI(
    title="statusx",
    description="ai status",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")


class Settings:
    DRIVEX_URL: str = os.getenv("DRIVEX_URL", "http://127.0.0.1")
    DRIVEX_KEY: str = os.getenv("DRIVEX_KEY", "")
    DRIVEX_TIMEOUT: int = int(os.getenv("DRIVEX_TIMEOUT", "6000"))


settings = Settings()


class ModelCheckRequest(BaseModel):
    models: Optional[List[str]] = Field(default=None, description="DriveX LLM models")
    timeout: Optional[int] = Field(default=None, description="Timeout in seconds")


class ModelHealthResponse(BaseModel):
    model: str
    status: str
    latency_ms: float
    error: Optional[str] = None


class ModelsHealthResponse(BaseModel):
    healthy: bool
    models: List[ModelHealthResponse]
    timestamp: float


def get_llm_models(timeout: int) -> List[str]:
    endpoint = f"{settings.DRIVEX_URL}/models"

    headers = {
        "Authorization": f"Bearer {settings.DRIVEX_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(
            endpoint,
            headers=headers,
            timeout=timeout
        )

        if response.status_code == 200:
            data = response.json()
            return [item["id"] for item in data["data"]]
        else:
            return []
    except Exception as _:
        return []


def check_model_health(model: str, timeout: int) -> ModelHealthResponse:
    start_time = time.time()

    endpoint = f"{settings.DRIVEX_URL}/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.DRIVEX_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Hello"}],
    }

    try:
        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,
            timeout=timeout
        )

        latency = (time.time() - start_time) * 1000  # Convert to milliseconds

        if response.status_code == 200:
            return ModelHealthResponse(
                model=model,
                status="healthy",
                latency_ms=round(latency, 2),
                error=None
            )
        else:
            try:
                error_detail = response.json().get("error", {}).get("message", str(response.text))
            except Exception:
                error_detail = str(response.text)
            return ModelHealthResponse(
                model=model,
                status="unhealthy",
                latency_ms=round(latency, 2),
                error=f"HTTP {response.status_code}: {error_detail}"
            )
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        return ModelHealthResponse(
            model=model,
            status="unhealthy",
            latency_ms=round(latency, 2),
            error=str(e)
        )


def verify_api_key():
    if not settings.DRIVEX_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="DRIVEX_KEY not configured"
        )


@app.get("/", tags=["Root"])
async def root():
    return FileResponse("static/index.html")


@app.get("/api", tags=["Root"])
async def api_root():
    return {
        "service": "statusx",
        "version": "1.0.0",
        "endpoints": {
            "/api/health": "Service health check",
            "/api/models/health": "Check health of multiple models",
            "/api/models/{model_id}/health": "Check health of a specific model",
        }
    }


@app.get("/api/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}


@app.post("/api/models/health", response_model=ModelsHealthResponse, tags=["Models"])
async def check_models_health(
        request: ModelCheckRequest = None,
        _: None = Depends(verify_api_key)
):
    request = request or ModelCheckRequest()
    timeout = request.timeout or settings.DRIVEX_TIMEOUT

    loop = asyncio.get_event_loop()
    models_to_check = await loop.run_in_executor(None, get_llm_models, timeout)
    health_results = await asyncio.gather(*[
        loop.run_in_executor(None, check_model_health, model, timeout) for model in models_to_check
    ])

    all_healthy = all(result.status == "healthy" for result in health_results)

    return ModelsHealthResponse(
        healthy=all_healthy,
        models=health_results,
        timestamp=time.time()
    )


@app.get("/api/models/{model_id}/health", response_model=ModelHealthResponse, tags=["Models"])
async def check_specific_model(
        model_id: str,
        timeout: int = settings.DRIVEX_TIMEOUT,
        _: None = Depends(verify_api_key)
):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, check_model_health, model_id, timeout)

    if result.status != "healthy":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=result.model_dump()
        )

    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
