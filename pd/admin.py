from django import forms
from django.contrib import admin
from django_select2.forms import Select2MultipleWidget
from pd.models import *
from pd.costants import *
# Register your models here.

class PsicologoAdminForm(forms.ModelForm):
    specializzazione = forms.MultipleChoiceField(
        choices=SPECIALIZZAZIONI_PSICOLOGO,
        widget=Select2MultipleWidget,
        required=False,
    )

    giorno_disponibile = forms.MultipleChoiceField(
        choices=GIORNI_SETTIMANA,
        widget=Select2MultipleWidget,
        required=False,
    )

    orario_disponibile = forms.MultipleChoiceField(
        choices=ORARI_DISPONIBILI,
        widget=Select2MultipleWidget,
        required=False,
    )


    class Meta:
        model = Psicologo
        fields = '__all__'

    def clean_specializzazione(self):
        # converti lista in stringa separata da virgola per salvarla nel CharField
        return ",".join(self.cleaned_data['specializzazione'])

    def clean_giorno_disponibile(self):
        return ",".join(self.cleaned_data['giorno_disponibile'])

    def clean_orario_disponibile(self):
        return ",".join(self.cleaned_data['orario_disponibile'])



class PsicologoAdmin(admin.ModelAdmin):
    form = PsicologoAdminForm
    list_display = ('nome','cognome')
    search_fields = ('nome','cognome',)
    list_filter = ('nome','cognome',)


class PazienteAdminForm(forms.ModelForm):
    giorno_disponibile = forms.MultipleChoiceField(
        choices=GIORNI_SETTIMANA,
        widget=Select2MultipleWidget,
        required=False,
    )

    orario_disponibile = forms.MultipleChoiceField(
        choices=ORARI_DISPONIBILI,
        widget=Select2MultipleWidget,
        required=False,
    )

    class Meta:
        model = Paziente
        fields = '__all__'

    def clean_giorno_disponibile(self):
        return ",".join(self.cleaned_data['giorno_disponibile'])

    def clean_orario_disponibile(self):
        return ",".join(self.cleaned_data['orario_disponibile'])


class PazienteAdmin(admin.ModelAdmin):
    form = PazienteAdminForm
    list_display = ('nome','cognome')
    search_fields = ('nome','cognome')
    list_filter = ('nome','cognome')


class SedutaAdmin(admin.ModelAdmin):
    search_fields = ('data','paziente__nome', 'paziente__cognome', 'psicologo__nome', 'psicologo__cognome',)

admin.site.register(Psicologo, PsicologoAdmin)
admin.site.register(Paziente, PazienteAdmin)
admin.site.register(Seduta, SedutaAdmin)