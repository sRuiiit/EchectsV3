## Logiciel de Gestion de Tournois d'Échecs (CLI - Python)

Ce programme permet de gérer des tournois d'échecs en local (hors ligne), en ligne de commande, avec une structure claire en architecture MVC (Modèle - Vue - Contrôleur) et une base de données légère (TinyDB).

---

### 🔧 Fonctionnalités

- Ajouter et afficher des **joueurs** (avec nom, prénom, classement, identifiant national, ID unique).
- Créer et consulter des **tournois** (nom, lieu, dates, description, nombre de tours, sélection de joueurs).
- Lancer un tournoi avec **appariements automatiques** sans répétition (chaque joueur ne joue qu'une fois contre les autres).
- Gérer les **rounds** avec saisie sécurisée des scores et attribution automatique des BYEs si impair.
- Affichage clair des **résultats** et du **classement final**.
- Sauvegarde automatique après chaque round.
- Interface 100% **en ligne de commande**.
- Persistance des données avec **TinyDB** (format JSON).
- Code structuré en **POO** et conforme à la PEP8.

---

### 📁 Structure du Projet

```
echiquier/
├── controllers/
│   ├── controleur_application.py
│   ├── controleur_joueur.py
│   ├── controleur_menu.py
│   └── controleur_tournoi.py
├── models/
│   ├── joueur.py
│   ├── tournoi.py
│   ├── match.py
│   ├── tour.py
│   ├── utils.py
│   └── database.py
├── views/
│   ├── vue_joueur.py
│   ├── vue_tournoi.py
│   ├── vue_match.py
│   └── vue_menu.py
├── main.py
└── requirements.txt
```

---

### ▶️ Lancer l'application

```bash
python main.py
```

---

### 📦 Installation des dépendances

```bash
pip install -r requirements.txt
```

---

### ✅ Outils de Qualité de Code

- [flake8](https://flake8.pycqa.org/) — vérification PEP8
- [black](https://black.readthedocs.io/) — formatage automatique
- [isort](https://pycqa.github.io/isort/) — tri des imports

---

### 💾 Base de données

- Fichier JSON généré automatiquement : `db.json`
- Format de stockage léger avec [TinyDB](https://tinydb.readthedocs.io/en/latest/).

---

### 📌 Fonctionnalités récemment ajoutées (2025)

- ✅ Saisie guidée des scores avec validation sécurisée (1, 0.5, 0).
- ✅ Affichage automatique des matchs à jouer pour chaque round.
- ✅ Système de rounds intelligent évitant les doublons d’appariement.
- ✅ Attribution automatique de victoire pour BYE si nombre impair de joueurs.
- ✅ Suppression des doublons visuels dans les rapports (liste joueurs vs classement).

---

### 🧭 Prochaines améliorations possibles

- Export des tournois (CSV, TXT, PDF).
- Interface graphique (Tkinter, web, etc.).
- Classement cumulé multi-tournois.
- Interface d’administration avec historique des performances.

---

### 👤 Auteur

Développé en 2025 par **Steve Raffner** — Développeur Python junior freelance.

Projet réalisé dans le cadre d'une formation OpenClassrooms. 🧠

---

### 🪪 Licence

Ce projet est libre d'utilisation pour un usage non-commercial ou éducatif.