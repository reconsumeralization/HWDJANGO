from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Job
from .utils import send_job_created_email, send_job_updated_email

@receiver(post_save, sender=Job)
def handle_job_save(sender, instance, created, **kwargs):
    if created:
        send_job_created_email(instance)
    else:
        send_job_updated_email(instance)
