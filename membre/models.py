from django.db import models

class Emprunteur(models.Model):
    name = models.CharField(max_length=50)
    blocked = models.BooleanField(default=False)

    def bloque(self):
        return "Oui" if self.blocked else "Non"