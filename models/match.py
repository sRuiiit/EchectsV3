# models/match.py

from models.joueur import Joueur

class Match:
    def __init__(self, joueur1, joueur2, resultat=None):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.resultat = resultat  # ex : (1.0, 0.0), ou (0.5, 0.5)

    def to_dict(self):
        return {
            "joueur1": self.joueur1.to_dict(),
            "joueur2": self.joueur2.to_dict(),
            "resultat": self.resultat,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            Joueur.from_dict(data["joueur1"]),
            Joueur.from_dict(data["joueur2"]),
            data["resultat"]
        )