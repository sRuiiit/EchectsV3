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


# views/vue_tournoi.py

def afficher_recapitulatif_tournoi(tournoi):
    """
    Affiche un tableau récapitulatif des joueurs, des résultats de chaque tour et des scores totaux.
    """
    print(f"\n📝 Récapitulatif du tournoi : {tournoi.nom} ({tournoi.lieu})")
    print(f"Durée : {tournoi.date_debut} → {tournoi.date_fin}")
    print(f"Nombre de tours : {tournoi.nb_tours}")
    print(f"Description : {tournoi.description}")
    print("\nJoueurs inscrits :")
    print("------------------------------------------------------------")

    # Afficher les joueurs
    print(f"{'Nom':<20}{'Classement':<10}{'ID':<5}{'Score total'}")
    print("-" * 50)
    for joueur in tournoi.joueurs:
        print(f"{joueur.nom} {joueur.prenom:<15}{joueur.classement:<10}{joueur.id_joueur:<5}")

    print("\nRésultats des tours :")
    print("------------------------------------------------------------")

    # Afficher les résultats des tours
    print(f"{'Tour':<10}{'Joueur 1':<20}{'Joueur 2':<20}{'Score Joueur 1':<15}{'Score Joueur 2'}")
    print("-" * 60)

    for i, tour in enumerate(tournoi.tours, start=1):
        for match in tour.liste_matchs:
            print(f"{tour.nom:<10}{match.joueur1.nom:<20}{match.joueur2.nom:<20}"
                  f"{match.resultat[0]:<15}{match.resultat[1]}")

    # Afficher le classement final
    print("\nClassement final :")
    print("------------------------------------------------------------")
    scores = {joueur.id_joueur: 0 for joueur in tournoi.joueurs}

    # Calculer les scores totaux
    for tour in tournoi.tours:
        for match in tour.liste_matchs:
            scores[match.joueur1.id_joueur] += match.resultat[0]
            scores[match.joueur2.id_joueur] += match.resultat[1]

    classement = sorted(tournoi.joueurs, key=lambda j: scores[j.id_joueur], reverse=True)

    print(f"{'Nom':<20}{'Classement':<10}{'Score final'}")
    print("-" * 50)
    for joueur in classement:
        print(f"{joueur.nom} {joueur.prenom:<15}{joueur.classement:<10}{scores[joueur.id_joueur]:<10}")