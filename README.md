# 🎬 Projet Supply Chain – Planification de tâches (Sujet 05)

Ce projet propose un moteur de calcul robuste pour résoudre des problèmes d'ordonnancement de tâches avec contraintes de dépendance (calcul de chemin critique, dates au plus tôt, durée totale).

Il est appliqué ici au cas concret du **tournage d'un film** (110 jours de durée totale).

---

## ✨ Fonctionnalités

* **Moteur mathématique** : Modélisation réseau via `NetworkX` et validation des données via `Pydantic`.
* **Interface CLI (Typer)** : Application en ligne de commande claire et rapide.
* **Interface GUI (Marimo)** : Dashboard interactif avec curseurs de simulation et **diagramme de Gantt** en temps réel.
* **Qualité** : Code typé (`mypy`), linté (`ruff`) et testé à 100% (`pytest`).

---

## 🚀 Démonstration et Utilisation

Nous recommandons d'utiliser [uv](https://github.com/astral-sh/uv) pour garantir une installation ultra-rapide et portable.

### 1. Installation
Clonez le dépôt, puis installez les dépendances :

~~~bash
uv pip install -e .
~~~

*(Note : Si vous n'utilisez pas `uv`, la commande standard `pip install -e .` fonctionnera également).*

### 2. Interface en Ligne de Commande (CLI)
L'interface est propulsée par `Typer`. Pour lancer le calcul du film directement dans votre terminal :

~~~bash
uv run python main.py
~~~

**Résultat attendu :**
> 🎬 === RÉSULTAT DE LA SIMULATION DU FILM ===  
> Durée totale du projet : 110.0 jours  
> Chemin critique : A ➜ C ➜ D ➜ F ➜ G ➜ H ➜ I ➜ K ➜ L

### 3. Interface Graphique Interactive (GUI)
L'application inclut un véritable **Éditeur de Projet dynamique** propulsé par Marimo. Ce n'est pas un simple visualiseur : vous pouvez créer, modifier et simuler vos propres plannings en temps réel.

Pour lancer l'interface :
~~~bash
uv run marimo edit app.py
~~~

**✨ Fonctionnalités de l'éditeur :**
- **Création dynamique :** Ajoutez ou supprimez des tâches avec leurs durées et prérequis. Le tableau, le chemin critique et le diagramme de Gantt (Plotly) se mettent à jour instantanément.
- **Gestion des dépendances avancées :** Notre moteur comprend la syntaxe de contraintes :
  - `A` : Commence dès la fin de A.
  - `A:15` : Commence 15 jours après la **fin** de A (Finish-to-Start avec délai).
  - `A:10:SS` : Commence 10 jours après le **début** de A (Start-to-Start avec délai).
  - *Note : Vous pouvez cumuler les prérequis en les séparant par des virgules (ex: `A, B:15, C:10:SS`).*
- **Sécurité anti-crash :** Si vous créez une boucle infinie (ex: A dépend de B, et B dépend de A) ou une dépendance vers une tâche inexistante, le moteur l'intercepte et affiche une alerte explicite.
- **Chargement rapide :** Un bouton permet de charger instantanément le cahier des charges du "Sujet 05" (Le Film) pour la démonstration.

---

## 📂 Architecture du Projet

Le projet a été refactorisé pour suivre les standards modernes de Python :

~~~text
SUPPLY-CHAIN/
├── src/
│   ├── engine.py        # Moteur de calcul (NetworkX)
│   └── models.py        # Modèles de données (Pydantic)
│
├── tests/
│   └── test_engine.py   # Tests unitaires (100% coverage)
│
├── app.py               # Application interactive (Marimo)
├── main.py              # CLI (Typer)
├── pyproject.toml       # Enregistrement des dépendances (uv/pip)
└── README.md
~~~

---

## 🧪 Tests et Qualité

Pour lancer la suite de tests ou vérifier le code, vous devez d'abord installer les dépendances de développement :

~~~bash
uv pip install -e ".[dev]"
~~~

Ensuite, pour lancer les tests et vérifier la couverture à 100% :
~~~bash
uv run pytest
~~~

Pour vérifier le typage et le linting :
~~~bash
uv run mypy src/
uv run ruff check .
~~~