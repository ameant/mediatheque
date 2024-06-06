from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Emprunteur
from bibliothecaire.models import Livre, Dvd, Cd, JeuDePlateau

def menu_membre(request):
    livres = Livre.objects.all()
    dvds = Dvd.objects.all()
    cds = Cd.objects.all()
    jps = JeuDePlateau.objects.all()
    return render(request, 'm_menu.html', {'livres': livres, 'dvds': dvds, 'cds': cds, 'jps': jps})

def m_connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('m_menu')
        else:
            messages.error(request,'Nom d\'utilisateur ou mot de passe incorrect.')
    return render (request, 'm_connection.html')

def liste_membres(request):
    emprunteurs = Emprunteur.objects.all()
    return render(request, 'member_list.html', {'emprunteurs': emprunteurs})