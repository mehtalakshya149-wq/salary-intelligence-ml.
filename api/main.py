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
from api.dashboard import router as dashboard_router
app.include_router(dashboard_router, prefix="/api/v1/dashboard", tags=["dashboard"])
from api.chat import router as chat_router
app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])
from api.cost_of_living import router as cost_of_living_router
app.include_router(cost_of_living_router, prefix="/api/v1/cost-of-living", tags=["cost-of-living"])
from api.report import router as report_router
app.include_router(report_router, prefix="/api/v1/report", tags=["report"])
from api.model_comparison import router as model_comparison_router
app.include_router(model_comparison_router, prefix="/api/v1/models", tags=["models"])
from api.notifications import router as notifications_router
app.include_router(notifications_router, prefix="/api/v1/notifications", tags=["notifications"])
from api.admin import router as admin_router
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])
from api.bias_audit import router as bias_audit_router
app.include_router(bias_audit_router, prefix="/api/v1/bias-report", tags=["bias-audit"])
from api.skill_gap import router as skill_gap_router
app.include_router(skill_gap_router, prefix="/api/v1/skill-gap-analysis", tags=["skill-gap"])
from api.story_ai import router as story_ai_router
app.include_router(story_ai_router, prefix="/api/v1/explain-story", tags=["explain-story"])
from api.interview_prep import router as interview_prep_router
app.include_router(interview_prep_router, prefix="/api/v1/interview-questions", tags=["interview-prep"])
from api.resume_analyzer import router as resume_analyzer_router
app.include_router(resume_analyzer_router, prefix="/api/v1/analyze-resume", tags=["resume-analyzer"])
@app.get("/")
async def root():
    return {"message": "Authentication Service is running. Visit /docs for OpenAPI documentation."}
