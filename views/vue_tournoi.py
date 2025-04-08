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