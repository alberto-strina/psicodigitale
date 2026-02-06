from psicodigitale.settings import TYPEFORM_TOKEN
from core.models import *
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

import json
import hmac
import hashlib

@csrf_exempt
def typeform_webhook(request):
    if request.method != "POST":
        return HttpResponseForbidden("Invalid method! Use POST method.")

    payload = request.body  # UNA SOLA LETTURA

    if not verify_typeform_signature(request.headers, payload):
        return HttpResponseForbidden("Invalid signature")

    data = json.loads(payload)

    TypeFormResponse.objects.create(payload=data)

    return JsonResponse({"status": "ok"})


def verify_typeform_signature(headers, payload):
    received_signature = headers.get("Typeform-Signature")
    if not received_signature:
        return False

    expected_signature = "sha256=" + hmac.new(
        TYPEFORM_TOKEN.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(received_signature, expected_signature)