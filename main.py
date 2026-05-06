from fastapi import FastAPI
from routers import events

app = FastAPI(title="RoadSense API", description="4-Layer Architectural Backend")

# Include Layer 1 Routes
app.include_router(events.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
