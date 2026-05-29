import marimo

__generated_with = "0.23.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from src.models import Project, Task, Dependency
    from src.engine import ProjectEngine

    # On définit les données du film 
    tasks_data = [
        Task(id="A", description="Ecriture du scénario", duration=30),
        Task(id="B", description="Casting", duration=12, dependencies=[Dependency(task_id="A", lag=15)]),
        Task(id="C", description="Choix du lieu", duration=8, dependencies=[Dependency(task_id="A", lag=20)]),
        Task(id="D", description="Découpage technique", duration=4, dependencies=[Dependency(task_id="A"), Dependency(task_id="C")]),
        Task(id="E", description="Décors", duration=7, dependencies=[Dependency(task_id="C"), Dependency(task_id="D")]),
        Task(id="F", description="Tournages extérieurs", duration=10, dependencies=[Dependency(task_id="A"), Dependency(task_id="B"), Dependency(task_id="C"), Dependency(task_id="D")]),
        Task(id="G", description="Tournages intérieurs", duration=12, dependencies=[Dependency(task_id="D"), Dependency(task_id="E"), Dependency(task_id="F")]),
        Task(id="H", description="Synchronisation", duration=3, dependencies=[Dependency(task_id="F"), Dependency(task_id="G")]),
        Task(id="I", description="Montage", duration=14, dependencies=[Dependency(task_id="H")]),
        Task(id="J", description="Son", duration=7, dependencies=[Dependency(task_id="I", lag=3, type="SS"), Dependency(task_id="H")]),
        Task(id="K", description="Mixage", duration=6, dependencies=[Dependency(task_id="I"), Dependency(task_id="J")]),
        Task(id="L", description="Tirage", duration=1, dependencies=[Dependency(task_id="K", lag=2)]),
    ]
    return Project, ProjectEngine, Task, mo, tasks_data


@app.cell
def _(mo, tasks_data):
    # On crée les sliders à partir des données de base
    retards_dict = {
        t.id: mo.ui.slider(start=0, stop=50, step=1, label=f"Retard {t.id} ({t.description})")
        for t in tasks_data
    }

    # On prépare l'affichage des sliders
    sliders_view = mo.md(f"###  Ajustement des durées \n {mo.vstack(list(retards_dict.values()))}")

    # On affiche
    sliders_view
    return (retards_dict,)


@app.cell
def _(Project, ProjectEngine, Task, mo, retards_dict, tasks_data):
    # 1. On définit les durées de base
    base_durations = {'A':30,'B':12,'C':8,'D':4,'E':7,'F':10,'G':12,'H':3,'I':14,'J':7,'K':6,'L':1}

    # 2. On reconstruit les tâches (la lecture de .value active le "Live")
    simulation_tasks = [
        Task(
            id=t.id, 
            description=t.description, 
            duration=base_durations[t.id] + retards_dict[t.id].value,
            dependencies=t.dependencies
        ) for t in tasks_data
    ]
    #J'ai essayé de faire en sorte que en faisant bouger les sliders au dessus ca actualiserait cette cellule et celle d'en dessous en meme temps, mais je n'ai pas réussi. Avec un seul slidder pour une seule tache, ca marche c'est bien réactif automatiquement sans devoir run les cellules en dessous mais quand j'ne ai ajouté plusieurs je dois run cette cellule pour mettre à jour les visualisations.

    # 3. Moteur et Calcul
    engine = ProjectEngine(Project(tasks=simulation_tasks))

    # 4. Affichage du résultat
    mo.md(f"""
    ##  Résultat de la simulation
    **Nouvelle durée totale : {engine.get_project_duration()} jours**

    **Chemin critique du planning initial :** `A ➜ C ➜ D ➜ F ➜ G ➜ H ➜ I ➜ K ➜ L`
    """)
    return engine, simulation_tasks


@app.cell
def _(engine, mo, simulation_tasks):
    # 1. On récupère les dates de début au plus tôt
    es_dates = engine.calculate_earliest_dates()

    # 2. On prépare les données pour le tableau avec Début et Fin
    data_table = []
    for task in simulation_tasks:
        start = es_dates[task.id]
        finish = start + task.duration
        data_table.append({
            "Tâche": task.id,
            "Description": task.description,
            "Début": f"Jour {start}",
            "Fin": f"Jour {finish}"
        })

    # 3. Affichage du tableau
    mo.ui.table(data_table, page_size=12) # ici page_size=12 pour faire tenir toutes les taches sur une seule page du tableau, sinon 2 pages donc moins lisible
    return


if __name__ == "__main__":
    app.run()
