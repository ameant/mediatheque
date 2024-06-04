from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from membre.models import Emprunteur
from .models import Livre, Dvd, Cd, JeuDePlateau
from .forms import BookForm, DvdForm, CdForm, BoardGameForm, BorrowingForm
def menu(request):
    return render(request, "menu.html")

def menu_bibliotheque(request):
    return render(request,"b_menu.html")

def b_connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('b_menu')
        else:
            messages.error(request,'Nom d\'utilisateur ou mot de passe incorrect.')
    return render (request, 'b_connection.html')

def m_creation(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            name = form.cleaned_data.get('name')
            emprunteur = Emprunteur.objects.create(name=name)
            emprunteur.save()
    else:
        form = CustomUserCreationForm()
    return render(request, 'm_subscription.html', {'form': form})

def liste_medias(request):
    livres = Livre.objects.all()
    dvds = Dvd.objects.all()
    cds = Cd.objects.all()
    jps = JeuDePlateau.objects.all()
    return render(request, 'media_list.html', {'livres': livres, 'dvds': dvds, 'cds': cds, 'jps': jps})

def ajout_livre(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_medias')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

def ajout_dvd(request):
    if request.method == 'POST':
        form = DvdForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_medias')
    else:
        form = DvdForm()
    return render(request, 'add_dvd.html', {'form': form})

def ajout_cd(request):
    if request.method == 'POST':
        form = CdForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_medias')
    else:
        form = CdForm()
    return render(request, 'add_cd.html', {'form': form})

def ajout_jp(request):
    if request.method == 'POST':
        form = BoardGameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_medias')
    else:
        form = BoardGameForm()
    return render(request, 'add_board_game.html', {'form': form})

def ajout_emprunt(request):
    if request.method == 'POST':
        form = BorrowingForm(request.POST)
        if form.is_valid():
            media_type = form.cleaned_data['media_type']
            media = form.cleaned_data['media']
            borrower = form.cleaned_data['borrower']

            if media_type == 'Livre':
                media = Livre.objects.get(pk=media.pk)
            elif media_type == 'Dvd':
                media = Dvd.objects.get(pk=media.pk)
            elif media_type == 'Cd':
                media = Cd.objects.get(pk=media.pk)
            elif media_type == 'JeuDePlateau':
                media = JeuDePlateau.objects.get(pk=media.pk)

            media.borrower = borrower
            media.available = False
            media.borrowing_date = timezone.now()
            media.save()

            return redirect('media_list')
    else:
        form = BorrowingForm()
    return render(request, 'add_borrowing.html', {'form': form})