from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class EmailNotificationService:
    @staticmethod
    def send_lead_notification(lead):
        """Send notification when a new lead is created"""
        subject = f"New Lead: {lead.first_name} {lead.last_name}"
        context = {
            'lead': lead,
            'dashboard_url': settings.DASHBOARD_URL
        }

        html_content = render_to_string('emails/new_lead_notification.html', context)

        send_mail(
            subject=subject,
            message=strip_tags(html_content),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=html_content
        )

    @staticmethod
    def send_lead_status_update(lead):
        """Send notification when lead status changes"""
        subject = f"Lead Status Update: {lead.first_name} {lead.last_name}"
        context = {
            'lead': lead,
            'status': lead.get_status_display()
        }

        html_content = render_to_string('emails/lead_status_update.html', context)

        send_mail(
            subject=subject,
            message=strip_tags(html_content),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=html_content
        )
