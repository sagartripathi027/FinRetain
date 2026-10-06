# 💳 FinRetain AI (MVP)

**Notice:** This project is an ML pipeline demonstration and internship portfolio MVP. It operates entirely on **synthetic/demo data** and is not a production-grade banking platform.

## Project Overview
FinRetain AI is a Django-based web application that predicts customer churn using a Machine Learning pipeline. It provides a clean dashboard to manage customers, run churn predictions, and view automated rule-based retention recommendations based on the prediction risk level.

## Features
- **User Authentication:** Secure signup, login, and logout.
- **Customer Management:** Full CRUD operations for customer profiles.
- **Churn Prediction:** Integration with a pre-trained scikit-learn ML pipeline to calculate churn probability.
- **Risk Classification:** Automatic assignment of LOW, MEDIUM, or HIGH risk.
- **Retention Recommendations:** Rule-based suggestions tailored to the customer's specific attributes and risk level.
- **Dashboard:** High-level metrics tracking total customers, risk distributions, and recent predictions.
- **Prediction History:** Persistent tracking of all historical predictions made for a customer.

## Tech Stack
- **Backend:** Django, Python
- **Machine Learning:** scikit-learn, Pandas, NumPy, Joblib (Logistic Regression Pipeline)
- **Database:** PostgreSQL (Production/Docker), SQLite (Local fallback)
- **Frontend:** HTML, CSS, Django Templates
- **Deployment:** Docker, Gunicorn

## Architecture
```text
User 
  ↓
Django Frontend (HTML/CSS)
  ↓
Django Backend (Authentication & Business Logic)
  ↓
predictions/services.py
  ↓
ml/models/churn_pipeline.joblib (Inference)
  ↓
PostgreSQL Database (Persistence)
```

## ML Approach
The current machine learning system is built upon a **synthetic/demo customer churn dataset**.
1. **Preprocessing:** Standard scaling and feature mapping.
2. **Model Evaluation:** Logistic Regression and Random Forest were evaluated.
3. **Selected Model:** **Logistic Regression** was chosen for its strong recall, explainability, and simplicity, making it ideal for this MVP.
4. **Integration:** The trained model is serialized using Joblib and loaded into memory by the Django backend for real-time inference without retraining.

## Data Scalability
The current project supports multiple CSV inputs through an automated ingestion layer, rather than hardcoding a single filename.

Example:
```text
ml/data/raw/
├── customer_001.csv
├── customer_002.csv
└── customer_003.csv
```

Data Flow:
```text
Multiple CSV files
        ↓
Ingestion (discovery & merging)
        ↓
Validation (schema & constraints)
        ↓
Unified dataset
        ↓
ML pipeline
```
*Note: The current implementation is designed for moderate-scale CSV data using Pandas. If the dataset eventually becomes too large for local storage or memory, the ingestion/storage layer can later be replaced with Parquet, Polars/DuckDB, object storage, or Apache Spark without redesigning the core Django prediction layer.*

## Database
The application is configured to use **PostgreSQL** in production (via `DATABASE_URL` environment variable) and seamlessly falls back to **SQLite** for zero-configuration local development.

## Project Structure
```text
FinRetain/
├── config/             # Django settings and root routing
├── customers/          # Customer CRUD and Dashboard views
├── predictions/        # ML inference services and prediction tracking
├── ml/                 # ML training scripts and serialized model artifacts
├── templates/          # HTML Templates (Base, Dashboard, Auth, etc.)
├── static/             # Static assets (if any)
├── Dockerfile          # Production Docker configuration
├── docker-compose.yml  # Local testing with PostgreSQL
└── requirements.txt    # Python dependencies
```

## Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secure-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://user:pass@host:5432/dbname
CSRF_TRUSTED_ORIGINS=https://your-deployment-url.com
```

## Local Setup
1. Clone the repository and create a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\activate
```
2. Install dependencies:
```powershell
pip install -r requirements.txt
```
3. Apply database migrations:
```powershell
python manage.py migrate
```

## Running Locally
Start the Django development server:
```powershell
python manage.py runserver
```
Visit `http://127.0.0.1:8000` to access the application.

## Running Tests
Run the comprehensive test suite (covers Auth, Models, Views, and ML Integration):
```powershell
python manage.py test
```

## Docker Usage
You can run the full application stack (Django + PostgreSQL) using Docker Compose:
```powershell
docker-compose up --build
```
The application will be accessible at `http://localhost:8000`.

## Deployment Notes
- **Target:** Hugging Face Spaces (or similar containerized platforms).
- **Security:** Ensure `DEBUG=False`, set a strong `SECRET_KEY`, configure `ALLOWED_HOSTS`, and set `CSRF_TRUSTED_ORIGINS` for HTTPS environments.
- **Static Files:** The Dockerfile automatically runs `collectstatic` for production serving.

## Limitations
- **Data:** Trained on synthetic/demo data; not representative of real financial market signals.
- **UI:** The frontend uses raw CSS without a heavy framework to remain lightweight and maintainable.
- **ML Artifact:** The serialized `churn_pipeline.joblib` file is tracked in git as it is required for deployment inference.

## Future Roadmap
- **V2 — DQN / Reinforcement Learning:** Transitioning from static rule-based retention recommendations to a dynamic agent that learns optimal retention strategies.
- **V3 — RAG:** Integrating a Retrieval-Augmented Generation layer to provide context-aware, knowledge-based explanations for AI decisions.
