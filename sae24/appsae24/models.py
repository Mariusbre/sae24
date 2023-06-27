from django.db import models


class capteurs(models.Model):
    IDs = models.CharField(max_length=255, primary_key=True)
    nom_capteur = models.CharField(max_length=255, unique=True)
    piece = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'capteurs'

    def __str__(self):
        return f"IDs: {self.IDs}, Capteur: {self.nom_capteur}, Pièce: {self.piece}"

    def dico(self):
        return {"nom_capteur": self.nom_capteur, "piece": self.piece}


class donnees(models.Model):
    capteur = models.ForeignKey(capteurs, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    degre = models.FloatField()

    class Meta:
        managed = False
        db_table = 'donnees'

    def __str__(self):
        return f"capteur: {self.capteur}, timestamp: {self.timestamp}, degre: {self.degre}"

    def dico(self):
        return {"capteur": self.capteur, "timestamp": self.timestamp, "degre": self.degre}
