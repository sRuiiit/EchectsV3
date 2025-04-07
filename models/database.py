# models/database.py

from tinydb import TinyDB, Query
from models.joueur import Joueur
from models.tournoi import Tournoi

class DatabaseManager:
    def __init__(self, db_path="db.json"):
        self.db = TinyDB(db_path)
        self.players_table = self.db.table("players")
        self.tournaments_table = self.db.table("tournaments")

    def insert_player(self, joueur):
        self.players_table.insert(joueur.to_dict())

    def get_all_players(self):
        return [Joueur.from_dict(j) for j in self.players_table.all()]

    def insert_tournament(self, tournoi):
        self.tournaments_table.insert(tournoi.to_dict())

    def get_all_tournaments(self):
        return [Tournoi.from_dict(t) for t in self.tournaments_table.all()]
