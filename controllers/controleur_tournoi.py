from models.tournoi import Tournoi
from views.vue_tournoi import obtenir_donnees_tournoi, afficher_liste_tournois

class ControleurTournoi:
    def __init__(self, db):
        self.db = db

    def creer_tournoi(self):
        nom, lieu, date_debut, date_fin = obtenir_donnees_tournoi()
        if date_debut >= date_fin:
            print("Erreur : la date de début doit être antérieure à la date de fin.")
            return
        joueurs = []
        tours = []
        tournoi = Tournoi(nom, lieu, date_debut, date_fin, joueurs, tours, None)
        self.db.insert_tournament(tournoi)
        print("Tournoi créé avec succès.")

    def afficher_tournois(self):
        tournois = self.db.get_all_tournaments()
        afficher_liste_tournois(tournois)

    def selectionner_tournoi(self):
        tournois = self.db.get_all_tournaments()
        if not tournois:
            print("Aucun tournoi disponible.")
            return None

        print("\nTournois disponibles :")
        for i, tournoi in enumerate(tournois):
            print(f"[{i+1}] {tournoi.nom} ({tournoi.date_debut} → {tournoi.date_fin})")

        while True:
            try:
                choix = int(input("Sélectionnez un tournoi par son numéro : "))
                if 1 <= choix <= len(tournois):
                    return tournois[choix - 1]
                else:
                    print("Numéro invalide. Réessayez.")
            except ValueError:
                print("Entrée non valide. Entrez un nombre.")

    def demarrer_premier_tour(self, tournoi):
        if not tournoi.joueurs or len(tournoi.joueurs) < 2:
            print("Pas assez de joueurs pour démarrer le tournoi.")
            return

        from models.match import Match
        from models.tour import Tour

        import random
        random.shuffle(tournoi.joueurs)
        liste_matchs = []

        for i in range(0, len(tournoi.joueurs) - 1, 2):
            joueur1 = tournoi.joueurs[i]
            joueur2 = tournoi.joueurs[i + 1]
            match = Match(joueur1, joueur2)
            liste_matchs.append(match)

        if len(tournoi.joueurs) % 2 == 1:
            joueur_sans_match = tournoi.joueurs[-1]
            match = Match(joueur_sans_match, Joueur("BYE", "", "", 0, -1), (1.0, 0.0))
            liste_matchs.append(match)

        nom_tour = "Round 1"
        tour = Tour(nom_tour, liste_matchs)
        tournoi.tours.append(tour)
        tournoi.tour_actuel = 1
        self.db.update_tournament(tournoi)

        print(f"✅ {nom_tour} démarré avec {len(liste_matchs)} matchs.")
