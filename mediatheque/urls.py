from django.contrib import admin
from django.urls import path
from bibliothecaire import views as bibliothecaire_views
from membre import views as membre_views

urlpatterns = [
    path('', bibliothecaire_views.menu, name='menu'),
    path('connexion-bibliothecaires/', bibliothecaire_views.b_connexion, name='b_connection'),
    path('inscription-membres/', bibliothecaire_views.m_creation, name='m_subscription'),
    path('connexion-membres/', membre_views.m_connexion, name='m_connection'),
    path('menu-bibliothecaires/', bibliothecaire_views.menu_bibliotheque, name='b_menu'),
    path('menu-membres/', membre_views.menu_membre, name='m_menu'),
    path('liste-membres/', membre_views.liste_membres, name='liste_membres'),
    path('modification-membre/<str:emprunteur_name>/', membre_views.modif_membre, name='member_update'),
    path('liste-medias/', bibliothecaire_views.liste_medias, name='liste_medias'),
    path('ajout-livre/', bibliothecaire_views.ajout_livre, name='ajout_livre'),
    path('ajout-dvd/', bibliothecaire_views.ajout_dvd, name='ajout_dvd'),
    path('ajout-cd/', bibliothecaire_views.ajout_cd, name='ajout_cd'),
    path('ajout-jp/', bibliothecaire_views.ajout_jp, name='ajout_jp'),
    path('ajout-emprunt/', bibliothecaire_views.ajout_emprunt, name='ajout_emprunt'),
    path('admin/', admin.site.urls),
]
