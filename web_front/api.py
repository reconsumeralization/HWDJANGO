from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.serializers import serialize
import json

@require_http_methods(["GET"])
def get_leads_api(request):
    leads = Lead.objects.active_leads()
    data = serialize('json', leads)
    return JsonResponse(json.loads(data), safe=False)

@require_http_methods(["POST"])
def create_lead_api(request):
    try:
        data = json.loads(request.body)
        lead = Lead.objects.create(**data)
        return JsonResponse({
            'status': 'success',
            'id': lead.id,
            'message': 'Lead created successfully'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
