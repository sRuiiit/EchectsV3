# models/tour.py

from models.match import Match
from datetime import datetime

class Tour:
    def __init__(self, nom, liste_matchs, date_debut=None, date_fin=None):
        self.nom = nom
        self.liste_matchs = liste_matchs
        self.date_debut = date_debut or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date_fin = date_fin

    def terminer(self):
        self.date_fin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "nom": self.nom,
            "liste_matchs": [m.to_dict() for m in self.liste_matchs],
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["nom"],
            [Match.from_dict(m) for m in data["liste_matchs"]],
            data.get("date_debut"),
            data.get("date_fin"),
        )