# 💳 FinRetain AI — Customer Churn Prediction MVP

> **Project Notice:** FinRetain AI is an internship and portfolio-focused Machine Learning MVP built using synthetic/demo customer data. It is an educational demonstration, not a production-grade banking platform.

## 📌 Project Overview

FinRetain AI is a Django-based web application that predicts customer churn using a pre-trained Machine Learning pipeline. It provides a dashboard to manage customer records, estimate churn probability, classify customer risk, and generate rule-based retention recommendations.

The project demonstrates how Machine Learning can be integrated into a traditional web application to support data-driven customer retention decisions.

## ✨ Features

- **User Authentication:** Signup, login, and logout.
- **Customer Management:** Create, view, update, and delete customer records.
- **Churn Prediction:** Predict customer churn probability using a pre-trained scikit-learn pipeline.
- **Risk Classification:** Categorize customers into LOW, MEDIUM, or HIGH risk.
- **Retention Recommendations:** Generate rule-based suggestions based on customer attributes and predicted risk.
- **Interactive Dashboard:** Display customer statistics, risk distributions, and recent predictions.
- **Prediction History:** Maintain a history of customer churn predictions.
- **CSV Data Ingestion:** Discover, merge, and validate multiple CSV files through a dedicated ingestion layer.
- **Model Integration:** Load a serialized ML pipeline using Joblib for inference without retraining on every request.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, Django |
| Machine Learning | scikit-learn, Pandas, NumPy |
| Model Serialization | Joblib |
| ML Algorithm | Logistic Regression |
| Database | PostgreSQL, SQLite |
| Frontend | HTML, CSS, Django Templates |
| Production Server | Gunicorn |
| Containerization | Docker, Docker Compose |
| Testing | Django Test Framework, pytest |

## 🏗️ Architecture

```text
User
  ↓
Django Frontend (HTML/CSS)
  ↓
Django Backend
  ├── Authentication
  ├── Customer Management
  └── Dashboard
         ↓
  Prediction Service
         ↓
  Pre-trained ML Pipeline
  (churn_pipeline.joblib)
         ↓
  Churn Probability & Risk Level
         ↓
  Rule-based Retention Recommendations
         ↓
  Database
  (PostgreSQL / SQLite)
```

## 🤖 Machine Learning Approach

FinRetain AI uses a pre-trained Logistic Regression pipeline for customer churn prediction.

### ML Workflow

1. **Data Ingestion:** Discover and load CSV files from the raw data directory.
2. **Data Validation:** Validate the expected schema, data types, and applicable constraints.
3. **Preprocessing:** Apply the preprocessing steps defined in the trained pipeline.
4. **Model Training and Evaluation:** Logistic Regression and Random Forest were evaluated during model development.
5. **Model Selection:** Logistic Regression was selected for this MVP based on the intended balance of recall, interpretability, and simplicity.
6. **Model Serialization:** Save the fitted pipeline using Joblib.
7. **Inference:** Load the saved pipeline in Django to generate churn predictions.

The pipeline performs inference using the saved model rather than retraining for every prediction request.

> **Important:** The dataset contains synthetic/demo data. Model results should not be interpreted as evidence of real-world banking or financial prediction performance.

## 📊 Data Scalability

The project includes a CSV ingestion layer designed to discover and combine multiple input files instead of relying on a single hardcoded filename.

Example directory structure:

```text
ml/
└── data/
    └── raw/
        ├── customer_001.csv
        ├── customer_002.csv
        └── customer_003.csv
```

### Data Processing Flow

```text
Multiple CSV Files
        ↓
File Discovery & Ingestion
        ↓
Schema and Data Validation
        ↓
Data Merging and Deduplication
        ↓
Unified Dataset
        ↓
ML Pipeline
```

The current implementation uses Pandas and is intended for moderate-scale CSV processing, subject to available memory and storage.

For larger datasets, the ingestion and storage layer can be extended in the future without necessarily redesigning the core Django prediction workflow.

## 🗄️ Database

The application supports:

- **SQLite:** Lightweight, zero-configuration local development.
- **PostgreSQL:** Intended for production-style deployment through the `DATABASE_URL` environment variable.

Database configuration, migrations, and persistent storage must be configured appropriately for the target deployment environment.

## 📁 Project Structure

```text
FinRetain/
├── config/                  # Django settings and root routing
├── customers/               # Customer management and dashboard
├── predictions/             # ML inference and prediction tracking
├── ml/
│   ├── data/
│   │   └── raw/             # Raw CSV input files
│   └── models/
│       └── churn_pipeline.joblib
├── templates/               # Django HTML templates
├── static/                  # CSS, JavaScript, and static assets
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Local application stack
├── requirements.txt         # Python dependencies
└── manage.py                # Django management entry point
```

*Note: The structure above represents the intended project layout. Actual paths may differ slightly depending on the current repository.*

## ⚙️ Environment Variables

Create a `.env` file in the project root for local configuration.

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://postgres:yourpassword@db:5432/finretain
CSRF_TRUSTED_ORIGINS=
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=finretain
POSTGRES_USER=postgres
```

For deployment:

- Set `DEBUG=False`.
- Configure a strong, private `SECRET_KEY`.
- Set `ALLOWED_HOSTS` to the deployment hostname.
- Configure `DATABASE_URL` when using PostgreSQL.
- Set `CSRF_TRUSTED_ORIGINS` to the appropriate HTTPS origin.
- Never commit real secrets or production credentials to Git.

## 🚀 Local Setup

### 1. Clone the Repository

```powershell
git clone https://github.com/sagartripathi027/FinRetain.git
cd FinRetain
```

### 2. Create a Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```powershell
python manage.py migrate
```

### 5. Start the Development Server

```powershell
python manage.py runserver
```

Open the application at:

http://127.0.0.1:8000/

## 🐳 Docker Setup

If Docker and Docker Compose are installed and the configuration is complete, run:

```powershell
docker-compose up --build
```

The application is intended to be accessible at:

http://localhost:8000/

The PostgreSQL service, environment variables, model artifact, and application startup configuration must be correctly configured in the Docker setup.

## 🧪 Running Tests

Run the Django test suite:

```powershell
python manage.py test
```

Run the ML data-layer tests, if pytest and the relevant tests are available:

```powershell
pytest ml/src/test_data_layer.py
```

These commands help validate application behavior, prediction integration, and data processing. Test results depend on the current code and environment.

## 🔐 Security and Deployment

Before deploying the application:

- Disable Django debug mode.
- Configure secure environment variables.
- Validate allowed hosts and trusted HTTPS origins.
- Ensure database migrations run successfully.
- Verify that the ML model artifact is available at the expected path.
- Configure static-file collection and serving.
- Test authentication, customer operations, and predictions in the deployment environment.
- Confirm that the database uses persistent storage.

The project includes Docker-based deployment configuration intended for container-compatible hosting platforms. Actual deployment compatibility depends on the platform's runtime, resource limits, and configuration.

## ⚠️ Current Limitations

- **Synthetic Dataset:** The model is trained using synthetic/demo customer data, not real banking records.
- **Model Generalization:** Performance on synthetic data does not guarantee performance on real customers.
- **Rule-based Recommendations:** Retention suggestions use predefined rules rather than a learned optimization policy.
- **CSV Processing:** The current data ingestion layer uses Pandas and is subject to memory and processing limits.
- **Deployment:** Production security, persistent storage, and platform-specific configuration require verification.
- **Frontend:** The interface uses Django Templates and standard HTML/CSS to keep the application lightweight.

## 🔮 Future Roadmap — Coming Soon

The following capabilities are planned for future versions. They are not represented as completed features in the current MVP.

### 1. DQN / Reinforcement Learning

Explore Deep Q-Networks (DQN) and reinforcement learning to investigate adaptive retention strategies and sequential decision-making using simulated customer interactions.

### 2. Retrieval-Augmented Generation (RAG)

Integrate RAG to retrieve relevant knowledge and provide context-aware explanations for churn predictions and retention recommendations.

### 3. Apache Spark & Distributed Data Processing

Explore Apache Spark and distributed processing technologies to support larger datasets and more scalable data ingestion workflows when the project outgrows its current Pandas-based approach.

### 4. Microservices Architecture

Evaluate separating selected responsibilities into independently deployable services if future requirements justify the additional infrastructure and operational complexity.

## 🎯 Project Goals

FinRetain AI demonstrates practical skills in:

- Django application development.
- Machine Learning pipeline integration.
- Customer churn prediction and risk classification.
- CSV data ingestion and validation.
- Database-backed application workflows.
- Automated testing and Docker-based deployment.

The focus is on building a maintainable, explainable, and portfolio-ready ML MVP before introducing more advanced architecture and AI capabilities.

---

**Developed by Sagar Tripathi**

*FinRetain AI — A Machine Learning MVP for Customer Churn Prediction.*
