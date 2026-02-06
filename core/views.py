from psicodigitale.settings import TYPEFORM_TOKEN
from core.models import *
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import hmac
import hashlib


@csrf_exempt
def typeform_webhook(request):
    if request.method == "POST":
    if not verify_typeform_signature(request):
        return HttpResponseForbidden("Invalid signature")

    # ORA puoi fidarti del payload
    data = json.loads(request.body)

    # TODO:
    # - validare campi
    # - cifrare subito
    # - salvare solo ciò che serve

    return JsonResponse({"status": "ok"})


def verify_typeform_signature(request):
    received_signature = request.headers.get("Typeform-Signature")

    if not received_signature:
        return False

    # body RAW, non toccarlo
    payload = request.body

    expected_signature = "sha256=" + hmac.new(
        TYPEFORM_TOKEN.encode("utf-8"),
        payload,
        hashlib.sha256
    ).hexdigest()

    # confronto in constant time (importantissimo)
    return hmac.compare_digest(received_signature, expected_signature)