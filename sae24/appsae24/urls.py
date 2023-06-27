from django.urls import path
from . import views

urlpatterns = [
    path('accueil/', views.accueil),
    path('liste_donnees/', views.liste_donnees),
    path('liste_capteurs/', views.liste_capteurs),
    path('update/<str:IDs>/', views.update),
    path('update_traitement/<str:IDs>/', views.update_traitement),
    path('update_capteurs/<str:IDs>/', views.update_capteurs),
]