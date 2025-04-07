# models/tournoi.py

from models.joueur import Joueur
from models.tour import Tour

class Tournoi:
    def __init__(self, nom, lieu, date_debut, date_fin, joueurs, tours, id_tournoi, nb_tours=4, tour_actuel=0, description=""):
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.joueurs = joueurs  # liste de Joueur
        self.tours = tours      # liste de Tour
        self.id_tournoi = id_tournoi
        self.nb_tours = nb_tours
        self.tour_actuel = tour_actuel
        self.description = description

    def to_dict(self):
        return {
            "nom": self.nom,
            "lieu": self.lieu,
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "joueurs": [joueur.to_dict() for joueur in self.joueurs],
            "tours": [tour.to_dict() for tour in self.tours],
            "id_tournoi": self.id_tournoi,
            "nb_tours": self.nb_tours,
            "tour_actuel": self.tour_actuel,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nom=data["nom"],
            lieu=data["lieu"],
            date_debut=data["date_debut"],
            date_fin=data["date_fin"],
            joueurs=[Joueur.from_dict(j) for j in data.get("joueurs", [])],
            tours=[Tour.from_dict(t) for t in data.get("tours", [])],
            id_tournoi=data["id_tournoi"],
            nb_tours=data.get("nb_tours", 4),
            tour_actuel=data.get("tour_actuel", 0),
            description=data.get("description", "")
        )

    def __str__(self):
        return f"{self.nom} ({self.lieu}) - du {self.date_debut} au {self.date_fin}"