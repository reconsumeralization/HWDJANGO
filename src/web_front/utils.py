from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_job_created_email(job):
    subject = f"New Job Created: {job.title}"
    html_message = render_to_string('emails/job_created.html', {'job': job})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [job.customer.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

def send_job_updated_email(job):
    subject = f"Job Updated: {job.title}"
    html_message = render_to_string('emails/job_updated.html', {'job': job})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [job.customer.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
