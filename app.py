from fastapi import FastAPI, HTTPException
import json

app = FastAPI(title="EchoWave API")

# Load precomputed recommendations (generated in Colab)
with open("recommendations.json", "r") as f:
    data = json.load(f)

# Convert list → dict for fast lookup
recommendation_map = {item["user_id"]: item["recommendations"] for item in data}


@app.get("/")
def home():
    return {"message": "EchoWave API is running!"}


@app.get("/recommend/{user_id}")
def recommend(user_id: int):
    if user_id not in recommendation_map:
        raise HTTPException(status_code=404, detail="User ID not found")
    
    return {
        "user_id": user_id,
        "recommendations": recommendation_map[user_id]
    }
