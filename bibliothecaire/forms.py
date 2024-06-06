from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Livre, Dvd, Cd, JeuDePlateau, Emprunteur
from django import forms
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label= ("Nom d'utilisateur"),
        max_length=50,
        help_text=("50 caractères maximum. Lettres, chiffres et @/./+/-/_ uniquement."),
        error_messages={
            'invalid': (
                "Entrez un nom d'utilisateur valide."),
        },
    )

    name = forms.CharField(label="Nom", max_length=50)

    password1 = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    password2 = forms.CharField(
        label="Confirmation de mot de passe",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("username", "name", "password1", "password2")

class BookForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['name', 'author', 'available']
        labels = {
            'name': 'Nom',
            'author': 'Auteur / Autrice',
            'available': 'Disponible'
        }

class DvdForm(forms.ModelForm):
    class Meta:
        model = Dvd
        fields = ['name', 'director', 'available']
        labels = {
            'name': 'Nom',
            'director': 'Réalisateur / Réalisatrice',
            'available': 'Disponible'
        }

class CdForm(forms.ModelForm):
    class Meta:
        model = Cd
        fields = ['name', 'artist', 'available']
        labels = {
            'name': 'Nom',
            'artist': 'Artiste',
            'available': 'Disponible'
        }

class BoardGameForm(forms.ModelForm):
    class Meta:
        model = JeuDePlateau
        fields = ['name', 'creator']
        labels = {
            'name': 'Nom',
            'creator': 'Créateur / Créatrice',
        }

class BookBorrowForm(forms.ModelForm):
    borrower = forms.CharField(label="Emprunteur / Emprunteuse")
    borrowing_date = forms.DateField(
        label="Date d\'emprunt",
        help_text="Format: JJ/MM/AAAA"
    )

    class Meta:
        model = Livre
        fields = ['name', 'author', 'borrowing_date']
        labels = {
            'name': 'Nom',
            'author': 'Auteur / Autrice',
            'borrowing_date': 'Date d\'emprunt'
        }

    def clean(self):
        cleaned_data = super().clean()
        borrower_name = cleaned_data.get('borrower')

        try:
            emprunteur = Emprunteur.objects.get(name=borrower_name)
        except Emprunteur.DoesNotExist:
            raise ValidationError(f"Emprunteur {borrower_name} n'existe pas.")

        total_borrows = (
                emprunteur.livre_set.filter(available=False).count() +
                emprunteur.dvd_set.filter(available=False).count() +
                emprunteur.cd_set.filter(available=False).count()
        )

        if total_borrows >= 3:
            raise ValidationError(f"{borrower_name} ne peut pas avoir plus de 3 emprunts à la fois")

        self.instance.borrower = emprunteur

        return cleaned_data

class DvdBorrowForm(BookBorrowForm):
    borrower = forms.CharField(label="Emprunteur / Emprunteuse")
    borrowing_date = forms.DateField(
        label="Date d\'emprunt",
        help_text="Format: JJ/MM/AAAA"
    )

    class Meta:
        model = Dvd
        fields = ['name', 'director', 'borrowing_date']
        labels = {
            'name': 'Nom',
            'name': 'Nom',
            'director': 'Réalisateur / Réalisatrice',
            'borrowing_date': 'Date d\'emprunt'
        }

class CdBorrowForm(BookBorrowForm):
    borrower = forms.CharField(label="Emprunteur / Emprunteuse")
    borrowing_date = forms.DateField(
        label="Date d\'emprunt",
        help_text="Format: JJ/MM/AAAA"
    )

    class Meta:
        model = Cd
        fields = ['name', 'artist', 'borrowing_date']
        labels = {
            'name': 'Nom',
            'artist': 'Artiste',
            'borrowing_date': 'Date d\'emprunt'
        }

class BorrowerUpdateForm(forms.ModelForm):
    class Meta:
        model = Emprunteur
        fields = ['name', 'blocked']
        labels = {
            'name': 'Nom',
            'blocked': 'Bloquer le membre'
        }