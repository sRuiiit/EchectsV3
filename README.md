Echiquier Mvc
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
# README.md

## Logiciel de Gestion de Tournois d'Échecs (CLI - Python)

Ce programme permet de gérer des tournois d'échecs en local (hors ligne), en ligne de commande, avec une structure claire en architecture MVC (Modèle - Vue - Contrôleur) et une base de données légère (TinyDB).

---

### 🔧 Fonctionnalités

- Ajouter et afficher des **joueurs** (avec nom, prénom, classement, identifiant national, ID unique).
- Créer et consulter des **tournois** (nom, lieu, dates, joueurs).
- Afficher les **listes de joueurs** et de **tournois** enregistrés.
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

### 📌 À améliorer dans les versions futures

- Gestion des matchs et des résultats
- Génération automatique des appariements
- Classement des joueurs dans un tournoi
- Export de rapports au format texte/CSV

---

### 👤 Auteur

Développé en 2025 par Steve Raffner — Développeur Python junior freelance.

Projet réalisé dans le cadre d'une formation OpenClassrooms. 🧠

---

### Licence

Ce projet est libre d'utilisation pour un usage non-commercial ou éducatif.

