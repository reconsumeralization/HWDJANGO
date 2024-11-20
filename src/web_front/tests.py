from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Customer, Property, Job, Lead

class JobModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.customer = Customer.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='jane.doe@hwroadasphalt.com',
            phone_number='+1234567890'
        )
        self.property = Property.objects.create(
            customer=self.customer,
            address='456 Elm St',
            city='Othertown',
            state='TX',
            zip_code='67890',
            square_footage=2000
        )
        self.job = Job.objects.create(
            title='Seal Asphalt Road',
            customer=self.customer,
            property=self.property,
            pavement_type='private_road',
            estimated_value=2500.00
        )

    def test_job_creation(self):
        self.assertEqual(self.job.title, 'Seal Asphalt Road')
        self.assertEqual(self.job.customer, self.customer)
        self.assertEqual(self.job.pavement_type, 'private_road')
        self.assertFalse(self.job.job_done)

    def test_job_str(self):
        self.assertEqual(str(self.job), 'Seal Asphalt Road - Private Road')

class LeadModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='leaduser', password='leadpass')
        self.lead = Lead.objects.create(
            first_name='John',
            last_name='Smith',
            email='john.smith@hwroadasphalt.com',
            phone_number='+1987654321',
            source='website',
            status='new'
        )

    def test_lead_creation(self):
        self.assertEqual(self.lead.first_name, 'John')
        self.assertEqual(self.lead.last_name, 'Smith')
        self.assertEqual(self.lead.status, 'new')

    def test_lead_str(self):
        self.assertEqual(str(self.lead), 'John Smith - New')

class JobViewTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='viewuser', password='viewpass')
        self.client.login(username='viewuser', password='viewpass')
        self.customer = Customer.objects.create(
            first_name='Alice',
            last_name='Johnson',
            email='alice.johnson@hwroadasphalt.com',
            phone_number='+1123456789'
        )
        self.property = Property.objects.create(
            customer=self.customer,
            address='789 Pine St',
            city='Sampletown',
            state='FL',
            zip_code='54321',
            square_footage=1800
        )
        self.job = Job.objects.create(
            title='Seal Driveway',
            customer=self.customer,
            property=self.property,
            pavement_type='driveway',
            estimated_value=800.00
        )

    def test_job_list_view(self):
        response = self.client.get(reverse('jobs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Seal Driveway')

    def test_job_detail_view(self):
        response = self.client.get(reverse('view_job', args=[self.job.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Seal Driveway')
        self.assertContains(response, 'Private Road')  # Adjust based on actual data

    def test_job_create_view(self):
        response = self.client.post(reverse('new_job'), {
            'title': 'Seal Parking Lot',
            'customer': self.customer.id,
            'property': self.property.id,
            'status': 'lead',
            'pavement_type': 'parking_lot',
            'estimated_value': 1500.00,
            'scheduled_date': '2023-12-01',
            'completion_date': '2023-12-15',
            'description': 'Seal the parking lot thoroughly.',
            'job_done': False,
            'job_seal_square_footage': 1200
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Job.objects.filter(title='Seal Parking Lot').exists())
