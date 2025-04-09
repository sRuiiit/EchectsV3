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
        joueurs_disponibles = self.db.get_all_players()
        if not joueurs_disponibles:
            print("⛔ Vous devez d'abord enregistrer des joueurs avant de créer un tournoi.")
            return None

        nom, lieu, date_debut, date_fin, nb_tours, description = obtenir_donnees_tournoi()
        nb_tours = int(nb_tours) if nb_tours.isdigit() else 4

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
            return None

        if len(joueurs_selectionnes) < 2:
            print("⚠️ Il faut au moins 2 joueurs pour créer un tournoi.")
            return None

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

    def afficher_plan_tournoi(self, tournoi):
        print(f"\n📅 Plan du tournoi : {tournoi.nom}")
        print("-------------------------------------------")
        if not tournoi.tours:
            print("Aucun round encore généré pour ce tournoi.")
            return

        for i, tour in enumerate(tournoi.tours, 1):
            print(f"Round {i} :")
            for match in tour.liste_matchs:
                if match.joueur2.nom == "BYE":
                    print(f" - {match.joueur1.nom} (joue seul - BYE)")
                else:
                    if match.resultat:
                        print(f" - {match.joueur1.nom} vs {match.joueur2.nom} [{match.resultat[0]} - {match.resultat[1]}]")
                    else:
                        print(f" - {match.joueur1.nom} vs {match.joueur2.nom} (à jouer)")
            print()

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

    def afficher_plan_tournoi(self, tournoi):
        print(f"\n📅 Plan du tournoi : {tournoi.nom}")
        print("-------------------------------------------")
        for i, tour in enumerate(tournoi.tours, 1):
            print(f"Round {i} :")
            for match in tour.liste_matchs:
                if match.joueur2.nom == "BYE":
                    print(f" - {match.joueur1.nom} (joue seul - BYE)")
                else:
                    resultat = ""
                    if match.resultat:
                        resultat = f" [{match.resultat[0]} - {match.resultat[1]}]"
                    print(f" - {match.joueur1.nom} vs {match.joueur2.nom}{resultat}")
            print()
        if not tournoi.tours:
            print("Aucun round encore généré pour ce tournoi.")

    def demander_resultat_match(self, joueur1, joueur2):
        while True:
            print(f"\nMatch : {joueur1.nom} vs {joueur2.nom}")
            print("Qui a gagné ?")
            print(f"1. {joueur1.nom}")
            print(f"2. {joueur2.nom}")
            print("3. Match nul")
            choix = input("> ").strip()
            if choix == "1":
                return (1.0, 0.0)
            elif choix == "2":
                return (0.0, 1.0)
            elif choix == "3":
                return (0.5, 0.5)
            else:
                print("⛔ Choix invalide. Veuillez taper 1, 2 ou 3.")

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
        joueurs = sorted(tournoi.joueurs, key=lambda j: scores.get(j.id_joueur, 0), reverse=True)
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

        joueurs_paires = set(j.id_joueur for p in appariements for j in p)
        joueur_solo = next((j for j in joueurs if j.id_joueur not in joueurs_paires), None)
        matchs = [Match(j1, j2) for j1, j2 in appariements]

        if joueur_solo:
            joueur_bye = Joueur("BYE", "", "", 0, -1)
            match_bye = Match(joueur_solo, joueur_bye)
            match_bye.resultat = (1.0, 0.0)
            matchs.append(match_bye)

        nouveau_tour.liste_matchs = matchs

        print("\n📋 Matchs du round à venir :")
        print("---------------------------------------")
        for i, match in enumerate(matchs, 1):
            if match.joueur2.nom == "BYE":
                print(f"{i}. {match.joueur1.nom} (joue seul - BYE)")
            else:
                print(f"{i}. {match.joueur1.nom} vs {match.joueur2.nom}")
        print("---------------------------------------")

        print("\n📝 Saisie des résultats :")
        for match in matchs:
            if match.joueur2.nom != "BYE":
                match.resultat = self.demander_resultat_match(match.joueur1, match.joueur2)

        nouveau_tour.date_heure_fin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tournoi.tours.append(nouveau_tour)
        self.db.update_tournament(tournoi)
        print(f"\n✅ {nom_round} terminé.")
        print("💾 Sauvegarde automatique du tournoi effectuée.")

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