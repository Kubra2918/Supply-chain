from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Dependency(BaseModel):
    """Représente un lien entre deux tâches."""
    task_id: str
    lag: float = 0.0
    type: Literal["FS", "SS"] = "FS"  # FS: Fin-à-Début, SS: Début-à-Début

class Task(BaseModel):
    """Définit une tâche du projet."""
    id: str
    description: str
    duration: float = Field(..., gt=0)
    dependencies: List[Dependency] = []

class Project(BaseModel):
    """Conteneur pour l'ensemble des tâches."""
    tasks: List[Task]