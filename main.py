# main.py

from models.database import DatabaseManager
from controllers.controleur_joueur import ControleurJoueur
from controllers.controleur_tournoi import ControleurTournoi
from controllers.controleur_menu import ControleurMenu

if __name__ == "__main__":
    print("\n=== Bienvenue dans le Gestionnaire de Tournois d'Échecs ===")

    # Initialiser la base de données et les contrôleurs
    db = DatabaseManager()
    controleur_joueur = ControleurJoueur(db)
    controleur_tournoi = ControleurTournoi(db)

    # Lancer le menu principal
    menu = ControleurMenu(controleur_joueur, controleur_tournoi)  # Pass the two controllers here
    menu.afficher_menu_principal()