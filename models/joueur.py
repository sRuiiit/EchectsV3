# models/joueur.py

class Joueur:
    def __init__(self, nom, prenom, identifiant_national, classement, id_joueur, date_naissance=None):
        self.nom = nom
        self.prenom = prenom
        self.identifiant_national = identifiant_national
        self.classement = classement
        self.id_joueur = id_joueur
        self.date_naissance = date_naissance

    def to_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "identifiant_national": self.identifiant_national,
            "classement": self.classement,
            "id_joueur": self.id_joueur,
            "date_naissance": self.date_naissance,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["nom"],
            data["prenom"],
            data["identifiant_national"],
            data["classement"],
            data["id_joueur"],
            data.get("date_naissance")
        )

    def __str__(self):
        return f"{self.nom} {self.prenom} (ID: {self.id_joueur}, Classement: {self.classement}, Né(e) le: {self.date_naissance})"
