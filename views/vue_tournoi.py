# views/vue_tournoi.py

def obtenir_donnees_tournoi():
    """Fonction pour obtenir les informations du tournoi de l'utilisateur"""
    print("\nCréation d'un nouveau tournoi :")
    nom = input("Nom du tournoi : ")
    lieu = input("Lieu du tournoi : ")
    date_debut = input("Date de début (YYYY-MM-DD) : ")
    date_fin = input("Date de fin (YYYY-MM-DD) : ")
    description = input("Description du tournoi : ")
    nb_tours = input("Nombre de tours (par défaut 4) : ") or "4"
    return nom, lieu, date_debut, date_fin, description, nb_tours

def afficher_liste_tournois(tournois):
    """Afficher la liste des tournois"""
    print("\n📋 Tournois disponibles :")
    for i, tournoi in enumerate(tournois, start=1):
        print(f"[{i}] {tournoi.nom} ({tournoi.date_debut} → {tournoi.date_fin})")

def afficher_details_tournoi(tournoi):
    """Afficher les détails d'un tournoi"""
    print(f"\n🏆 Détails du tournoi : {tournoi.nom}")
    print(f"Lieu : {tournoi.lieu}")
    print(f"Dates : {tournoi.date_debut} → {tournoi.date_fin}")
    print(f"Nombre de tours : {tournoi.nb_tours}")
    print(f"Description : {tournoi.description}")

# Importer la fonction calcul_scores depuis utils.py
from models.utils import calcul_scores

def afficher_recapitulatif_tournoi(tournoi):
    print(f"\nRécapitulatif du tournoi : {tournoi.nom}")
    print(f"Durée : {tournoi.date_debut} → {tournoi.date_fin}")
    print(f"Nombre de tours : {tournoi.nb_tours}")
    print(f"Description : {tournoi.description}")

    # Calcul des scores totaux
    scores = calcul_scores(tournoi)

    # Affichage des joueurs et scores
    print("\nJoueurs inscrits :")
    print("----------------------------------------------------------------------")
    print(f"{'Nom':<20}{'Prénom':<20}{'Score total':<15}")
    print("----------------------------------------------------------------------")
    for joueur in tournoi.joueurs:
        print(f"{joueur.nom:<20}{joueur.prenom:<20}{scores.get(joueur.id_joueur, 0):<15}")

    # Affichage des résultats des tours
    print("\nRésultats des tours :")
    print("--------------------------------------------------------------------------------------------------")
    print(f"{'Tour':<10}{'Joueur 1':<20}{'Joueur 2':<20}{'Score Joueur 1':<20}{'Score Joueur 2':<20}")
    print("--------------------------------------------------------------------------------------------------")
    for tour in tournoi.tours:
        for match in tour.liste_matchs:
            score1 = match.resultat[0] if match.resultat is not None else "Non joué"
            score2 = match.resultat[1] if match.resultat is not None else "Non joué"
            print(f"{tour.nom:<10}{match.joueur1.nom:<20}{match.joueur2.nom:<20}{str(score1):<20}{str(score2):<20}")

    # Classement final
    print("\nClassement final :")
    print("----------------------------------------------------------------------")
    print(f"{'Nom':<20}{'Prénom':<20}{'Score final':<15}")
    print("----------------------------------------------------------------------")
    classement = sorted(tournoi.joueurs, key=lambda j: scores.get(j.id_joueur, 0), reverse=True)
    for joueur in classement:
        print(f"{joueur.nom:<20}{joueur.prenom:<20}{scores.get(joueur.id_joueur, 0):<15}")