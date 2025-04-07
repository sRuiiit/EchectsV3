# models/database.py

from tinydb import TinyDB, Query
from models.joueur import Joueur
from models.tournoi import Tournoi

class DatabaseManager:
    def __init__(self, db_path="echiquier.json"):
        self.db = TinyDB(db_path)
        self.players_table = self.db.table("players")
        self.tournaments_table = self.db.table("tournaments")

        # Initialisation sécurisée des compteurs
        all_tournois = self.tournaments_table.all()
        self.tournament_count = max(
            [t.get("id_tournoi", 0) for t in all_tournois], default=0
        )

        all_joueurs = self.players_table.all()
        self.player_count = max(
            [j.get("id_joueur", 0) for j in all_joueurs], default=0
        )

    def insert_player(self, joueur):
        self.player_count += 1
        joueur.id_joueur = self.player_count
        self.players_table.insert(joueur.to_dict())

    def get_player(self, player_id):
        player_data = self.players_table.get(Query().id_joueur == player_id)
        if player_data:
            return Joueur.from_dict(player_data)
        return None

    def update_player(self, joueur):
        self.players_table.update(joueur.to_dict(), Query().id_joueur == joueur.id_joueur)

    def delete_player(self, player_id):
        self.players_table.remove(Query().id_joueur == player_id)

    def get_all_players(self):
        return [Joueur.from_dict(player) for player in self.players_table.all()]

    def insert_tournament(self, tournoi):
        self.tournament_count += 1
        tournoi.id_tournoi = self.tournament_count
        self.tournaments_table.insert(tournoi.to_dict())

    def update_tournament(self, tournoi):
        self.tournaments_table.update(
            tournoi.to_dict(),
            Query().id_tournoi == tournoi.id_tournoi
        )

    def get_tournament(self, tournament_id):
        tournament_data = self.tournaments_table.get(Query().id_tournoi == tournament_id)
        if tournament_data:
            return Tournoi.from_dict(tournament_data)
        return None

    def delete_tournament(self, tournament_id):
        self.tournaments_table.remove(Query().id_tournoi == tournament_id)

    def get_all_tournaments(self):
        return [Tournoi.from_dict(tournoi) for tournoi in self.tournaments_table.all()]