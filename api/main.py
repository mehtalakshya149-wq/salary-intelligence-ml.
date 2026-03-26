from fastapi import FastAPI, Request
from api.auth import router as auth_router
from api.database import engine, Base
import api.models  # Required for metadata bindings
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("FastAPI_Interceptor")

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.warning(f"Skipping table creation (DB may be offline): {e}")

app = FastAPI(title="Authentication API")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    
    # Log the structural payload via the ELK/Datadog ready logger
    logger.info(f"Method: {request.method} | Path: {request.url.path} | Status: {response.status_code} | Latency: {process_time:.4f}s")
    
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.include_router(auth_router, tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Authentication Service is running. Visit /docs for OpenAPI documentation."}
