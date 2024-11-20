from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

class LeadAnalyticsService:
    @staticmethod
    def get_lead_statistics(days=30):
        """Get lead statistics for the specified period"""
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)

        return {
            'total_leads': Lead.objects.filter(
                created_at__range=[start_date, end_date]
            ).count(),

            'conversion_rate': LeadAnalyticsService._calculate_conversion_rate(
                start_date, end_date
            ),

            'source_distribution': Lead.objects.filter(
                created_at__range=[start_date, end_date]
            ).values('source').annotate(
                count=Count('id')
            ),

            'status_distribution': Lead.objects.filter(
                created_at__range=[start_date, end_date]
            ).values('status').annotate(
                count=Count('id')
            )
        }

    @staticmethod
    def _calculate_conversion_rate(start_date, end_date):
        total = Lead.objects.filter(
            created_at__range=[start_date, end_date]
        ).count()

        converted = Lead.objects.filter(
            created_at__range=[start_date, end_date],
            status='converted'
        ).count()

        return (converted / total * 100) if total > 0 else 0
