import os
import io
import warnings
import numpy as np
import pandas as pd
import joblib

from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
from typing import Any, Dict, List, Literal, Optional

warnings.filterwarnings("ignore")

# ── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Student Exam Score Predictor",
    description=(
        "Predicts a student's exam score based on academic and personal factors.\n\n"
        "## Endpoints\n"
        "- **POST /predict** – Return a predicted exam score for a student.\n"
        "- **POST /predict/validate** – Validate a request body without running the model.\n"
        "- **GET /schema** – Return the full JSON schema for `StudentFeatures`.\n"
        "- **POST /retrain** – Upload a CSV to retrain the model.\n\n"
        "## Enum values (case-sensitive)\n"
        "All string fields must use **exact** capitalisation shown in the schema. "
        "For example `\"Medium\"` is valid; `\"medium\"` is not."
    ),
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

# Human-readable constraint hints used in validation error messages.
FIELD_HINTS: Dict[str, str] = {
    "Hours_Studied":              "integer between 1 and 44",
    "Attendance":                 "integer between 60 and 100",
    "Parental_Involvement":       'one of "Low", "Medium", "High" (case-sensitive)',
    "Access_to_Resources":        'one of "Low", "Medium", "High" (case-sensitive)',
    "Extracurricular_Activities": 'one of "No", "Yes" (case-sensitive)',
    "Sleep_Hours":                "integer between 4 and 10",
    "Previous_Scores":            "integer between 50 and 100",
    "Motivation_Level":           'one of "Low", "Medium", "High" (case-sensitive)',
    "Internet_Access":            'one of "No", "Yes" (case-sensitive)',
    "Tutoring_Sessions":          "integer between 0 and 8",
    "Family_Income":              'one of "Low", "Medium", "High" (case-sensitive)',
    "Teacher_Quality":            'one of "Low", "Medium", "High" (case-sensitive)',
    "School_Type":                'one of "Public", "Private" (case-sensitive)',
    "Peer_Influence":             'one of "Positive", "Negative", "Neutral" (case-sensitive)',
    "Physical_Activity":          "integer between 0 and 6",
    "Learning_Disabilities":      'one of "No", "Yes" (case-sensitive)',
    "Parental_Education_Level":   'one of "High School", "College", "Postgraduate" (case-sensitive)',
    "Distance_from_Home":         'one of "Near", "Moderate", "Far" (case-sensitive)',
}


class StudentFeatures(BaseModel):
    Hours_Studied: int = Field(
        ..., ge=1, le=44,
        description="Hours spent studying per week. Must be an integer from **1 to 44**.",
    )
    Attendance: int = Field(
        ..., ge=60, le=100,
        description="Attendance percentage. Must be an integer from **60 to 100**.",
    )
    Parental_Involvement: Literal["Low", "Medium", "High"] = Field(
        ...,
        description='Level of parental involvement. Accepted values: `"Low"`, `"Medium"`, `"High"` (case-sensitive).',
    )
    Access_to_Resources: Literal["Low", "Medium", "High"] = Field(
        ...,
        description='Access to learning resources. Accepted values: `"Low"`, `"Medium"`, `"High"` (case-sensitive).',
    )
    Extracurricular_Activities: Literal["No", "Yes"] = Field(
        ...,
        description='Participation in extracurricular activities. Accepted values: `"No"`, `"Yes"` (case-sensitive).',
    )
    Sleep_Hours: int = Field(
        ..., ge=4, le=10,
        description="Average sleep hours per night. Must be an integer from **4 to 10**.",
    )
    Previous_Scores: int = Field(
        ..., ge=50, le=100,
        description="Score achieved in the previous exam. Must be an integer from **50 to 100**.",
    )
    Motivation_Level: Literal["Low", "Medium", "High"] = Field(
        ...,
        description='Student motivation level. Accepted values: `"Low"`, `"Medium"`, `"High"` (case-sensitive).',
    )
    Internet_Access: Literal["No", "Yes"] = Field(
        ...,
        description='Whether the student has internet access. Accepted values: `"No"`, `"Yes"` (case-sensitive).',
    )
    Tutoring_Sessions: int = Field(
        ..., ge=0, le=8,
        description="Number of tutoring sessions attended per month. Must be an integer from **0 to 8**.",
    )
    Family_Income: Literal["Low", "Medium", "High"] = Field(
        ...,
        description='Family income level. Accepted values: `"Low"`, `"Medium"`, `"High"` (case-sensitive).',
    )
    Teacher_Quality: Literal["Low", "Medium", "High"] = Field(
        ...,
        description='Perceived quality of teaching. Accepted values: `"Low"`, `"Medium"`, `"High"` (case-sensitive).',
    )
    School_Type: Literal["Public", "Private"] = Field(
        ...,
        description='Type of school attended. Accepted values: `"Public"`, `"Private"` (case-sensitive).',
    )
    Peer_Influence: Literal["Positive", "Negative", "Neutral"] = Field(
        ...,
        description='Influence of peers on the student. Accepted values: `"Positive"`, `"Negative"`, `"Neutral"` (case-sensitive).',
    )
    Physical_Activity: int = Field(
        ..., ge=0, le=6,
        description="Hours of physical activity per week. Must be an integer from **0 to 6**.",
    )
    Learning_Disabilities: Literal["No", "Yes"] = Field(
        ...,
        description='Whether the student has a learning disability. Accepted values: `"No"`, `"Yes"` (case-sensitive).',
    )
    Parental_Education_Level: Literal["High School", "College", "Postgraduate"] = Field(
        ...,
        description='Highest education level of parents. Accepted values: `"High School"`, `"College"`, `"Postgraduate"` (case-sensitive).',
    )
    Distance_from_Home: Literal["Near", "Moderate", "Far"] = Field(
        ...,
        description='Distance from home to school. Accepted values: `"Near"`, `"Moderate"`, `"Far"` (case-sensitive).',
    )

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


class ValidationErrorDetail(BaseModel):
    field: str
    message: str
    expected: Optional[str] = None
    received: Optional[Any] = None


class ValidationErrorResponse(BaseModel):
    detail: str
    errors: List[ValidationErrorDetail]


class ValidateResponse(BaseModel):
    valid: bool
    message: str
    errors: Optional[List[ValidationErrorDetail]] = None


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


def _format_validation_errors(raw_errors: list) -> List[ValidationErrorDetail]:
    """
    Convert Pydantic v2 error dicts into human-readable ``ValidationErrorDetail``
    objects, enriched with the expected-value hint from ``FIELD_HINTS``.
    """
    details: List[ValidationErrorDetail] = []
    for err in raw_errors:
        # loc is a tuple, e.g. ('Hours_Studied',) or ('body', 'Hours_Studied')
        loc = err.get("loc", ())
        field = str(loc[-1]) if loc else "unknown"
        msg   = err.get("msg", "Invalid value")
        received = err.get("input")
        expected = FIELD_HINTS.get(field)
        details.append(
            ValidationErrorDetail(
                field=field,
                message=msg,
                expected=expected,
                received=received,
            )
        )
    return details


# ── Global validation-error handler ──────────────────────────────────────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Replace FastAPI's default 422 response with a richer payload that names
    every invalid field, explains what was received, and states what is expected.
    """
    errors = _format_validation_errors(exc.errors())
    return JSONResponse(
        status_code=422,
        content={
            "detail": (
                f"{len(errors)} validation error(s) in request body. "
                "Check the 'errors' list for field-level details."
            ),
            "errors": [e.model_dump() for e in errors],
        },
    )


# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "message": (
            "Student Exam Score Prediction API is running. "
            "Visit /docs for Swagger UI or /schema for the input schema."
        ),
    }


@app.get(
    "/schema",
    tags=["Schema"],
    summary="Return the JSON schema for StudentFeatures",
    response_description="JSON Schema object describing all required fields, types, and constraints",
)
def get_schema() -> Dict[str, Any]:
    """
    Returns the full JSON Schema for the ``StudentFeatures`` request body.

    Clients can use this schema to validate their payload locally before
    calling ``/predict``, avoiding unnecessary 422 errors.

    Key points:
    - All 18 fields are **required**.
    - Enum fields are **case-sensitive** (e.g. `"Medium"`, not `"medium"`).
    - Numeric fields have inclusive min/max constraints.
    """
    return StudentFeatures.model_json_schema()


@app.post(
    "/predict/validate",
    response_model=ValidateResponse,
    tags=["Prediction"],
    summary="Validate a StudentFeatures payload without running the model",
    responses={
        200: {"description": "Payload is valid or invalid — see the `valid` flag and `errors` list"},
    },
)
async def validate_predict(request: Request) -> ValidateResponse:
    """
    Accepts the same JSON body as ``/predict`` and validates it against the
    ``StudentFeatures`` schema **without** running the prediction model.

    - Returns `valid: true` when the payload is fully correct.
    - Returns `valid: false` with a detailed `errors` list when it is not,
      so clients can fix every problem before calling ``/predict``.

    This endpoint always returns **HTTP 200** — the `valid` flag in the body
    indicates whether the data passed validation.
    """
    try:
        body = await request.json()
    except Exception:
        return ValidateResponse(
            valid=False,
            message="Request body is not valid JSON.",
            errors=[
                ValidationErrorDetail(
                    field="body",
                    message="Could not parse request body as JSON.",
                    expected="A JSON object with all 18 StudentFeatures fields.",
                )
            ],
        )

    try:
        StudentFeatures.model_validate(body)
        return ValidateResponse(
            valid=True,
            message="Payload is valid. You can safely call POST /predict with this body.",
        )
    except ValidationError as exc:
        errors = _format_validation_errors(exc.errors())
        return ValidateResponse(
            valid=False,
            message=(
                f"{len(errors)} validation error(s) found. "
                "Fix the fields listed in 'errors' and try again."
            ),
            errors=errors,
        )


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(student: StudentFeatures):
    """
    Accepts a student's academic and personal features and returns
    the predicted exam score (0–100).

    All 18 fields are required. If any field fails validation, a **422**
    response is returned with a detailed `errors` list explaining exactly
    which fields are wrong and what values are expected.

    Use **POST /predict/validate** to pre-validate your payload, or
    **GET /schema** to retrieve the full field schema.
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