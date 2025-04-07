# controllers/controleur_application.py

from controllers.controleur_menu import ControleurMenu
from controllers.controleur_joueur import ControleurJoueur
from controllers.controleur_tournoi import ControleurTournoi
from models.database import DatabaseManager

class ControleurApplication:
    def __init__(self):
        self.db = DatabaseManager()
        self.menu = ControleurMenu()
        self.controleur_joueur = ControleurJoueur(self.db)
        self.controleur_tournoi = ControleurTournoi(self.db)

    def run(self):
        while True:
            choix = self.menu.afficher_menu_principal()
            if choix == "1":
                self.menu_joueur()
            elif choix == "2":
                self.menu_tournoi()
            elif choix == "3":
                print("Fermeture de l'application.")
                break

    def menu_joueur(self):
        while True:
            choix = self.menu.afficher_menu_joueurs()
            if choix == "1":
                self.controleur_joueur.creer_joueur()
            elif choix == "2":
                self.controleur_joueur.afficher_joueurs()
            elif choix == "3":
                break

    def menu_tournoi(self):
        while True:
            choix = self.menu.afficher_menu_tournois()
            if choix == "1":
                self.controleur_tournoi.creer_tournoi()
            elif choix == "2":
                self.controleur_tournoi.afficher_tournois()
            elif choix == "3":
                break
