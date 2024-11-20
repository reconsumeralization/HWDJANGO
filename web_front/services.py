from decimal import Decimal
from typing import Optional
from django.db.models import Sum
from .models import Job, Customer, Property

class JobService:
    @staticmethod
    def calculate_job_quote(square_footage: int,
                          patch_footage: Optional[int] = None) -> Decimal:
        base_rate = Decimal('395.00')
        per_sqft_rate = Decimal('0.22')

        if square_footage <= 1000:
            seal_quote = base_rate
        else:
            extra_footage = square_footage - 1000
            seal_quote = base_rate + (extra_footage * per_sqft_rate)

        patch_quote = Decimal('0.00')
        if patch_footage:
            patch_quote = Decimal(patch_footage) * Decimal('2.50')

        return seal_quote + patch_quote

    @staticmethod
    def get_customer_job_history(customer_id: int) -> dict:
        return Job.objects.filter(
            property__customer_id=customer_id
        ).aggregate(
            total_jobs=Count('id'),
            total_value=Sum('total_quote'),
            completed_jobs=Count('id', filter=Q(status='completed'))
        ) 
