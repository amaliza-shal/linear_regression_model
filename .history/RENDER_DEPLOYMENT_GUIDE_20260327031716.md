# Render Deployment Guide for Student Exam Score Prediction API

## Prerequisites
- GitHub account with the repository pushed (✅ Already done)
- Render.com account

---

## Step-by-Step Deployment Instructions

### **Step 1: Go to Render Dashboard**
1. Visit https://render.com
2. Sign in with your GitHub account (or create an account)
3. Click **"New +"** button in the top right

### **Step 2: Select Web Service**
1. Click **"Web Service"**
2. Select your GitHub repository: `linear_regression_model`
3. Click **"Connect"**

### **Step 3: Configure Deployment Settings**
Fill in the following fields:

| Field | Value |
|-------|-------|
| **Name** | `student-exam-predictor` |
| **Region** | `Oregon (or closest to you)` |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `bash build.sh` |
| **Start Command** | `cd summative/API && uvicorn prediction:app --host 0.0.0.0 --port 8000` |

### **Step 4: Environment Variables (Optional)**
- Leave empty for now (defaults will work)

### **Step 5: Plan Selection**
- Select **"Free"** plan (if you want)
- Or select **"Starter"** for better performance ($7/month)

### **Step 6: Deploy**
1. Click **"Create Web Service"**
2. Wait for deployment to complete (5-10 minutes)
3. You'll see a URL like: `https://student-exam-predictor.onrender.com`

---

## **Step 7: Access Your API**

Once deployed successfully, visit:
```
https://student-exam-predictor.onrender.com/docs
```

You'll see the Swagger UI documentation where you can test the `/predict` endpoint.

---

## **If Deployment Fails**

Check the **Logs** tab on Render. Common issues:

1. **"Python 3.14" error** → Already fixed with `runtime.txt`
2. **"requirements.txt not found"** → Already fixed with `build.sh`
3. **Build timeout** → May need Starter plan (builds faster)
4. **"Connection reset by peer"** → Render temporary issue, retry deployment

To retry: Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## **Testing Your API**

### Using Swagger UI (Easiest):
1. Go to `https://student-exam-predictor.onrender.com/docs`
2. Click the **"/predict"** endpoint to expand it
3. Click **"Try it out"**
4. Fill in sample student data:
   ```json
   {
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
     "Distance_from_Home": "Near"
   }
   ```
5. Click **"Execute"**
6. See the predicted exam score in the response!

### Using cURL (Terminal):
```bash
curl -X POST "https://student-exam-predictor.onrender.com/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
    "Distance_from_Home": "Near"
  }'
```

---

## **Share Your API**

Give others this link to use your API:
```
https://student-exam-predictor.onrender.com/docs
```

They can make predictions without needing to install anything locally!

---

## **API Endpoints Reference**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check |
| `/docs` | GET | Interactive API documentation (Swagger UI) |
| `/predict` | POST | Get exam score prediction |
| `/retrain` | POST | Upload new data and retrain the model |

---

## **Troubleshooting Tips**

✅ **Check Logs** → Click "Logs" tab on Render dashboard
✅ **Restart Service** → Click "Restart instance"
✅ **Manual Deploy** → Force a redeploy from latest commit
✅ **Check GitHub** → Make sure files are pushed to `main` branch

If all else fails, contact Render support: support@render.com

---
