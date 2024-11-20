from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('customers/', views.CustomerListView.as_view(), name='customers'),
    path('jobs/', views.JobListView.as_view(), name='jobs'),
    path('jobs/new/', views.JobCreateView.as_view(), name='new_job'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='view_job'),
    path('jobs/<int:pk>/edit/', views.JobUpdateView.as_view(), name='edit_job'),
    path('leads/', views.LeadListView.as_view(), name='leads'),
    path('leads/new/', views.LeadCreateView.as_view(), name='new_lead'),
    path('leads/<int:pk>/', views.LeadDetailView.as_view(), name='lead_detail'),
    path('leads/<int:pk>/edit/', views.LeadUpdateView.as_view(), name='edit_lead'),
    path('leads/dashboard/', views.LeadDashboardView.as_view(), name='lead_dashboard'),
    # Add other URL patterns as needed
]
