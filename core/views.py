import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # necessario
def typeform_webhook(request):
    payload = json.loads(request.body)

    # DEBUG: guarda cosa arriva
    print(payload)
    return HttpResponse("OK")

