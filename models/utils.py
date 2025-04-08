# models/utils.py

from collections import defaultdict

def calcul_scores(tournoi):
    scores = defaultdict(float)
    for tour in tournoi.tours:
        for match in tour.liste_matchs:
            if match.resultat:
                scores[match.joueur1.id_joueur] += match.resultat[0]
                scores[match.joueur2.id_joueur] += match.resultat[1]
    return scores