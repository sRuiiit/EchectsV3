# controllers/controleur_menu.py

class ControleurMenu:
    def __init__(self, controleur_joueur, controleur_tournoi):
        self.controleur_joueur = controleur_joueur
        self.controleur_tournoi = controleur_tournoi

    def afficher_menu_principal(self):
        while True:
            print("\n=== MENU PRINCIPAL ===")
            print("1. Gérer les joueurs")
            print("2. Gérer les tournois")
            print("3. Voir le récapitulatif du tournoi")
            print("4. Quitter")

            choix = input("Votre choix : ")

            if choix == "1":
                self.menu_joueurs()
            elif choix == "2":
                self.menu_tournois()
            elif choix == "3":
                tournoi = self.controleur_tournoi.selectionner_tournoi()
                if tournoi:
                    self.controleur_tournoi.afficher_recapitulatif(tournoi)
            elif choix == "4":
                print("À bientôt !")
                break
            else:
                print("Choix invalide. Réessayez.")

    def menu_joueurs(self):
        while True:
            print("\n--- GESTION DES JOUEURS ---")
            print("1. Ajouter un joueur")
            print("2. Afficher les joueurs")
            print("3. Retour")

            choix = input("Votre choix : ")

            if choix == "1":
                self.controleur_joueur.creer_joueur()
            elif choix == "2":
                self.controleur_joueur.afficher_joueurs()
            elif choix == "3":
                break
            else:
                print("Choix invalide.")

    def menu_tournois(self):
        while True:
            print("\n--- GESTION DES TOURNOIS ---")
            print("1. Créer un tournoi")
            print("2. Afficher les tournois")
            print("3. Démarrer le premier tour")
            print("4. Générer le tour suivant")
            print("5. Voir les joueurs d’un tournoi")
            print("6. Retour")

            choix = input("Votre choix : ")

            if choix == "1":
                self.controleur_tournoi.creer_tournoi()
            elif choix == "2":
                self.controleur_tournoi.afficher_tournois()
            elif choix == "3":
                tournoi = self.controleur_tournoi.selectionner_tournoi()
                if tournoi:
                    self.controleur_tournoi.demarrer_premier_tour(tournoi)
            elif choix == "4":
                tournoi = self.controleur_tournoi.selectionner_tournoi()
                if tournoi:
                    self.controleur_tournoi.demarrer_tour_suivant(tournoi)
                    # Saisie des résultats après chaque tour
                    self.controleur_tournoi.saisir_resultats_tour(tournoi)
            elif choix == "5":
                self.controleur_tournoi.afficher_joueurs_dun_tournoi()
            elif choix == "6":
                break
            else:
                print("Choix invalide.")