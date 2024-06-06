from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from membre.models import Emprunteur
from .models import Livre, Dvd, Cd, JeuDePlateau
from .forms import BookForm, DvdForm, CdForm, BoardGameForm,  BookBorrowForm, DvdBorrowForm, CdBorrowForm, BorrowerUpdateForm
from django.db import transaction
from django.http import HttpResponse
from django.contrib.auth.models import User

def menu(request):
    return render(request, "menu.html")

def menu_bibliotheque(request):
    return render(request,"b_menu.html")

def b_connexion(request):
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('b_menu')
        else:
            messages.error(request,'Nom d\'utilisateur ou mot de passe incorrect.')
    return render (request, 'b_connection.html')

def m_creation(request):
    """
        View function for user creation.

        Parameters:
        - request: HttpRequest object

        Returns:
        - If request method is POST and form is valid, redirects to 'b_menu'.
        - If request method is GET, renders 'm_subscription.html' template with form.

        Example:
        >>> from django.test import RequestFactory
        >>> from .forms import CustomUserCreationForm
        >>> from .models import Emprunteur
        >>> factory = RequestFactory()
        >>> request = factory.post('/', {'username': 'testuser', 'password1': 'testpassword', 'password2': 'testpassword'})
        >>> response = m_creation(request)
        >>> response.status_code
        302
        >>> response.url
        '/b_menu/'
        >>> Emprunteur.objects.get(name='testuser')
        <Emprunteur: Emprunteur object (1)>
        """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            emprunteur = Emprunteur.objects.create(name=user.username)
            emprunteur.save()
            return redirect('b_menu')
    else:
        form = CustomUserCreationForm()
    return render(request, 'm_subscription.html', {'form': form})

def liste_medias(request):
    livres = Livre.objects.all()
    dvds = Dvd.objects.all()
    cds = Cd.objects.all()
    jps = JeuDePlateau.objects.all()

    for livre in livres:
        livre.is_late = livre.is_late()
    for dvd in dvds:
        dvd.is_late = dvd.is_late()
    for cd in cds:
        cd.is_late = cd.is_late()

    return render(request, 'media_list.html', {'livres': livres, 'dvds': dvds, 'cds': cds, 'jps': jps})

def ajout_livre(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_medias')
    else:
        form = BookForm()
    return render(request, 'add_media.html', {'form': form})

def ajout_dvd(request):
    if request.method == 'POST':
        form = DvdForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_medias')
    else:
        form = DvdForm()
    return render(request, 'add_media.html', {'form': form})

def ajout_cd(request):
    if request.method == 'POST':
        form = CdForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_medias')
    else:
        form = CdForm()
    return render(request, 'add_media.html', {'form': form})

def ajout_jp(request):
    if request.method == 'POST':
        form = BoardGameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_medias')
    else:
        form = BoardGameForm()
    return render(request, 'add_media.html', {'form': form})

def emprunt_livre(request, livre_name):
    livre = Livre.objects.get(name=livre_name)
    if request.method == 'POST':
        form = BookBorrowForm(request.POST, instance=livre)
        if form.is_valid():
            with transaction.atomic():
                borrower_name = form.cleaned_data['borrower']
                borrower, created = Emprunteur.objects.get_or_create(name=borrower_name)

                if borrower.blocked:
                    return HttpResponse("Emprunteur / Emprunteuse bloqué.e")

                livre.borrower = borrower
                livre.available = False
                form.save()
            return redirect('liste_medias')
    else:
        form = BookBorrowForm(instance=livre)
    return render(request, 'borrow_media.html', {'form': form})

def emprunt_dvd(request, dvd_name):
    dvd = Dvd.objects.get(name=dvd_name)
    if request.method == 'POST':
        form = DvdBorrowForm(request.POST, instance=dvd)
        if form.is_valid():
            with transaction.atomic():
                borrower = form.cleaned_data['borrower']
                borrower, created = Emprunteur.objects.get_or_create(name=borrower)
                dvd.borrower = borrower
                dvd.available = False
                form.save()
            return redirect('liste_medias')
    else:
        form = DvdBorrowForm(instance=dvd)
    return render(request, 'borrow_media.html', {'form': form})

def emprunt_cd(request, cd_name):
    cd = Cd.objects.get(name=cd_name)
    if request.method == 'POST':
        form = CdBorrowForm(request.POST, instance=cd)
        if form.is_valid():
            with transaction.atomic():
                borrower = form.cleaned_data['borrower']
                borrower, created = Emprunteur.objects.get_or_create(name=borrower)
                cd.borrower = borrower
                cd.available = False
                form.save()
            return redirect('liste_medias')
    else:
        form = CdBorrowForm(instance=cd)
    return render(request, 'borrow_media.html', {'form': form})

def modif_membre(request, emprunteur_name):
    emprunteur = Emprunteur.objects.get(name=emprunteur_name)
    if request.method == 'POST':
        form = BorrowerUpdateForm(request.POST, instance=emprunteur)
        if form.is_valid():
            form.save()
            return redirect('liste_membres')
    else:
        form = BorrowerUpdateForm(instance=emprunteur)
    return render(request, 'member_update.html', {'form': form})

def supp_membre(request, emprunteur_name):
    emprunteur = Emprunteur.objects.get(name=emprunteur_name)

    if request.method == 'POST':
        emprunteur.delete()
        try:
            user = User.objects.get(username=emprunteur_name)
            user.delete()
        except User.DoesNotExist:
            pass
        return redirect('liste_membres')