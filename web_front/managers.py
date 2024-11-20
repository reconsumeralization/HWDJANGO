from django.db import models
from django.utils import timezone

class LeadManager(models.Manager):
    def active_leads(self):
        return self.exclude(status__in=['converted', 'unqualified'])

    def recent_leads(self, days=30):
        cutoff = timezone.now() - timezone.timedelta(days=days)
        return self.filter(created_at__gte=cutoff)

    def by_source(self, source):
        return self.filter(source=source)

class JobManager(models.Manager):
    def active_jobs(self):
        return self.exclude(status__in=['completed', 'cancelled'])

    def upcoming_jobs(self):
        return self.filter(
            scheduled_date__gte=timezone.now().date(),
            status='scheduled'
        )

    def overdue_jobs(self):
        return self.filter(
            scheduled_date__lt=timezone.now().date(),
            status__in=['scheduled', 'in-progress']
        )
