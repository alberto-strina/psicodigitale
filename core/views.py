from psicodigitale.settings import TYPEFORM_SECRET_KEY
from core.models import *
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

import json
import hmac
import hashlib
import base64


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
        return HttpResponseNotAllowed(["POST"])

    received_signature = request.headers.get("Typeform-Signature")

    if not received_signature:
        return HttpResponseForbidden("Permission denied")

    try:
        sha_name, signature = received_signature.split("=", 1)
    except ValueError:
        return HttpResponseForbidden("Invalid signature format")

    if sha_name != "sha256":
        return JsonResponse(
            {"detail": "Operation not supported"},
            status=501
        )

    raw_body = request.body

    if not verify_signature(signature, raw_body):
        return HttpResponseForbidden("Invalid signature")

    # payload JSON (se ti serve)
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        payload = None

    # TODO: logica webhook qui
    TypeFormResponse.objects.create(payload=payload, headers=request.headers)

    return JsonResponse({"status": "ok"})


def verify_signature(received_signature: str, payload: bytes) -> bool:
    secret = TYPEFORM_SECRET_KEY
    if not secret:
        raise RuntimeError("TYPEFORM_SECRET_KEY not set")

    digest = hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256
    ).digest()

    expected_signature = base64.b64encode(digest).decode()

    return hmac.compare_digest(expected_signature, received_signature)