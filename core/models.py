from pd.costants import *
from django.db import models

class Psicologo(models.Model):
    # Informazioni personali
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    # Informazioni professionali
    specializzazione = models.CharField(max_length=255, blank=True, null=True)
    partita_iva = models.CharField(max_length=20, blank=True, null=True)
    esperienza_anni = models.PositiveIntegerField(default=0)

    giorno_disponibile = models.CharField(max_length=255, blank=True, null=True)

    # Orario di disponibilità
    orario_disponibile = models.CharField(max_length=255, blank=True, null=True)

    # Foto profilo
    #foto = models.ImageField(upload_to='psicologi_foto/', blank=True, null=True)

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['cognome', 'nome']
        verbose_name = "Psicologo"
        verbose_name_plural = "Psicologi"

    def __str__(self):
        return f"{self.nome} {self.cognome}"


class Paziente(models.Model):
    # Stato di emergenza

    # Dati personali
    nome = models.CharField(max_length=50, verbose_name="Nome")
    cognome = models.CharField(max_length=50, verbose_name="Cognome")
    email = models.EmailField(verbose_name="Email")
    telefono = models.CharField(max_length=20, verbose_name="Numero di telefono")
    eta = models.PositiveIntegerField(verbose_name="Età")

    psicologo = models.ForeignKey(
        Psicologo,
        on_delete=models.SET_NULL,  # Se lo psicologo viene eliminato, il campo diventa null
        null=True,
        blank=True,
        related_name="paziente"
    )

    emergenza = models.BooleanField(default=False, verbose_name="Sei in pericolo?")

    # Informazioni sul compilatore
    rappresentante = models.CharField(
        max_length=100,
        verbose_name="Per chi stai compilando questo questionario?",
        blank=True
    )

    # Scelta dello psicologo
    preferenza_psicologo = models.CharField(
        max_length=100,
        choices=GENERE_PSICOLOGO,
        verbose_name="Da quale psicologo vorresti essere seguito?",
        blank=True
    )

    # Sintomi e motivazioni
    sintomi = models.TextField(verbose_name="Sintomi psicologici")
    ambito = models.CharField(
        max_length=100,
        verbose_name="Ambito del problema"
    )
    motivo = models.TextField(
        verbose_name="Motivo per iniziare un percorso psicologico"
    )

    # Disponibilità e interessi
    giorno_disponibile = models.CharField(max_length=255, blank=True, null=True)
    orario_disponibile = models.CharField(max_length=255, blank=True, null=True)
    terapia_gruppo = models.BooleanField(
        default=False,
        verbose_name="Interessato a un percorso di gruppo?"
    )

    # Tracciamento
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['cognome', 'nome']
        verbose_name = "Paziente"
        verbose_name_plural = "Pazienti"

    def __str__(self):
        return f"{self.nome} {self.cognome}"


class Seduta(models.Model):
    data = models.DateTimeField(verbose_name="Data seduta")
    psicologo = models.ForeignKey(
        Psicologo,
        on_delete=models.CASCADE,
        related_name='sedute'
    )
    paziente = models.ForeignKey(
        Paziente,
        on_delete=models.CASCADE,
        related_name='sedute'
    )
    tipo_seduta = models.CharField(
        max_length=100,
        verbose_name="Tipo seduta"
    )
    avvenuta = models.BooleanField(
        default=False,
        verbose_name="Seduta avvenuta"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creato il")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aggiornato il")

    class Meta:
        ordering = ['data']
        verbose_name = "Seduta"
        verbose_name_plural = "Sedute"

    def __str__(self):
        return f"{self.data.strftime('%d/%m/%Y %H:%M')} - {self.paziente.nome} {self.paziente.cognome} ({self.tipo_seduta})"


# ---------------------------- WEBHOOKS ---------------------------- #

class TypeFormResponse(models.Model):
    payload = models.JSONField(blank=False, null=False)
    headers = models.JSONField(blank=False, null=False)
    received_at = models.DateTimeField(auto_now_add=True)

class StripeFormResponse(models.Model):
    payload = models.JSONField(blank=False, null=False)
    headers = models.JSONField(blank=False, null=False)
    received_at = models.DateTimeField(auto_now_add=True)

class AcuityFormResponse(models.Model):
    payload = models.JSONField(blank=False, null=False)
    headers = models.JSONField(blank=False, null=False)
    received_at = models.DateTimeField(auto_now_add=True)