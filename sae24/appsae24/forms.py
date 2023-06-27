from django import forms
from django.forms import ModelForm
from . import models


class CapteursForm(ModelForm):
    class Meta:
        model = models.capteurs
        fields = ('nom_capteur', 'piece')
        labels = {
            'nom_capteur': 'nom_capteur',
            'piece': 'piece',
        }


class DonneesForm(ModelForm):
    class Meta:
        model = models.donnees
        fields = ('capteur', 'timestamp', 'degre')
        labels = {
            'capteur': 'capteur',
            'timestamp': 'timestamp',
            'degre': 'degre',
        }