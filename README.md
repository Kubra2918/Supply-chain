#  Projet Supply Chain – Planification de tâches

##  Objectif du projet

Ce projet a pour objectif de résoudre un problème d’ordonnancement de tâches avec contraintes de dépendance.

À partir d’un ensemble de tâches, nous cherchons à :

* déterminer les dates de début et de fin de chaque tâche
* calculer la durée totale du projet
* identifier le chemin critique

---

##  Cas étudié : tournage d’un film

Nous avons appliqué notre modèle à un exemple de planification du tournage d’un film.

Résultats obtenus :

* **Durée totale du projet : 110 jours**
* **Chemin critique :**

  A → C → D → F → G → H → I → K → L

Le chemin critique correspond à la suite de tâches qui détermine la durée minimale du projet.

---

##  Fonctionnalités

Le programme permet de :

* modéliser des tâches avec des dépendances
* calculer automatiquement les dates de début et de fin
* déterminer un ordre valide d’exécution
* afficher les résultats sous forme de tableau
* visualiser le planning avec un diagramme de Gantt
* utiliser une interface simple en ligne de commande
* utiliser une interface interactive avec Marimo

---

##  Structure du projet

```
SUPPLY CHAIN/
│
├── src/
│   ├── models.py        # Classes (Task, Dependency, Project)
│   └── engine.py        # Moteur de calcul (ProjectEngine)
│
├── model.py             # Modélisation simple des tâches
├── solver.py            # Algorithme de résolution du planning
├── app.py               # Interface interactive Marimo
├── main.py              # Interface en ligne de commande
├── notebook_supply_chain.ipynb
├── README.md
│
├── tests/
│   ├── test_solver.py
│   └── test_engine.py
```

---

##  Lancer le programme

Dans le terminal, se placer dans le dossier du projet puis exécuter :

```bash
python main.py
```

Ensuite, choisir :

```
1
```

Le programme affiche :

* le planning des tâches
* la durée totale du projet
* le chemin critique

Un diagramme de Gantt s’ouvre également pour visualiser le planning.

---
## Interface interactive (Marimo)

Une interface interactive a été développée avec Marimo.

Elle permet de :

* modifier les durées des tâches avec des sliders
* simuler l’impact sur le planning
* afficher les résultats dynamiquement

Lancer l’interface :

```
marimo edit app.py
```

---

##  Tests

Des tests ont été réalisés avec **pytest** pour vérifier le bon fonctionnement du programme.

Pour lancer les tests :

```bash
pytest
```

Résultat attendu :

```
5 passed
```

---

## 🧠 Approche

Le projet a été réalisé en plusieurs étapes :

1. Résolution manuelle du problème dans un notebook
2. Généralisation du modèle à une famille de problèmes
3. Implémentation d’une solution en Python (structure modulaire)
4. Ajout d’une interface utilisateur (CLI + Marimo) et d’une visualisation graphique

---

##  Auteur

KURNAZ Kubra
MOREAU Matteo
