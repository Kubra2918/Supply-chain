import typer
from src.models import Task, Dependency, Project
from src.engine import ProjectEngine

# On initialise l'application Typer
app = typer.Typer(help="Application de gestion de planning de projet (Sujet 05)")

@app.command()
def film():
    """
    Calcule et affiche le planning du projet de tournage d'un film.
    """
    # 1. On charge les données du film avec la nouvelle architecture
    tasks_data = [
        Task(id="A", description="Scénario", duration=30),
        Task(id="B", description="Casting", duration=12, dependencies=[Dependency(task_id="A", lag=15)]),
        Task(id="C", description="Lieu", duration=8, dependencies=[Dependency(task_id="A", lag=20)]),
        Task(id="D", description="Découpage", duration=4, dependencies=[Dependency(task_id="A"), Dependency(task_id="C")]),
        Task(id="E", description="Décors", duration=7, dependencies=[Dependency(task_id="C"), Dependency(task_id="D")]),
        Task(id="F", description="Extérieurs", duration=10, dependencies=[Dependency(task_id="A"), Dependency(task_id="B"), Dependency(task_id="C"), Dependency(task_id="D")]),
        Task(id="G", description="Intérieurs", duration=12, dependencies=[Dependency(task_id="D"), Dependency(task_id="E"), Dependency(task_id="F")]),
        Task(id="H", description="Synchro", duration=3, dependencies=[Dependency(task_id="F"), Dependency(task_id="G")]),
        Task(id="I", description="Montage", duration=14, dependencies=[Dependency(task_id="H")]),
        Task(id="J", description="Son", duration=7, dependencies=[Dependency(task_id="I", lag=3, type="SS"), Dependency(task_id="H")]),
        Task(id="K", description="Mixage", duration=6, dependencies=[Dependency(task_id="I"), Dependency(task_id="J")]),
        Task(id="L", description="Tirage", duration=1, dependencies=[Dependency(task_id="K", lag=2)]),
    ]

    project = Project(tasks=tasks_data)
    engine = ProjectEngine(project)

    # 2. Affichage des résultats dans la console
    print("\n🎬 === RÉSULTAT DE LA SIMULATION DU FILM ===")
    print(f"Durée totale du projet : {engine.get_project_duration()} jours")
    print(f"Chemin critique       : {' ➜ '.join(engine.get_critical_path())}\n")

if __name__ == "__main__":
    app()