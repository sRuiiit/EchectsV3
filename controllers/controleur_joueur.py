# controllers/controleur_joueur.py

from models.joueur import Joueur
from views.vue_joueur import afficher_joueur, afficher_liste_joueurs, obtenir_donnees_joueur

class ControleurJoueur:
    def __init__(self, db):
        self.db = db

    def creer_joueur(self):
        nom, prenom, identifiant, classement, date_naissance = obtenir_donnees_joueur()
        joueur = Joueur(nom, prenom, identifiant, classement, id_joueur=None, date_naissance=date_naissance)
        self.db.insert_player(joueur)
        print("✅ Joueur ajouté avec succès.")

    def afficher_joueurs(self):
        joueurs = self.db.get_all_players()
        afficher_liste_joueurs(joueurs)

