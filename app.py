from fastapi import FastAPI
import json
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALSModel
from pyspark.sql.functions import explode, col
import uvicorn

app = FastAPI(title="EchoWave API")

# Start Spark
spark = SparkSession.builder.appName("EchoWave_Backend").getOrCreate()

# Load ALS model
model = ALSModel.load("EchoWave_Model")

# Load genre labels
with open("genre_labels.json", "r") as f:
    genre_labels = json.load(f)

@app.get("/")
def home():
    return {"message": "EchoWave API is running!"}

@app.get("/recommend/{user_id}")
def recommend(user_id: int):

    # Convert userID to Spark-friendly format
    user_df = spark.createDataFrame([(user_id,)], ["userID_int"])

    # Get recommendations for this user
    recs = model.recommendForUserSubset(user_df, 5)

    # Explode recommendations
    recs = recs.withColumn("rec", explode("recommendations")) \
        .select(
            col("userID_int"),
            col("rec.genreIndex").alias("genreIndex"),
            col("rec.rating").alias("score")
        )

    results = []
    for row in recs.collect():
        idx = int(row["genreIndex"])
        genre = genre_labels[idx] if idx < len(genre_labels) else "Unknown"

        results.append({
            "genre": genre,
            "score": float(row["score"])
        })

    return {
        "user_id": user_id,
        "recommendations": results
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
