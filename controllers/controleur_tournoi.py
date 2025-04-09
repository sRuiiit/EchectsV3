from models.tournoi import Tournoi
from models.joueur import Joueur
from models.match import Match
from models.tour import Tour
from views.vue_tournoi import obtenir_donnees_tournoi, afficher_liste_tournois
from views.vue_joueur import afficher_liste_joueurs
import random
from collections import defaultdict
from views.vue_tournoi import afficher_recapitulatif_tournoi
from datetime import datetime

class ControleurTournoi:
    def __init__(self, db):
        self.db = db

    def afficher_recapitulatif(self, tournoi):
        afficher_recapitulatif_tournoi(tournoi)

    def creer_tournoi(self):
        nom, lieu, date_debut, date_fin, nb_tours, description = obtenir_donnees_tournoi()
        nb_tours = int(nb_tours) if nb_tours.isdigit() else 4

        joueurs_disponibles = self.db.get_all_players()
        if not joueurs_disponibles:
            print("⚠️ Aucun joueur disponible. Créez des joueurs d'abord.")
            return

        print("\nVoici les joueurs disponibles :")
        afficher_liste_joueurs(joueurs_disponibles)

        joueurs_selectionnes = []
        print("\nEntrez les numéros des joueurs à ajouter au tournoi (séparés par des virgules, ex: 1,3,5):")
        saisie = input("> ")
        try:
            indexes = [int(i.strip()) - 1 for i in saisie.split(",") if i.strip().isdigit()]
            for idx in indexes:
                if 0 <= idx < len(joueurs_disponibles):
                    joueurs_selectionnes.append(joueurs_disponibles[idx])
        except Exception as e:
            print(f"⚠️ Erreur lors de la sélection des joueurs : {e}")
            return

        if len(joueurs_selectionnes) < 2:
            print("⚠️ Il faut au moins 2 joueurs pour créer un tournoi.")
            return

        tournoi = Tournoi(
            nom=nom,
            lieu=lieu,
            date_debut=date_debut,
            date_fin=date_fin,
            joueurs=joueurs_selectionnes,
            tours=[],
            id_tournoi=None,
            nb_tours=nb_tours,
            tour_actuel=0,
            description=description
        )

        self.db.insert_tournament(tournoi)
        print(f"✅ Tournoi '{nom}' créé avec {len(joueurs_selectionnes)} joueurs.")
        return tournoi

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

    def demander_score(self, joueur):
        while True:
            print(f"\nRésultat pour {joueur.nom} :")
            print("  1 → Victoire")
            print("  0.5 → Égalité")
            print("  0 → Défaite")
            choix = input("Entrez le score (1 / 0.5 / 0) : ").strip()
            if choix in ["1", "0.5", "0"]:
                return float(choix)
            else:
                print("⛔ Entrée invalide. Veuillez entrer 1, 0.5 ou 0.")

    def gerer_round(self, tournoi):
        numero_tour = len(tournoi.tours) + 1

        if numero_tour > int(tournoi.nb_tours):
            print("✅ Tous les tours ont déjà été joués.")
            return

        nom_round = f"Round {numero_tour}"
        date_debut = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nouveau_tour = Tour(nom_round, date_debut)

        print(f"\n🎯 Création de {nom_round}...")

        scores = self.calcul_scores(tournoi)
        joueurs_tries = sorted(tournoi.joueurs, key=lambda j: scores.get(j.id_joueur, 0), reverse=True)
        matchs = []

        while len(joueurs_tries) >= 2:
            joueur1 = joueurs_tries.pop(0)
            joueur2 = joueurs_tries.pop(0)
            matchs.append(Match(joueur1, joueur2))

        nouveau_tour.liste_matchs = matchs

        print("\n📋 Matchs du round :")
        for match in matchs:
            print(f"{match.joueur1.nom} vs {match.joueur2.nom}")

        print("\n📝 Saisie des résultats :")
        for match in matchs:
            score1 = self.demander_score(match.joueur1)
            score2 = self.demander_score(match.joueur2)
            match.resultat = (score1, score2)

        nouveau_tour.date_heure_fin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tournoi.tours.append(nouveau_tour)
        self.db.update_tournament(tournoi)
        print(f"\n✅ {nom_round} terminé et enregistré.")

    def afficher_tournois(self):
        tournois = self.db.get_all_tournaments()
        if not tournois:
            print("Aucun tournoi trouvé.")
            return
        afficher_liste_tournois(tournois)

    def calcul_scores(self, tournoi):
        scores = defaultdict(float)
        for tour in tournoi.tours:
            for match in tour.liste_matchs:
                if match.resultat:
                    scores[match.joueur1.id_joueur] += match.resultat[0]
                    scores[match.joueur2.id_joueur] += match.resultat[1]
        return scores

    def afficher_joueurs_dun_tournoi(self):
        tournoi = self.selectionner_tournoi()
        if not tournoi:
            return

        if not tournoi.joueurs:
            print("Ce tournoi ne contient aucun joueur.")
            return

        print(f"\n👥 Joueurs du tournoi '{tournoi.nom}' :")
        for joueur in sorted(tournoi.joueurs, key=lambda j: j.nom):
            print(f"- {joueur.nom} {joueur.prenom} (ID: {joueur.id_joueur}, Classement: {joueur.classement})")