# controllers/controleur_tournoi.py

from models.tournoi import Tournoi
from models.joueur import Joueur
from models.match import Match
from models.tour import Tour
from views.vue_tournoi import obtenir_donnees_tournoi, afficher_liste_tournois
from views.vue_joueur import afficher_liste_joueurs
import random
from collections import defaultdict

class ControleurTournoi:
    def __init__(self, db):
        self.db = db

    def creer_tournoi(self):
        nom, lieu, date_debut, date_fin, nb_tours, description = obtenir_donnees_tournoi()

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

    def afficher_tournois(self):
        tournois = self.db.get_all_tournaments()
        if not tournois:
            print("Aucun tournoi trouvé.")
            return
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

    def saisir_resultats_tour(self, tournoi):
        if tournoi.tour_actuel == 0 or tournoi.tour_actuel > len(tournoi.tours):
            print("Aucun tour en cours.")
            return

        tour = tournoi.tours[tournoi.tour_actuel - 1]
        print(f"\n📝 Résultats pour {tour.nom} :")
        for match in tour.liste_matchs:
            print(f"Match : {match.joueur1.nom} vs {match.joueur2.nom}")
            try:
                r1 = float(input(f"Score de {match.joueur1.nom} : "))
                r2 = float(input(f"Score de {match.joueur2.nom} : "))
                match.resultat = (r1, r2)
            except ValueError:
                print("Entrée invalide. Match non enregistré.")

        self.db.update_tournament(tournoi)
        print("✅ Résultats enregistrés.")

    def calcul_scores(self, tournoi):
        scores = defaultdict(float)
        for tour in tournoi.tours:
            for match in tour.liste_matchs:
                if match.resultat:
                    scores[match.joueur1.id_joueur] += match.resultat[0]
                    scores[match.joueur2.id_joueur] += match.resultat[1]
        return scores

    def historique_matchs(self, tournoi):
        rencontres = set()
        for tour in tournoi.tours:
            for match in tour.liste_matchs:
                id1 = match.joueur1.id_joueur
                id2 = match.joueur2.id_joueur
                if id1 > id2:
                    id1, id2 = id2, id1
                rencontres.add((id1, id2))
        return rencontres

    def demarrer_tour_suivant(self, tournoi):
        if tournoi.tour_actuel >= tournoi.nb_tours:
            print("✅ Tous les tours ont été joués.")
            return

        scores = self.calcul_scores(tournoi)
        joueurs = sorted(tournoi.joueurs, key=lambda j: (-scores.get(j.id_joueur, 0), j.nom))
        rencontres_existantes = self.historique_matchs(tournoi)

        appariements = []
        deja_paires = set()
        i = 0

        while i < len(joueurs) - 1:
            joueur1 = joueurs[i]
            for j in range(i + 1, len(joueurs)):
                joueur2 = joueurs[j]
                paire = tuple(sorted([joueur1.id_joueur, joueur2.id_joueur]))
                if paire not in rencontres_existantes and joueur2.id_joueur not in deja_paires:
                    appariements.append((joueur1, joueur2))
                    deja_paires.update([joueur1.id_joueur, joueur2.id_joueur])
                    break
            i += 1

        if len(joueurs) % 2 == 1:
            for joueur in joueurs:
                if joueur.id_joueur not in deja_paires:
                    appariements.append((joueur, Joueur("BYE", "", "", 0, -1)))
                    break

        tournoi.tour_actuel += 1
        matches = [Match(j1, j2) for j1, j2 in appariements]
        nouveau_tour = Tour(f"Round {tournoi.tour_actuel}", matches)
        tournoi.tours.append(nouveau_tour)
        self.db.update_tournament(tournoi)
        print(f"🌀 Round {tournoi.tour_actuel} généré avec {len(matches)} matchs.")

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
