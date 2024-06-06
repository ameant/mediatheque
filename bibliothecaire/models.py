from django.db import models
from membre.models import Emprunteur
from django.utils import timezone

class Media(models.Model):
    name = models.CharField(max_length=50)
    borrowing_date = models.DateField(null=True, blank=True)
    available = models.BooleanField(default=True)
    borrower = models.ForeignKey(Emprunteur, on_delete=models.SET_NULL, null=True, blank=True)

    def disponible(self):
        return "Oui" if self.available else "Non"

    def is_late(self):
        if self.borrowing_date:
            return (timezone.now().date() - self.borrowing_date).days > 7
        return False

    class Meta:
        abstract = True

class Livre(Media):
    author = models.CharField(max_length=50)

class Dvd(Media):
    director = models.CharField(max_length=50)

class Cd(Media):
    artist = models.CharField(max_length=50)

class JeuDePlateau(models.Model):
    name = models.CharField(max_length=50)
    creator = models.CharField(max_length=50)