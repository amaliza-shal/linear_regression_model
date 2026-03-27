import os
import io
import warnings
import numpy as np
import pandas as pd
import joblib

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal

warnings.filterwarnings("ignore")

# ── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Student Exam Score Predictor",
    description="Predicts a student's exam score based on academic and personal factors.",
    version="1.0.0",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
# Explicitly list allowed origins instead of using wildcard "*"
# This is required when allow_credentials=True and improves security.
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://10.0.2.2",        # Android emulator → host machine
    "http://10.0.2.2:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)

# ── Model paths ───────────────────────────────────────────────────────────────
MODEL_PATH  = "best_model.pkl"
SCALER_PATH = "scaler.pkl"
DATA_PATH   = "StudentPerformanceFactors.csv"

# ── Load model & scaler ───────────────────────────────────────────────────────
model  = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# Encoding maps (must match what was used in Task 1 training)
ENCODE = {
    "Parental_Involvement":    {"Low": 0, "Medium": 1, "High": 2},
    "Access_to_Resources":     {"Low": 0, "Medium": 1, "High": 2},
    "Extracurricular_Activities": {"No": 0, "Yes": 1},
    "Motivation_Level":        {"Low": 0, "Medium": 1, "High": 2},
    "Internet_Access":         {"No": 0, "Yes": 1},
    "Family_Income":           {"Low": 0, "Medium": 1, "High": 2},
    "Teacher_Quality":         {"Low": 0, "Medium": 1, "High": 2},
    "School_Type":             {"Public": 0, "Private": 1},
    "Peer_Influence":          {"Negative": 0, "Neutral": 1, "Positive": 2},
    "Learning_Disabilities":   {"No": 0, "Yes": 1},
    "Parental_Education_Level":{"High School": 0, "College": 1, "Postgraduate": 2},
    "Distance_from_Home":      {"Far": 0, "Moderate": 1, "Near": 2},
}

FEATURE_ORDER = [
    "Hours_Studied", "Attendance", "Parental_Involvement",
    "Access_to_Resources", "Extracurricular_Activities", "Sleep_Hours",
    "Previous_Scores", "Motivation_Level", "Internet_Access",
    "Tutoring_Sessions", "Family_Income", "Teacher_Quality",
    "School_Type", "Peer_Influence", "Physical_Activity",
    "Learning_Disabilities", "Parental_Education_Level", "Distance_from_Home",
]


# ── Pydantic schema ───────────────────────────────────────────────────────────
class StudentFeatures(BaseModel):
    Hours_Studied:              int   = Field(..., ge=1,  le=44,  description="Hours spent studying per week (1–44)")
    Attendance:                 int   = Field(..., ge=60, le=100, description="Attendance percentage (60–100)")
    Parental_Involvement:       Literal["Low", "Medium", "High"]
    Access_to_Resources:        Literal["Low", "Medium", "High"]
    Extracurricular_Activities: Literal["No", "Yes"]
    Sleep_Hours:                int   = Field(..., ge=4,  le=10,  description="Average sleep hours per night (4–10)")
    Previous_Scores:            int   = Field(..., ge=50, le=100, description="Score in previous exam (50–100)")
    Motivation_Level:           Literal["Low", "Medium", "High"]
    Internet_Access:            Literal["No", "Yes"]
    Tutoring_Sessions:          int   = Field(..., ge=0,  le=8,   description="Number of tutoring sessions per month (0–8)")
    Family_Income:              Literal["Low", "Medium", "High"]
    Teacher_Quality:            Literal["Low", "Medium", "High"]
    School_Type:                Literal["Public", "Private"]
    Peer_Influence:             Literal["Positive", "Negative", "Neutral"]
    Physical_Activity:          int   = Field(..., ge=0,  le=6,   description="Hours of physical activity per week (0–6)")
    Learning_Disabilities:      Literal["No", "Yes"]
    Parental_Education_Level:   Literal["High School", "College", "Postgraduate"]
    Distance_from_Home:         Literal["Near", "Moderate", "Far"]

    model_config = {
        "json_schema_extra": {
            "example": {
                "Hours_Studied": 20,
                "Attendance": 85,
                "Parental_Involvement": "Medium",
                "Access_to_Resources": "High",
                "Extracurricular_Activities": "Yes",
                "Sleep_Hours": 7,
                "Previous_Scores": 75,
                "Motivation_Level": "Medium",
                "Internet_Access": "Yes",
                "Tutoring_Sessions": 2,
                "Family_Income": "Medium",
                "Teacher_Quality": "High",
                "School_Type": "Public",
                "Peer_Influence": "Positive",
                "Physical_Activity": 3,
                "Learning_Disabilities": "No",
                "Parental_Education_Level": "College",
                "Distance_from_Home": "Near",
            }
        }
    }


class PredictionResponse(BaseModel):
    predicted_exam_score: float
    message: str


# ── Helper ────────────────────────────────────────────────────────────────────
def encode_and_scale(data: dict) -> np.ndarray:
    row = {}
    for feat in FEATURE_ORDER:
        val = data[feat]
        if feat in ENCODE:
            val = ENCODE[feat][val]
        row[feat] = val
    df_row = pd.DataFrame([row])[FEATURE_ORDER]
    scaled  = scaler.transform(df_row)
    return scaled


# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Student Exam Score Prediction API is running. Visit /docs for Swagger UI."}


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(student: StudentFeatures):
    """
    Accepts a student's academic and personal features and returns
    the predicted exam score.
    """
    try:
        X = encode_and_scale(student.model_dump())
        score = float(model.predict(X)[0])
        score = round(max(0.0, min(100.0, score)), 2)
        return PredictionResponse(
            predicted_exam_score=score,
            message="Prediction successful."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/retrain", tags=["Retraining"])
async def retrain(file: UploadFile = File(...)):
    """
    Upload a new CSV file with the same columns as the training data.
    The model will be retrained on the combined (old + new) dataset
    and saved back to disk.
    """
    global model, scaler

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    try:
        contents = await file.read()
        new_df   = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        required_cols = FEATURE_ORDER + ["Exam_Score"]
        missing = [c for c in required_cols if c not in new_df.columns]
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing columns: {missing}")

        # Load original data and combine
        original_df = pd.read_csv(DATA_PATH)
        combined_df = pd.concat([original_df, new_df], ignore_index=True)
        combined_df.dropna(subset=required_cols, inplace=True)

        # Encode categoricals
        for col, mapping in ENCODE.items():
            if col in combined_df.columns:
                combined_df[col] = combined_df[col].map(mapping)

        X = combined_df[FEATURE_ORDER].values
        y = combined_df["Exam_Score"].values

        # Re-fit scaler and model
        from sklearn.preprocessing import StandardScaler
        from sklearn.linear_model import LinearRegression

        new_scaler = StandardScaler()
        X_scaled   = new_scaler.fit_transform(X)

        new_model  = LinearRegression()
        new_model.fit(X_scaled, y)

        # Persist
        joblib.dump(new_model,  MODEL_PATH)
        joblib.dump(new_scaler, SCALER_PATH)

        model  = new_model
        scaler = new_scaler

        return {
            "message": "Model retrained successfully.",
            "new_training_rows": len(combined_df),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining error: {str(e)}")