from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Customer, Property, Job

class JobModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number='+1234567890'
        )
        self.property = Property.objects.create(
            customer=self.customer,
            address='123 Main St',
            city='Anytown',
            state='CA',
            zip_code='12345',
            square_footage=1500
        )
        self.job = Job.objects.create(
            title='Seal Driveway',
            customer=self.customer,
            property=self.property,
            pavement_type='driveway',
            estimated_value=500.00
        )

    def test_job_creation(self):
        self.assertEqual(self.job.title, 'Seal Driveway')
        self.assertEqual(self.job.customer, self.customer)
        self.assertEqual(self.job.pavement_type, 'driveway')
        self.assertFalse(self.job.job_done)

    def test_job_str(self):
        self.assertEqual(str(self.job), 'Seal Driveway - Driveway')

class JobViewsTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number='+1234567890'
        )
        self.property = Property.objects.create(
            customer=self.customer,
            address='123 Main St',
            city='Anytown',
            state='CA',
            zip_code='12345',
            square_footage=1500
        )

    def test_create_job_view(self):
        response = self.client.post(reverse('new_job'), {
            'title': 'Seal Parking Lot',
            'customer': self.customer.id,
            'property': self.property.id,
            'status': 'lead',
            'pavement_type': 'parking_lot',
            'estimated_value': 1500.00,
            'job_done': False,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Job.objects.filter(title='Seal Parking Lot').exists())
