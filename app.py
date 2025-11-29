from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI(title="EchoWave API")

# -------------------------------------------------------
# CORS: Required for Vercel frontend to call this API
# -------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow all — you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------
# Load precomputed recommendations (generated in Colab)
# -------------------------------------------------------
with open("recommendations.json", "r") as f:
    data = json.load(f)

# Convert list → dict for fast lookup
recommendation_map = {
    str(item["user_id"]): item["recommendations"] 
    for item in data
}

# -------------------------------------------------------
# Health check
# -------------------------------------------------------
@app.get("/")
def home():
    return {"message": "EchoWave API is running!"}

# -------------------------------------------------------
# Recommendation endpoint
# -------------------------------------------------------
@app.get("/recommend/{user_id}")
def recommend(user_id: int):

    user_str = str(user_id)  # because keys are strings

    if user_str not in recommendation_map:
        raise HTTPException(status_code=404, detail="User ID not found")
    
    return {
        "user_id": user_id,
        "recommendations": recommendation_map[user_str]
    }
