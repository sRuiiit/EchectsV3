# models/tournoi.py

from models.joueur import Joueur
from models.tour import Tour

class Tournoi:
    def __init__(self, nom, lieu, date_debut, date_fin, description, nb_tours=4, tour_actuel=1, joueurs=None, tours=None, id_tournoi=None):
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.description = description
        self.nb_tours = nb_tours
        self.tour_actuel = tour_actuel
        self.joueurs = joueurs if joueurs else []
        self.tours = tours if tours else []
        self.id_tournoi = id_tournoi

    def to_dict(self):
        return {
            "nom": self.nom,
            "lieu": self.lieu,
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "description": self.description,
            "nb_tours": self.nb_tours,
            "tour_actuel": self.tour_actuel,
            "joueurs": [j.to_dict() for j in self.joueurs],
            "tours": [t.to_dict() for t in self.tours],
            "id_tournoi": self.id_tournoi,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["nom"],
            data["lieu"],
            data["date_debut"],
            data["date_fin"],
            data.get("description", ""),
            data.get("nb_tours", 4),
            data.get("tour_actuel", 1),
            [Joueur.from_dict(j) for j in data["joueurs"]],
            [Tour.from_dict(t) for t in data["tours"]],
            data["id_tournoi"]
        )

    def __str__(self):
        return f"{self.nom} - {self.lieu} ({self.date_debut} → {self.date_fin}) - {self.description}"


# views/vue_tournoi.py

def afficher_tournoi(tournoi):
    print(tournoi)

def afficher_liste_tournois(tournois):
    print("\nListe des tournois :")
    for tournoi in tournois:
        print("-", tournoi)

def obtenir_donnees_tournoi():
    print("\nCréation d'un nouveau tournoi :")
    nom = input("Nom du tournoi : ")
    lieu = input("Lieu du tournoi : ")
    date_debut = input("Date de début (YYYY-MM-DD) : ")
    date_fin = input("Date de fin (YYYY-MM-DD) : ")
    description = input("Description : ")
    nb_tours = input("Nombre de tours (4 par défaut) : ")
    nb_tours = int(nb_tours) if nb_tours else 4
    return nom, lieu, date_debut, date_fin, description, nb_tours


# controllers/controleur_tournoi.py

from models.tournoi import Tournoi
from views.vue_tournoi import obtenir_donnees_tournoi, afficher_liste_tournois

class ControleurTournoi:
    def __init__(self, db):
        self.db = db

    def creer_tournoi(self):
        nom, lieu, date_debut, date_fin, description, nb_tours = obtenir_donnees_tournoi()
        if date_debut >= date_fin:
            print("Erreur : la date de début doit être antérieure à la date de fin.")
            return
        tournoi = Tournoi(
            nom=nom,
            lieu=lieu,
            date_debut=date_debut,
            date_fin=date_fin,
            description=description,
            nb_tours=nb_tours,
        )
        self.db.insert_tournament(tournoi)
        print("Tournoi créé avec succès.")

    def afficher_tournois(self):
        tournois = self.db.get_all_tournaments()
        afficher_liste_tournois(tournois)
