import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Config
from schema import OrderRequest, OrderResponse
from models import OrderStore
from services.ai_service import AIService
from services.order_service import OrderService
from routers import orders
# Log
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Drive Thru Ordering System",
    description="AI-powered drive-thru ordering system",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
order_store = OrderStore()
ai_service = AIService()
order_service = OrderService(order_store, ai_service)

app.state.order_store = order_store
app.state.ai_service = ai_service
app.state.order_service = order_service
app.include_router(orders.router, tags=["Orders"])

# Endpoints
@app.get("/")
def health_check():
    return {"status": "healthy", "message": "Drive Thru Ordering System API"}

@app.get("/health")
def detailed_health_check():
    return {"status": "healthy", "service": "drive-thru-api", "version": "1.0.0"}



# Startup
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG,
        log_level="info"
    )