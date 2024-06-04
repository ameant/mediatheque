from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Media, Livre, Dvd, Cd, JeuDePlateau, Emprunteur
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
class BorrowingForm(forms.Form):
    media_type = forms.ChoiceField(choices=[('Livre', 'Livre'), ('Dvd', 'Dvd'), ('Cd', 'Cd'), ('JeuDePlateau', 'Jeu de Plateau')])
    media = forms.ModelChoiceField(queryset=Livre.objects.filter(available=True), required=False)
    borrower = forms.ModelChoiceField(queryset=Emprunteur.objects.all())

    def clean(self):
        cleaned_data = super().clean()
        media_type = cleaned_data.get('media_type')
        if media_type == 'Livre':
            self.fields['media'].queryset = Livre.objects.filter(available=True)
        elif media_type == 'Dvd':
            self.fields['media'].queryset = Dvd.objects.filter(available=True)
        elif media_type == 'Cd':
            self.fields['media'].queryset = Cd.objects.filter(available=True)
        elif media_type == 'JeuDePlateau':
            self.fields['media'].queryset = JeuDePlateau.objects.filter(available=True)
        return cleaned_data