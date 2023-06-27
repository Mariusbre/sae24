from . import models
from .forms import CapteursForm
from django.shortcuts import render, HttpResponseRedirect
from datetime import datetime
import matplotlib.pyplot as plt


def accueil(request):
    return render(request, 'appsae24/accueil.html')


def liste_donnees(request):
    capteur_id = request.GET.get('capteur_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    data = models.donnees.objects.all()
    if capteur_id:
        data = data.filter(capteur__IDs=capteur_id)

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%d/%m/%Y').date()
        end_date = datetime.strptime(end_date, '%d/%m/%Y').date()
        data = data.filter(timestamp__range=(start_date, end_date))
    date = [d.timestamp for d in data]
    degre = [d.degre for d in data]

    plt.plot(date, degre)
    plt.xlabel('Date')
    plt.ylabel('Degrés')
    plt.title('Graphique des degrés')
    plt.grid(True)

    plt.show()

    context = {'data': data, 'degre': degre}
    return render(request, 'appsae24/liste_donnees.html', context)


def liste_capteurs(request):
    liste_c = list(models.capteurs.objects.all())
    return render(request, 'appsae24/liste_capteurs.html', {"liste_c": liste_c})


def update(request, IDs):
    capteurs = models.capteurs.objects.get(IDs=IDs)
    form = CapteursForm(capteurs.dico())
    return render(request, "appsae24/update_capteurs.html", {"form": form, "IDs": IDs})


def update_traitement(request, IDs):
    capteurs = models.capteurs.objects.get(IDs=IDs)
    form = CapteursForm(request.POST, instance=capteurs)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/appsae24/liste_capteurs/")
    else:
        return render(request, 'appsae24/update_capteurs.html', {"form": form, "IDs": IDs})


def update_capteurs(request, IDs):
    capteurs = models.capteurs.objects.get(IDs=IDs)
    form = CapteursForm(instance=capteurs)
    return render(request, "appsae24/update_capteurs.html", {"form": form, "IDs": IDs})