# FINRETAIN — End-to-End Project Development Specification

## 1. Project Identity

**Project Name:** FinRetain

**Purpose:**  
FinRetain is an ML-powered customer retention platform. It analyzes customer and transaction-related data, predicts the probability that a customer may churn, classifies the customer's risk level, identifies important risk factors, and provides a retention strategy/recommendation.

**Primary Technology Requirement:**
- Backend: Django
- Frontend: Django Templates + HTML/CSS/JavaScript
- ML: Python + Pandas + NumPy + Scikit-learn
- Database: PostgreSQL
- API: Django REST Framework where appropriate
- Model serialization: Joblib
- Deployment: Docker + Hugging Face Spaces

The project must be implemented as a real, maintainable application rather than a simple ML demo.

---

## 2. Current Project Structure

```text
FinRetain/
│
├── manage.py
├── README.md
├── requirements.txt
├── Dockerfile
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
│
├── customers/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
│
├── predictions/
│   ├── models.py
│   ├── services.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
│
├── ml/
│   ├── data/
│   ├── models/
│   ├── notebooks/
│   └── src/
│       ├── preprocessing.py
│       ├── features.py
│       ├── train.py
│       ├── evaluate.py
│       └── __init__.py
│
├── templates/
└── static/
```

Do not rebuild the repository from scratch if existing implementation is present. First inspect and understand the existing code, then modify only what is necessary.

---

## 3. Final System Architecture

```text
                         ┌──────────────────────┐
                         │      USER / ADMIN    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   DJANGO FRONTEND    │
                         │                      │
                         │ HTML / CSS / JS      │
                         │ Dashboard            │
                         │ Forms                │
                         │ Reports              │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │        DJANGO BACKEND        │
                    │                              │
                    │ Authentication               │
                    │ Customer Management           │
                    │ Transaction Management        │
                    │ Prediction Views/API         │
                    │ Business Logic               │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
          ┌──────────────────┐          ┌──────────────────┐
          │   PostgreSQL     │          │   ML SERVICE     │
          │                  │          │                  │
          │ Users            │          │ Data Validation  │
          │ Customers        │          │ Preprocessing    │
          │ Transactions     │          │ Feature Engineer │
          │ Predictions      │          │ Trained Model    │
          │ Recommendations  │          │ Prediction       │
          └──────────────────┘          └────────┬─────────┘
                                                  │
                                                  ▼
                                      ┌────────────────────┐
                                      │  CHURN PREDICTION  │
                                      │                    │
                                      │ Probability        │
                                      │ Risk Classification│
                                      └─────────┬──────────┘
                                                │
                                                ▼
                                      ┌────────────────────┐
                                      │ RETENTION STRATEGY │
                                      │                    │
                                      │ Risk-based Action  │
                                      │ Recommendation     │
                                      └─────────┬──────────┘
                                                │
                                                ▼
                                      ┌────────────────────┐
                                      │   DJANGO DASHBOARD │
                                      │                    │
                                      │ Churn Score        │
                                      │ Risk Level         │
                                      │ Key Factors        │
                                      │ Recommendations    │
                                      └────────────────────┘
```

### Important architecture rule

The ML component is logically a separate **ML Service/module**, but it does not need to be a separate server for the first version.

The initial deployment can run Django and the ML inference pipeline in the same Docker application. The code must still keep ML logic separated from Django views.

Recommended connection:

```text
Django View/API
      ↓
predictions/services.py
      ↓
ML inference function
      ↓
ml/models/churn_pipeline.joblib
      ↓
Prediction
      ↓
Django response
```

---

## 4. Core Product Flow

### User Flow

```text
Signup / Login
      ↓
Dashboard
      ↓
Add / Upload Customer Data
      ↓
Validate Customer Data
      ↓
Run Churn Prediction
      ↓
Churn Probability
      ↓
Risk Level
      ↓
Important Risk Factors
      ↓
Retention Recommendation
      ↓
Save Prediction
      ↓
View Dashboard / History
```

### Admin Flow

```text
Admin Login
    ↓
Admin Dashboard
    ↓
Customer Overview
    ↓
Risk Distribution
    ↓
High-Risk Customers
    ↓
Prediction History
    ↓
Customer Details
    ↓
Retention Insights
```

---

## 5. ML Pipeline

The ML pipeline must be reproducible.

```text
Raw Dataset
    ↓
Data Validation
    ↓
Data Cleaning
    ↓
EDA
    ↓
Feature Engineering
    ↓
Train / Test Split
    ↓
Preprocessing
    ↓
Model Training
    ↓
Model Evaluation
    ↓
Model Selection
    ↓
Complete Pipeline Serialization
    ↓
churn_pipeline.joblib
```

### Training models

Start by comparing suitable classification models, for example:

- Logistic Regression
- Random Forest
- XGBoost, if included in the final dependency set

Do not assume one model is best before evaluation.

### Evaluation metrics

Report at minimum:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion Matrix

Churn prediction should not optimize only for accuracy. Recall, F1-score and ROC-AUC should be considered when selecting the final model.

---

## 6. Preprocessing Rule

Preprocessing used during training and inference must be identical.

Use a Scikit-learn Pipeline / ColumnTransformer so preprocessing and the estimator can be serialized together.

Conceptually:

```text
Input Features
      ↓
ColumnTransformer
 ├── Numerical preprocessing
 └── Categorical preprocessing
      ↓
ML Estimator
      ↓
Saved Pipeline
```

Save the complete pipeline, not only the model.

Expected artifact:

```text
ml/models/churn_pipeline.joblib
```

The `.joblib` file is generated after training. Do not create a fake placeholder model manually.

---

## 7. Django ↔ ML Integration

ML training and ML inference are different operations.

### Training

Training is performed separately:

```text
Dataset
 ↓
train.py
 ↓
evaluate.py
 ↓
Best Pipeline
 ↓
churn_pipeline.joblib
```

### Production inference

Django does NOT train the model when a user requests a prediction.

Instead:

```text
User Input
 ↓
Django Form/API Validation
 ↓
predictions/services.py
 ↓
Load Saved Pipeline
 ↓
pipeline.predict()
 ↓
pipeline.predict_proba()
 ↓
Risk Classification
 ↓
Retention Recommendation
 ↓
Save Prediction
 ↓
Return Dashboard Result
```

The saved model should be loaded efficiently. Avoid loading the model from disk on every request if a safe application-level caching/loading approach can be used.

---

## 8. Risk Classification

The application should convert churn probability into understandable risk categories.

Example starting policy:

```text
Probability < 0.30
→ LOW

0.30–0.70
→ MEDIUM

Probability > 0.70
→ HIGH
```

These thresholds are configurable and should not be presented as universally correct. They can be tuned after model evaluation and product requirements are finalized.

---

## 9. Retention Recommendation Engine

The system should not only display a probability.

It should also produce an actionable recommendation based on:

- Risk level
- Important customer features
- Recent activity
- Transaction behavior
- Complaints/service usage
- Other validated model/business signals

Example:

```text
Risk: HIGH

Churn Probability: 78%

Key Signals:
- Low recent activity
- Reduced transaction frequency
- Increased complaints

Recommended Action:
- Customer follow-up
- Service review
- Personalized retention offer
```

Recommendations must be based on available data and documented rules. Do not invent customer information.

---

## 10. Suggested Database Entities

The final schema should be designed after inspecting the actual requirements and dataset.

At minimum consider:

### User

Use Django authentication unless there is a strong reason for a custom user model.

### Customer

Possible fields:

```text
id
customer_id
name
email
tenure
balance
transaction_frequency
complaints
service_usage
created_at
updated_at
```

Exact fields must be determined from the final ML dataset and product requirements.

### Transaction

Possible fields:

```text
id
customer
amount
transaction_type
transaction_date
```

### Prediction

Possible fields:

```text
id
customer
churn_probability
risk_level
prediction
created_at
```

### RetentionRecommendation

Possible fields:

```text
id
prediction
recommendation
reason
created_at
```

Do not duplicate fields unnecessarily. Use proper Django relationships.

---

## 11. Django Applications

### customers

Responsible for:

- Customer model
- Customer forms
- Customer CRUD
- Customer data validation
- Customer dashboard information
- Admin registration

### predictions

Responsible for:

- Prediction model
- Prediction history
- Prediction views/API
- Calling ML inference
- Risk classification
- Retention recommendation
- Prediction results

### ml

Responsible for:

- Dataset
- Preprocessing
- Feature engineering
- Training
- Evaluation
- Model artifact

Django views should not contain ML training code.

---

## 12. File Responsibilities

### `ml/src/preprocessing.py`

Responsible for:

- Data cleaning
- Missing-value handling
- Data type handling
- Preprocessing configuration

### `ml/src/features.py`

Responsible for:

- Feature engineering
- Feature definitions
- Feature transformations that belong to the ML workflow

### `ml/src/train.py`

Responsible for:

- Loading dataset
- Splitting data
- Building candidate models
- Training
- Saving the best complete pipeline

### `ml/src/evaluate.py`

Responsible for:

- Evaluation metrics
- Confusion matrix
- Model comparison
- Evaluation output

### `predictions/services.py`

Responsible for:

- Loading/accessing trained pipeline
- Preparing validated input
- Running inference
- Returning prediction/probability
- Keeping ML integration outside views

---

## 13. UI Requirements

The application should have a professional dashboard.

### Main pages

```text
/login
/register
/dashboard
/customers
/customers/<id>
/predictions
/predictions/<id>
```

Exact URLs may change according to implementation.

### Dashboard should show

- Total customers
- High-risk customers
- Medium-risk customers
- Low-risk customers
- Average churn probability
- Risk distribution
- Recent predictions
- High-risk customer list

Use charts only where they improve understanding.

---

## 14. Security Requirements

Implement:

- Django authentication
- CSRF protection
- Django password hashing
- Form validation
- Permission checks
- Secure production settings
- Environment variables for secrets
- No hard-coded production credentials
- No committed `.env` files
- Safe file/data validation

If REST endpoints are exposed, apply appropriate authentication and permission controls.

---

## 15. Configuration

Production secrets/configuration must use environment variables.

Examples:

```text
SECRET_KEY
DEBUG
ALLOWED_HOSTS
DATABASE_URL
```

Do not commit real secrets.

Use a `.gitignore` for:

```text
.env
*.pyc
__pycache__/
*.sqlite3
ml/models/*.joblib
venv/
.venv/
```

Whether the trained model artifact should be committed or stored externally must be decided based on artifact size and deployment strategy.

---

## 16. Docker

The Docker setup must support:

```text
Django
+
ML dependencies
+
Production WSGI server
```

The container must be reproducible from the repository.

Before deployment verify:

```text
docker build
docker run
Django migrations
collectstatic
application startup
ML inference
```

---

## 17. Deployment Target

Target deployment:

**Hugging Face Spaces using Docker.**

Initial deployment architecture:

```text
Hugging Face Space
        │
        ▼
     Docker
        │
        ▼
     Django
        │
   ┌────┴────┐
   ↓         ↓
 PostgreSQL  ML Pipeline
             ↓
      churn_pipeline.joblib
```

If PostgreSQL is not practical inside the deployment environment, use an external managed PostgreSQL database through `DATABASE_URL`.

Do not put sensitive production database credentials into the repository.

---

## 18. Development Order

Follow this order unless existing code requires a different sequence:

### Phase 1 — Audit

1. Inspect every existing file.
2. Understand current code.
3. Identify incomplete/broken areas.
4. Do not overwrite working code unnecessarily.

### Phase 2 — Django Foundation

1. Configure settings.
2. Configure URLs.
3. Configure templates/static.
4. Configure environment variables.
5. Configure database.
6. Verify Django startup.

### Phase 3 — Database

1. Build Customer model.
2. Build Transaction model if required.
3. Build Prediction model.
4. Build RetentionRecommendation model.
5. Register useful models in admin.
6. Run migrations.

### Phase 4 — ML

1. Finalize dataset.
2. Analyze target distribution.
3. Clean data.
4. Define features.
5. Build preprocessing.
6. Train multiple candidate models.
7. Evaluate.
8. Select final model.
9. Save complete pipeline.

### Phase 5 — Integration

1. Create ML inference service.
2. Connect `predictions/services.py` to saved pipeline.
3. Validate Django input.
4. Run prediction.
5. Calculate risk level.
6. Generate retention recommendation.
7. Save result.

### Phase 6 — UI

1. Authentication pages.
2. Dashboard.
3. Customer list/detail.
4. Prediction form.
5. Prediction result.
6. Prediction history.
7. Admin dashboard.

### Phase 7 — Testing

Test:

- Authentication
- Forms
- Models
- CRUD
- Prediction service
- Invalid input
- Missing values
- ML inference
- Database persistence
- Permissions
- Production settings

### Phase 8 — Docker

Build and run locally.

### Phase 9 — Deployment

Deploy to Hugging Face Docker Space and verify the complete production flow.

### Phase 10 — Documentation

Update README with:

- Project overview
- Architecture
- Features
- ML approach
- Dataset
- Metrics
- Installation
- Environment variables
- Local run instructions
- Docker instructions
- Deployment
- API documentation
- Screenshots

---

## 19. Antigravity + Gemini Implementation Rules

This repository is intended to be developed using **Antigravity with a Gemini model**.

When analyzing this project:

1. Read this document completely before making changes.
2. Inspect the current repository before coding.
3. Do not assume files are empty or broken.
4. Do not rebuild the project from scratch when an existing implementation can be improved.
5. Preserve working functionality.
6. Follow the architecture defined here.
7. Keep Django business logic separate from ML training logic.
8. Keep ML inference integration inside a service/module, not directly inside large views.
9. Do not train the model during normal web requests.
10. Do not hard-code secrets.
11. Do not create fake ML outputs just to make the UI appear functional.
12. Do not claim model accuracy without actually evaluating the model.
13. Do not add unnecessary frameworks when Django already provides the required functionality.
14. Prefer simple, maintainable implementations.
15. Before changing architecture, explain why the existing architecture is insufficient.
16. After each major phase, verify the application before moving forward.
17. Fix errors at their source instead of hiding them.
18. Do not silently remove existing features.
19. Do not change product scope without explicit approval.
20. Keep the implementation consistent with this specification from development through deployment.

---

## 20. Gemini Execution Protocol

For each implementation task, Gemini should follow:

```text
READ
 ↓
INSPECT
 ↓
PLAN
 ↓
IMPLEMENT
 ↓
RUN / TEST
 ↓
VERIFY
 ↓
REPORT
```

Before editing:

```text
1. Identify relevant files.
2. Read their current contents.
3. Explain the intended change briefly.
4. Make the smallest correct change.
```

After editing:

```text
1. Run appropriate checks.
2. Run Django checks.
3. Run tests where available.
4. Verify imports.
5. Verify database migrations.
6. Verify ML inference when ML code changes.
```

Do not mark a task complete merely because code was written.

---

## 21. Definition of Done

FinRetain is considered complete only when:

- Django application starts successfully.
- Authentication works.
- PostgreSQL connection works in production configuration.
- Customer records can be created/viewed/managed.
- ML pipeline can be trained reproducibly.
- Final model is evaluated with documented metrics.
- Complete preprocessing + model pipeline is saved.
- Django can load the trained pipeline.
- A valid customer input produces a real prediction.
- Churn probability is displayed.
- Risk classification is displayed.
- Key risk signals are displayed where supported.
- Retention recommendation is generated from defined logic.
- Prediction is saved to the database.
- Prediction history works.
- Dashboard displays real database data.
- Security settings are production-aware.
- Docker build succeeds.
- Docker container starts successfully.
- Production deployment works.
- README explains setup and architecture.

---

## 22. Final Product Goal

FinRetain should demonstrate a complete real-world workflow:

```text
DATA
 ↓
MACHINE LEARNING
 ↓
MODEL EVALUATION
 ↓
MODEL SERIALIZATION
 ↓
DJANGO INTEGRATION
 ↓
REAL USER INPUT
 ↓
PREDICTION
 ↓
RISK ANALYSIS
 ↓
RETENTION RECOMMENDATION
 ↓
DATABASE
 ↓
DASHBOARD
 ↓
DOCKER
 ↓
DEPLOYMENT
```

The goal is not only to demonstrate an ML model.

The goal is to demonstrate an **end-to-end Django + Machine Learning product**.
