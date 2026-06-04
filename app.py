import marimo

__generated_with = "0.23.2"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    from src.models import Project, Task, Dependency
    from src.engine import ProjectEngine
    import plotly.express as px
    import pandas as pd
    import datetime

    # Le modèle par défaut du film
    default_tasks = [
        Task(id="A", description="Ecriture du scénario", duration=30),
        Task(id="B", description="Casting", duration=12, dependencies=[Dependency(task_id="A", lag=15)]),
        Task(id="C", description="Choix du lieu", duration=8, dependencies=[Dependency(task_id="A", lag=20)]),
        Task(id="D", description="Découpage technique", duration=4, dependencies=[Dependency(task_id="A"), Dependency(task_id="C")]),
        Task(id="E", description="Décors", duration=7, dependencies=[Dependency(task_id="C"), Dependency(task_id="D")]),
        Task(id="F", description="Tournages extérieurs", duration=10, dependencies=[Dependency(task_id="A"), Dependency(task_id="B"), Dependency(task_id="C"), Dependency(task_id="D")]),
        Task(id="G", description="Tournages intérieurs", duration=12, dependencies=[Dependency(task_id="D"), Dependency(task_id="E"), Dependency(task_id="F")]),
        Task(id="H", description="Synchronisation", duration=3, dependencies=[Dependency(task_id="F"), Dependency(task_id="G")]),
        Task(id="I", description="Montage", duration=14, dependencies=[Dependency(task_id="H")]),
        # Exemple de tâche SS dans le modèle de base :
        Task(id="J", description="Son", duration=7, dependencies=[Dependency(task_id="I", lag=3, type="SS"), Dependency(task_id="H")]),
        Task(id="K", description="Mixage", duration=6, dependencies=[Dependency(task_id="I"), Dependency(task_id="J")]),
        Task(id="L", description="Tirage", duration=1, dependencies=[Dependency(task_id="K", lag=2)]),
    ]
    return Dependency, Project, ProjectEngine, Task, datetime, default_tasks, mo, pd, px


@app.cell
def _(mo):
    # Gestion d'état : on démarre sur un projet vide
    get_tasks, set_tasks = mo.state([])
    return get_tasks, set_tasks


@app.cell
def _(default_tasks, get_tasks, mo, set_tasks):
    # Fonctions des boutons globaux
    def load_movie(*args):
        set_tasks(default_tasks)

    def clear_all(*args):
        set_tasks([])

    btn_movie = mo.ui.button(label="🎬 Charger l'exemple (Sujet 05)", on_click=load_movie)
    btn_clear = mo.ui.button(label="🗑️ Vider le projet", on_click=clear_all)
    
    return btn_clear, btn_movie, clear_all, load_movie


@app.cell
def _(Dependency, Task, get_tasks, mo, set_tasks):
    # --- ZONE 1 : AJOUT DE TÂCHE ---
    id_in = mo.ui.text(label="ID de la tâche (ex: M)")
    desc_in = mo.ui.text(label="Nom / Description")
    dur_in = mo.ui.number(start=1, stop=1000, value=1, label="Durée (jours)")
    deps_in = mo.ui.text(label="Prérequis (Optionnel)")

    def create_task(*args):
        v_id = id_in.value.strip()
        v_desc = desc_in.value
        v_dur = dur_in.value
        v_deps = deps_in.value
        
        if v_id:  
            try:
                deps = []
                if v_deps:
                    for d in v_deps.split(","):
                        parts = d.strip().split(":")
                        t_id = parts[0].strip()
                        lag = int(parts[1]) if len(parts) > 1 else 0
                        
                        # NOUVEAU : On gère le tag :SS s'il est présent
                        if len(parts) > 2 and parts[2].strip().upper() == "SS":
                            deps.append(Dependency(task_id=t_id, lag=lag, type="SS"))
                        else:
                            deps.append(Dependency(task_id=t_id, lag=lag))
                
                new_task = Task(id=v_id, description=v_desc, duration=v_dur, dependencies=deps)
                
                current_ids = [t.id for t in get_tasks()]
                if new_task.id not in current_ids:
                    set_tasks(get_tasks() + [new_task])
            except Exception:
                pass 

    btn_add = mo.ui.button(label="➕ Créer la tâche", on_click=create_task)
    
    # NOUVEAU : La bulle d'aide explique la commande :SS
    task_form_ui = mo.md(f'''
    {id_in} {desc_in} 
    {dur_in} 
    {deps_in}
    
    <small><i>💡 <b>Comment remplir les prérequis ?</b><br>
    - Laissez vide si la tâche n'a pas de prérequis.<br>
    - <b>Après la FIN d'une tâche :</b> Tapez la lettre et les jours d'attente (ex: <b>A:15</b> pour attendre 15j après la FIN de A).<br>
    - <b>Depuis le DÉBUT d'une tâche :</b> Ajoutez <b>:SS</b> à la fin (ex: <b>A:10:SS</b> pour démarrer 10j après le DÉBUT de A).<br>
    - Séparez par des virgules s'il y en a plusieurs (ex: <b>A, B:15, C:10:SS</b>).
    </i></small>
    
    <br><br>
    {btn_add}
    ''')

    # --- ZONE 2 : SUPPRESSION SPÉCIFIQUE ---
    del_id_in = mo.ui.text(label="ID de la tâche à effacer (ex: C)")
    
    def delete_specific_task(*args):
        target_id = del_id_in.value.strip()
        if target_id:
            set_tasks([t for t in get_tasks() if t.id != target_id])

    btn_del = mo.ui.button(label="❌ Supprimer cette tâche", on_click=delete_specific_task)
    del_form_ui = mo.md(f'''{del_id_in} <br> {btn_del}''')
    
    return (
        btn_add, btn_del, create_task, delete_specific_task,
        del_form_ui, del_id_in, deps_in, desc_in, dur_in, id_in, task_form_ui
    )


@app.cell
def _(btn_clear, btn_movie, del_form_ui, mo, task_form_ui):
    # Assemblage du menu supérieur
    ui_controls = mo.md(f'''
    ## ⚙️ Éditeur de Projet Supply Chain

    **1. Actions globales :** {btn_movie} {btn_clear}
    
    ---
    
    **2. ➕ Ajouter une nouvelle tâche :**
    {task_form_ui}
    
    ---
    
    **3. ➖ Retirer une tâche spécifique :**
    {del_form_ui}
    ''')
    
    return ui_controls,


@app.cell
def _(Project, ProjectEngine, datetime, get_tasks, mo, pd, px, ui_controls):
    # Affichage central utilisant mo.vstack pour une stabilité d'affichage parfaite
    def _build_dashboard():
        current_tasks = get_tasks()

        if not current_tasks:
            return mo.vstack([
                ui_controls,
                mo.md("⚠️ **Le projet est actuellement vide. Commencez par créer une tâche ou cliquez sur '🎬 Charger l'exemple'.**")
            ])
            
        try:
            project = Project(tasks=current_tasks)
            engine = ProjectEngine(project)

            duration = engine.get_project_duration()
            crit_path = engine.get_critical_path()
            schedule = engine.get_schedule()

            table_data = []
            for t in current_tasks:
                # NOUVEAU : Le tableau est intelligent et indique si on part de la fin ou du début !
                deps_list = []
                for d in t.dependencies:
                    d_type = getattr(d, "type", "FS") # FS (Finish-to-Start) est la valeur par défaut
                    if d_type == "SS":
                        deps_list.append(f"{d.task_id} (+{d.lag}j depuis le DÉBUT)")
                    else:
                        deps_list.append(f"{d.task_id} (+{d.lag}j depuis la FIN)")
                
                deps_str = ", ".join(deps_list) if deps_list else "Aucun"
                table_data.append({"ID": t.id, "Tâche": t.description, "Durée": f"{t.duration}j", "Prérequis": deps_str})

            start_date = datetime.date.today()
            df_data = []
            for t_id, data in schedule.items():
                df_data.append({
                    "Tâche": f"{t_id} - {data['description']}",
                    "Début": start_date + datetime.timedelta(days=data['start']),
                    "Fin": start_date + datetime.timedelta(days=data['end']),
                    "Statut": "Critique" if t_id in crit_path else "Normale"
                })
            
            df = pd.DataFrame(df_data)
            fig = px.timeline(
                df, x_start="Début", x_end="Fin", y="Tâche", color="Statut",
                color_discrete_map={"Critique": "#EF4444", "Normale": "#3B82F6"},
                title="📊 Diagramme de Gantt"
            )
            fig.update_yaxes(autorange="reversed")

            return mo.vstack([
                ui_controls,
                mo.md("---"),
                mo.md("### 📋 Cahier des charges actuel"),
                mo.ui.table(table_data, page_size=15),
                mo.md("---"),
                mo.md(f"### 🚀 Résultats de l'analyse\n**Durée totale estimée : {duration} jours** | **Chemin critique :** `{' ➜ '.join(crit_path)}`"),
                fig
            ])
            
        except Exception as e:
            return mo.vstack([
                ui_controls,
                mo.md("---"),
                mo.md(f"❌ **Impossible de calculer le planning.** `Détail de l'erreur : {str(e)}`\n\n*Vérifiez vos prérequis. Si vous venez de supprimer une tâche, assurez-vous qu'elle n'était pas un prérequis pour une autre tâche encore présente dans le tableau.*")
            ])

    ui_dashboard = _build_dashboard()
    ui_dashboard
    return ui_dashboard,


if __name__ == "__main__":
    app.run()