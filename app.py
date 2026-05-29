import marimo

__generated_with = "0.23.2"
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
    # Cellule 2 : Création des sliders
    sliders_dict = {
        t.id: mo.ui.slider(start=0, stop=50, step=1, label=f"Retard {t.id} ({t.description})")
        for t in tasks_data
    }

    # La magie est ici : on emballe le tout dans un composant UI Marimo
    retards_ui = mo.ui.dictionary(sliders_dict)

    # On affiche
    sliders_view = mo.md(f"### Ajustement des durées \n {retards_ui}")
    sliders_view
    return (retards_ui,)


@app.cell(hide_code=True)
def _(Project, ProjectEngine, Task, mo, retards_ui, tasks_data):
    # Cellule 3 : Calcul avec les nouvelles durées
    # 1. On définit les durées de base
    base_durations = {'A':30,'B':12,'C':8,'D':4,'E':7,'F':10,'G':12,'H':3,'I':14,'J':7,'K':6,'L':1}

    # 2. On lit les valeurs directement depuis retards_ui.value
    simulation_tasks = [
        Task(
            id=t.id, 
            description=t.description, 
            # Ici on utilise retards_ui.value[t.id] pour avoir la réactivité en direct
            duration=base_durations[t.id] + retards_ui.value[t.id],
            dependencies=t.dependencies
        ) for t in tasks_data
    ]

    # 3. Moteur et Calcul
    engine = ProjectEngine(Project(tasks=simulation_tasks))

    # 4. Affichage du résultat
    mo.md(f"""
    ##  Résultat de la simulation
    **Nouvelle durée totale : {engine.get_project_duration()} jours**

    **Chemin critique du planning initial :** `A ➜ C ➜ D ➜ F ➜ G ➜ H ➜ I ➜ K ➜ L`
    """)
    return engine, simulation_tasks


@app.cell(hide_code=True)
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


@app.cell
def _(engine, mo):
    import plotly.express as px
    import pandas as pd
    import datetime

    # 1. On récupère le planning détaillé et le chemin critique
    schedule = engine.get_schedule()
    critical_path = engine.get_critical_path()

    # Plotly a besoin de vraies dates pour le Gantt, on simule que le projet commence aujourd'hui
    start_date = datetime.date.today()

    # 2. On prépare les données pour Plotly
    df_data = []
    for t_id, data in schedule.items():
        df_data.append({
            "Tâche": f"{t_id} - {data['description']}",
            "Début": start_date + datetime.timedelta(days=data['start']),
            "Fin": start_date + datetime.timedelta(days=data['end']),
            # On tag les tâches critiques pour les mettre en rouge
            "Statut": "Critique" if t_id in critical_path else "Normale"
        })
    
    df = pd.DataFrame(df_data)

    # 3. On crée le graphique
    fig = px.timeline(
        df, 
        x_start="Début", 
        x_end="Fin", 
        y="Tâche", 
        color="Statut",
        color_discrete_map={"Critique": "#EF4444", "Normale": "#3B82F6"}, # Rouge et Bleu
        title="📊 Diagramme de Gantt du Projet"
    )
    fig.update_yaxes(autorange="reversed") # Pour avoir la tâche A tout en haut

    # 4. On l'affiche dans Marimo !
    mo.ui.plotly(fig)
    return


if __name__ == "__main__":
    app.run()
