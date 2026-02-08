from psicodigitale.settings import TYPEFORM_TOKEN
from core.models import *
from psicodigitale.settings import TYPEFORM_TOKEN
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

import json
import hmac
import hashlib


@csrf_exempt
def stripe_webhook(request):
    if request.method != "POST":
        return HttpResponseForbidden("POST only")

    # 1️⃣ raw body (UNA VOLTA)
    raw_payload = request.body
    if not raw_payload:
        return HttpResponseForbidden("Empty body")
    print(request.headers)
    # # 2️⃣ verifica firma sui BYTES
    # if not is_valid_signature(request.headers, raw_payload):
    #     return HttpResponseForbidden("Wrong signature")

    # 3️⃣ SOLO ORA parse JSON
    try:
        parsed_payload = json.loads(raw_payload.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponseForbidden("Invalid JSON")

    # 4️⃣ salva JSON
    StripeFormResponse.objects.create(payload=parsed_payload)


@csrf_exempt
def acuity_webhook(request):
    if request.method != "POST":
        return HttpResponseForbidden("POST only")

    # 1️⃣ raw body (UNA VOLTA)
    raw_payload = request.body
    if not raw_payload:
        return HttpResponseForbidden("Empty body")

    # # 2️⃣ verifica firma sui BYTES
    # if not is_valid_signature(request.headers, raw_payload):
    #     return HttpResponseForbidden("Wrong signature")

    # 3️⃣ SOLO ORA parse JSON
    try:
        parsed_payload = json.loads(raw_payload.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponseForbidden("Invalid JSON")

    # 4️⃣ salva JSON
    AcuityFormResponse.objects.create(payload=parsed_payload)


@csrf_exempt
def typeform_webhook(request):
    if request.method != "POST":
        return HttpResponseForbidden("POST only")

    # 1️⃣ raw body (UNA VOLTA)
    raw_payload = request.body
    if not raw_payload:
        return HttpResponseForbidden("Empty body")

    # # 2️⃣ verifica firma sui BYTES
    # if not is_valid_signature(request.headers, raw_payload):
    #     return HttpResponseForbidden("Wrong signature")

    # 3️⃣ SOLO ORA parse JSON
    try:
        parsed_payload = json.loads(raw_payload.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponseForbidden("Invalid JSON")

    # 4️⃣ salva JSON
    TypeFormResponse.objects.create(payload=parsed_payload, headers=dict(request.headers))

    return JsonResponse({"status": "ok"})


def is_valid_signature(headers, payload: bytes) -> bool:
    received = headers.get("Typeform-Signature")
    if not received:
        return False

    received = received.strip()

    secret = TYPEFORM_TOKEN.encode("utf-8")

    expected = "sha256=" + hmac.new(
        secret,
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(received, expected)