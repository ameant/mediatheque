from django.db import models
from membre.models import Emprunteur

class Media(models.Model):
    name = models.CharField(max_length=50)
    borrowing_date = models.DateField(null=True, blank=True)
    available = models.BooleanField(default=True)
    borrower = models.ForeignKey(Emprunteur, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True

    def disponible(self):
        return "Oui" if self.available else "Non"

    def emprunter(self, borrower):
        self.borrower = borrower
        self.available = False
        self.borrowing_date = timezone.now()
        self.save()

    def retourner(self):
        self.borrower = None
        self.available = True
        self.borrowing_date = None
        self.save()
class Livre(Media):
    author = models.CharField(max_length=50)

class Dvd(Media):
    director = models.CharField(max_length=50)

class Cd(Media):
    artist = models.CharField(max_length=50)

class JeuDePlateau(models.Model):
    name = models.CharField(max_length=50)
    creator = models.CharField(max_length=50)