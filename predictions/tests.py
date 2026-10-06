from django.test import TestCase
from django.contrib.auth.models import User
from customers.models import Customer
from predictions.models import Prediction, RetentionRecommendation
from predictions.services import classify_risk, generate_recommendation, run_churn_prediction, get_ml_pipeline
from django.urls import reverse
import os
import joblib
import pandas as pd
from django.conf import settings

class PredictionServicesTestCase(TestCase):
    def setUp(self):
        self.customer_low_risk = Customer.objects.create(
            customer_id='CUST-LOW',
            name='Low Risk',
            email='low@example.com',
            tenure=25,
            balance=100.0,
            transaction_frequency=10,
            complaints=0,
            service_usage=0.8
        )
        self.customer_high_risk = Customer.objects.create(
            customer_id='CUST-HIGH',
            name='High Risk',
            email='high@example.com',
            tenure=2,
            balance=0.0,
            transaction_frequency=1,
            complaints=3,
            service_usage=0.1
        )

    def test_classify_risk(self):
        self.assertEqual(classify_risk(0.2), 'LOW')
        self.assertEqual(classify_risk(0.5), 'MEDIUM')
        self.assertEqual(classify_risk(0.8), 'HIGH')

    def test_generate_recommendation(self):
        # Low risk
        rec, reason = generate_recommendation('LOW', self.customer_low_risk)
        self.assertEqual(rec, "Send loyalty appreciation reward.")
        self.assertIn("long-term user", reason)

        # High risk
        rec, reason = generate_recommendation('HIGH', self.customer_high_risk)
        self.assertEqual(rec, "Assign to specialized support immediately.")
        self.assertIn("Elevated complaints", reason)

    def test_model_loading_and_prediction(self):
        # Ensure the model exists before trying to run prediction
        model_path = os.path.join(settings.BASE_DIR, 'ml', 'models', 'churn_pipeline.joblib')
        if not os.path.exists(model_path):
            self.skipTest("ML Model artifact not found. Skipping prediction integration test.")
            
        prediction = run_churn_prediction(self.customer_high_risk)
        self.assertIsNotNone(prediction)
        self.assertEqual(prediction.customer, self.customer_high_risk)
        self.assertTrue(hasattr(prediction, 'recommendation'))

class PredictionViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.customer = Customer.objects.create(
            customer_id='CUST-TEST',
            name='Test Cust',
            email='test@example.com',
            tenure=5,
            balance=50.0,
            transaction_frequency=5,
            complaints=1,
            service_usage=0.5
        )

    def test_run_prediction_view_requires_auth(self):
        url = reverse('predictions:run_prediction', args=[self.customer.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_run_prediction_view_authenticated(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('predictions:run_prediction', args=[self.customer.pk])
        
        # Ensure the model exists before trying to run prediction
        model_path = os.path.join(settings.BASE_DIR, 'ml', 'models', 'churn_pipeline.joblib')
        if not os.path.exists(model_path):
            self.skipTest("ML Model artifact not found. Skipping view integration test.")

        response = self.client.post(url)
        self.assertRedirects(response, reverse('customers:customer_detail', args=[self.customer.pk]))
        
        # Verify prediction was created
        self.assertEqual(Prediction.objects.filter(customer=self.customer).count(), 1)
