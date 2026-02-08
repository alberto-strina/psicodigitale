from django.urls import path
from .views import typeform_webhook,acuity_webhook,stripe_webhook

urlpatterns = [
    path("webhook/typeform/", typeform_webhook, name="typeform_webhook"),
    path("webhook/stripe/", stripe_webhook, name="stripe_webhook"),
    path("webhook/acuity/", acuity_webhook, name="acuity_webhook"),
]
