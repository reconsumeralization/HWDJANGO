from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def status_color(status):
    """Return Bootstrap color class based on lead status"""
    colors = {
        'new': 'primary',
        'contacted': 'info',
        'qualified': 'success',
        'converted': 'warning',
        'unqualified': 'danger'
    }
    return colors.get(status, 'secondary')

@register.simple_tag
def lead_age(created_at):
    """Return human-readable time since lead creation"""
    delta = timezone.now() - created_at
    if delta.days == 0:
        hours = delta.seconds // 3600
        if hours == 0:
            minutes = delta.seconds // 60
            return f"{minutes} minutes ago"
        return f"{hours} hours ago"
    return f"{delta.days} days ago"
