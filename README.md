# 🎬 Projet Supply Chain – Planification de tâches (Sujet 05)

Ce projet propose un moteur de calcul robuste pour résoudre des problèmes d'ordonnancement de tâches avec contraintes de dépendance (calcul de chemin critique, dates au plus tôt, durée totale).

Il est appliqué ici au cas concret du **tournage d'un film** (110 jours de durée totale).

---

## ✨ Fonctionnalités

* **Moteur mathématique** : Modélisation réseau via `NetworkX` et validation des données via `Pydantic`.
* **Interface CLI (Typer)** : Application en ligne de commande claire et rapide.
* **Interface GUI (Marimo)** : Dashboard interactif avec curseurs de simulation et **diagramme de Gantt** en temps réel.
* **Qualité pro** : Code typé (`mypy`), linté (`ruff`) et testé à 100% (`pytest`).

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
python main.py
~~~

**Résultat attendu :**
> 🎬 === RÉSULTAT DE LA SIMULATION DU FILM ===  
> Durée totale du projet : 110.0 jours  
> Chemin critique : A ➜ C ➜ D ➜ F ➜ G ➜ H ➜ I ➜ K ➜ L

### 3. Interface Graphique Interactive (GUI)
Pour ouvrir le tableau de bord interactif et visualiser le diagramme de Gantt :

~~~bash
marimo edit app.py
~~~

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

Pour lancer la suite de tests et vérifier la couverture :

~~~bash
python -m pytest --cov=src
~~~

Pour vérifier le typage et le linting :

~~~bash
python -m mypy src/
python -m ruff check .
~~~

---
**Auteurs :** KURNAZ Kubra & MOREAU Matteo