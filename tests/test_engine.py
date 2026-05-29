import pytest
from src.models import Task, Dependency, Project
from src.engine import ProjectEngine

def test_film_project():
    # On recrée les données du film avec la nouvelle architecture Pydantic
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
    
    # Vérification de la durée totale
    assert engine.get_project_duration() == 110.0
    
    # Vérification du chemin critique
    critical_path = engine.get_critical_path()
    assert critical_path == ['A', 'C', 'D', 'F', 'G', 'H', 'I', 'K', 'L']

def test_simple_case():
    tasks_data = [
        Task(id="A", description="Tâche A", duration=10),
        Task(id="B", description="Tâche B", duration=5, dependencies=[Dependency(task_id="A")]),
    ]
    engine = ProjectEngine(Project(tasks=tasks_data))
    es_dates = engine.calculate_earliest_dates()
    
    assert es_dates["A"] == 0.0
    assert es_dates["B"] == 10.0
    assert engine.get_project_duration() == 15.0