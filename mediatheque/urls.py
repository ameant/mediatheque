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
    path('modification-membre/<str:emprunteur_name>/', bibliothecaire_views.modif_membre, name='member_update'),
    path('suppression-membre/<str:emprunteur_name>/', bibliothecaire_views.supp_membre, name='member_supp'),
    path('liste-medias/', bibliothecaire_views.liste_medias, name='liste_medias'),
    path('ajout-media/', bibliothecaire_views.ajout_livre, name='ajout_livre'),
    path('ajout-dvd/', bibliothecaire_views.ajout_dvd, name='ajout_dvd'),
    path('ajout-cd/', bibliothecaire_views.ajout_cd, name='ajout_cd'),
    path('ajout-jp/', bibliothecaire_views.ajout_jp, name='ajout_jp'),
    path('emprunt-livre/<str:livre_name>/', bibliothecaire_views.emprunt_livre, name='emprunt_livre'),
    path('emprunt-dvd/<str:dvd_name>/', bibliothecaire_views.emprunt_dvd, name='emprunt_dvd'),
    path('emprunt-cd/<str:cd_name>/', bibliothecaire_views.emprunt_cd, name='emprunt_cd'),
    path('admin/', admin.site.urls),
]