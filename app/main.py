from fastapi import FastAPI

app = FastAPI(
    title="Healthcare Evidence Backend",
    version="1.0.0",
    description="Backend API for healthcare evidence management"
)

@app.get("/health")
def health_check():
    return{
        "status": "UP",
        "service": "healthcare-evidence-backend"
    }