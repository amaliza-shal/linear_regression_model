# Student Exam Score Predictor

> **Predict student exam scores using machine learning** - Empowering educators to identify at-risk students early and provide targeted academic support.

---

## 🎯 Mission
To empower children from underserved communities by providing access to quality education through intelligent prediction systems, enabling educators to identify struggling students early and offer targeted support to help them succeed.

## 📊 Problem Statement
Many educators struggle to predict which students may struggle with upcoming exams. By analyzing academic performance and personal factors (study hours, attendance, family background, resources, motivation), we can build a predictive model to:
- Identify at-risk students early
- Enable proactive interventions
- Improve overall student success rates
- Reduce educational inequality

---

## 📈 Dataset
| Property | Details |
|----------|---------|
| **Source** | Kaggle - StudentPerformanceFactors |
| **Link** | https://www.kaggle.com/datasets/lainguyn123/student-performance-factors |
| **Total Records** | 6,607 students |
| **Features** | 20 academic and personal factors |
| **Target** | Exam Score (0-100) |

### Features Included
- **Academic**: Hours Studied, Attendance, Previous Scores, Tutoring Sessions
- **Personal**: Sleep Hours, Physical Activity, Motivation Level
- **Family**: Parental Involvement, Parental Education, Family Income
- **School**: Teacher Quality, School Type, Peer Influence, Distance from Home
- **Resources**: Access to Resources, Internet Access, Learning Disabilities
- **Activities**: Extracurricular Activities

---

## 🤖 Machine Learning Models
| Model | Status | Notes |
|-------|--------|-------|
| Linear Regression | ✅ Production | Currently deployed |
| Decision Tree | ✅ Tested | Alternative model |
| Random Forest | ✅ Tested | Ensemble approach |

---

## 🚀 Live API
The trained model is deployed and ready to use!

### **Base URL**
```
https://linearregressionmodel-production-b605.up.railway.app/
```

### **Interactive API Documentation**
```
https://linearregressionmodel-production-b605.up.railway.app/docs
```

### **API Endpoints**

#### 1. Health Check
```bash
https://linearregressionmodel-production-b605.up.railway.app/docs#/Health/root__get
```
**Response:**
```json
{
  "status": "ok",
  "message": "Student Exam Score Prediction API is running."
}
```

#### 2. Make a Prediction
```bash
POST https://linearregressionmodel-production-b605.up.railway.app/predict
Content-Type: application/json
```

**Request Example:**
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

**Response Example:**
```json
{
  "predicted_exam_score": 78.45,
  "message": "Prediction successful."
}
```

#### 3. Retrain Model (Upload New Data)
```bash
POST https://linearregressionmodel-production-b605.up.railway.app/retrain
Content-Type: multipart/form-data
```

---

## 📱 Flutter Mobile App

A complete Flutter application is included for easy mobile access to the prediction API.

### **Quick Start**

**Prerequisites:**
- Flutter 3.10+ installed
- Android emulator or physical device
- Internet connection

**Installation & Run:**
```bash
# Clone repository
git clone https://github.com/amaliza-shal/linear_regression_model.git
cd linear_regression_model/summative/flutter_app

# Install dependencies
flutter pub get

# Run the app
flutter run
```

**Features:**
- ✅ User-friendly form with all 18 input fields
- ✅ Real-time validation
- ✅ Loading indicators
- ✅ Direct connection to live API
- ✅ Beautiful UI with Material Design 3
- ✅ Error handling and messages

---

## 📁 Project Structure
```
linear_regression_model/
│
├── summative/
│   ├── linear_regression/
│   │   └── Multivariate.ipynb
│   │
│   ├── API/
│   │   ├── prediction.py
│   │   ├── requirements.txt
│   │   ├── best_model.pkl
│   │   ├── scaler.pkl
│   │   ├── StudentPerformanceFactors.csv
│   │   └── .python-version
│   │
│   └── flutter_app/
│       ├── lib/main.dart
│       ├── pubspec.yaml
│       ├── android/
│       └── ios/
│
├── README.md
├── runtime.txt
├── build.sh
└── .git/
```

---

## 🛠️ Technologies Stack

### **Backend**
- Python 3.11.9
- FastAPI
- scikit-learn
- pandas
- numpy
- joblib
- uvicorn

### **Frontend**
- Flutter/Dart
- HTTP

### **Deployment & DevOps**
- Railway
- GitHub
- Docker

### **Data Science**
- Jupyter Notebook
- StandardScaler
- Linear Regression

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| Model Type | Linear Regression |
| Training Samples | 6,607 |
| Features Used | 18 |
| Output Range | 0-100 (Exam Score %) |
| Training Status | ✅ Complete |

---

## 📸 Screenshots
*Flutter app interface showing form and prediction results*

---

## 🎬 Video Demo
[Link to YouTube demo - coming soon]

---

## 📝 How It Works

### **Pipeline:**
1. **User Input** → Flutter app collects student data
2. **Data Encoding** → Categorical variables converted to numeric
3. **Feature Scaling** → Data normalized using StandardScaler
4. **Model Prediction** → Linear Regression model predicts score
5. **Result Display** → Shows predicted score to user

### **Model Equation:**
```
Predicted Score = β₀ + β₁(Hour_Studied) + β₂(Attendance) + ... + β₁₈(Distance_from_Home)
```

---

## ✅ Quality Checklist

### **Backend (API)**
- ✅ FastAPI implementation with validation
- ✅ CORS enabled for mobile app
- ✅ Model serialization with joblib
- ✅ Error handling and logging
- ✅ Deployed on Railway with Python 3.11.9

### **Mobile App (Flutter)**
- ✅ HTTP package for API calls
- ✅ Form validation for all fields
- ✅ Loading states and error messages
- ✅ Material Design 3 UI
- ✅ Connected to live API

### **DevOps**
- ✅ runtime.txt for Python version
- ✅ build.sh for deployment
- ✅ requirements.txt with dependencies
- ✅ All files pushed to GitHub

---

## 🚀 Deployment Steps (Already Complete)

### **API Deployment on Railway:**
1. ✅ Repository pushed to GitHub
2. ✅ Connected project to Railway
3. ✅ Python 3.11.9 runtime configured
4. ✅ Dependencies specified in requirements.txt
5. ✅ Service deployed at https://linearregressionmodel-production-b605.up.railway.app

### **Flutter App:**
1. ✅ Project created and configured
2. ✅ HTTP dependency added
3. ✅ Connected to live API
4. ✅ All files pushed to GitHub

---

## 📞 Support & Troubleshooting

### **API Not Responding?**
- Check API status: https://linearregressionmodel-production-b605.up.railway.app
- View Railway logs for errors

### **Flutter App Won't Connect?**
- Verify internet connection
- Check API URL is correct in main.dart
- Restart the app

### **Prediction Seems Wrong?**
- Verify all input values are within valid ranges
- Check data encoding matches training data

---

## 👨‍💻 Contributors
- **Amaliza Shal** - Project Lead, Model Development, Deployment

---

## 📄 License
This project is open source and available under the MIT License.

---

## 🔗 Links
- **GitHub Repo**: https://github.com/amaliza-shal/linear_regression_model
- **Live API**: https://linearregressionmodel-production-b605.up.railway.app/docs
- **Dataset**: https://www.kaggle.com/datasets/lainguyn123/student-performance-factors

---

**Last Updated:** March 29, 2026  
**Status:** ✅ Production Ready 🚀
