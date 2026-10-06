from django.test import TestCase, Client
from django.contrib.auth.models import User
from customers.models import Customer
from django.urls import reverse

class CustomerCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.customer = Customer.objects.create(
            customer_id='CUST-TEST',
            name='Test Customer',
            email='test@example.com',
            tenure=5,
            balance=100.0,
            transaction_frequency=2,
            complaints=0,
            service_usage=0.5
        )

    def test_list_view(self):
        response = self.client.get(reverse('customers:customer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Customer')

    def test_detail_view(self):
        response = self.client.get(reverse('customers:customer_detail', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CUST-TEST')

    def test_create_customer(self):
        data = {
            'customer_id': 'CUST-NEW',
            'name': 'New Customer',
            'email': 'new@example.com',
            'tenure': 1,
            'balance': 0.0,
            'transaction_frequency': 1,
            'complaints': 0,
            'service_usage': 0.1
        }
        response = self.client.post(reverse('customers:customer_create'), data)
        self.assertEqual(response.status_code, 302) # Redirect on success
        self.assertEqual(Customer.objects.count(), 2)

    def test_invalid_create(self):
        data = {
            'customer_id': 'CUST-NEW',
            # missing required fields
        }
        response = self.client.post(reverse('customers:customer_create'), data)
        self.assertEqual(response.status_code, 200) # Re-render form with errors
        self.assertContains(response, 'This field is required')

    def test_update_customer(self):
        data = {
            'customer_id': 'CUST-TEST',
            'name': 'Updated Name',
            'email': 'test@example.com',
            'tenure': 5,
            'balance': 100.0,
            'transaction_frequency': 2,
            'complaints': 0,
            'service_usage': 0.5
        }
        response = self.client.post(reverse('customers:customer_update', args=[self.customer.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, 'Updated Name')

    def test_delete_customer(self):
        response = self.client.post(reverse('customers:customer_delete', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Customer.objects.count(), 0)


