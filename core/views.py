import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # necessario
def typeform_webhook(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    payload = json.loads(request.body)

    # DEBUG: guarda cosa arriva
    print(json.dumps(payload, indent=2))

    answers = payload["form_response"]["answers"]

    for answer in answers:
        field_id = answer["field"]["id"]
        value = answer.get("text") or answer.get("email") or answer.get("number")
        print(field_id, value)

    return JsonResponse({"status": "ok"})