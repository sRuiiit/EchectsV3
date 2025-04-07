# views/vue_match.py

def afficher_match(match):
    print(f"{match.joueur1.nom} vs {match.joueur2.nom} - Résultat : {match.resultat}")


def afficher_resultats_matchs(liste_matchs):
    print("\nRésultats des matchs :")
    for match in liste_matchs:
        afficher_match(match)


# views/vue_menu.py

def afficher_titre():
    print("""
===================================
    LOGICIEL TOURNOIS D'ÉCHECS
===================================
""")