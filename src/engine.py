import networkx as nx
from .models import Project

class ProjectEngine:
    """Calculateur de planning utilisant la méthode du chemin critique."""
    
    def __init__(self, project: Project):
        self.project = project
        # On ajoute le type ": nx.DiGraph" grace à mypy pour mieux comprendre le type de graphe que nous utilisons
        self.graph: nx.DiGraph = nx.DiGraph()
        self._build_graph()

    def _build_graph(self):
        """Construit le réseau de tâches."""
        for task in self.project.tasks:
            self.graph.add_node(task.id, duration=task.duration)
            for dep in task.dependencies:
                # 1. On cherche la tâche précédente pour calculer le "poids" du lien
                pred_task = next(t for t in self.project.tasks if t.id == dep.task_id)
                
                # 2. Calcul du poids temporel (Durée + Décalage)
                if dep.type == "FS":
                    poids = pred_task.duration + dep.lag
                else:  # SS (Début à Début)
                    poids = dep.lag
                
                # 3. On ajoute le poids à l'arête pour que NetworkX trouve le vrai chemin
                self.graph.add_edge(
                    dep.task_id, 
                    task.id, 
                    lag=dep.lag, 
                    type=dep.type,
                    weight=poids  # L'ingrédient secret !
                )

    def calculate_earliest_dates(self) -> dict:
        """Calcule les dates au plus tôt (Forward Pass)."""
        earliest_start = {task.id: 0.0 for task in self.project.tasks}
        
        # On parcourt le graphe dans l'ordre logique (topologique)
        for node in nx.topological_sort(self.graph):
            
            
            # La date de début est le max des contraintes de ses prédécesseurs
            for pred_id in self.graph.predecessors(node):
                edge_data = self.graph.get_edge_data(pred_id, node)
                pred_task = next(t for t in self.project.tasks if t.id == pred_id)
                
                if edge_data['type'] == "FS":  # Fin à Début
                    arrival = earliest_start[pred_id] + pred_task.duration + edge_data['lag']
                else:  # SS: Début à Début (ex: tâche J)
                    arrival = earliest_start[pred_id] + edge_data['lag']
                
                earliest_start[node] = max(earliest_start[node], arrival)
                
        return earliest_start

    def get_project_duration(self) -> float:
        """Retourne la durée totale du projet."""
        es = self.calculate_earliest_dates()
        return max(es[t.id] + t.duration for t in self.project.tasks)
    
    def get_critical_path(self) -> list:
        """Retourne la liste des tâches sur le chemin le plus long."""
        import networkx as nx
        return nx.dag_longest_path(self.graph)
    
    #Pour utiliser le diagramme de Gantt, nous avons besoin de connaître les dates de début et de fin de chaque tâche.
    #Cette méthode calcule ces dates en fonction des dépendances et des durées.
    def get_schedule(self) -> dict:
        """Calcule les dates de début et de fin pour chaque tâche."""
        import networkx as nx
        schedule = {}
        
        # On parcourt les tâches dans l'ordre chronologique des dépendances
        for node in nx.topological_sort(self.graph):
            task = next(t for t in self.project.tasks if t.id == node)
            early_start = 0
            
            # On regarde toutes les tâches précédentes pour trouver la date de début
            for pred in self.graph.predecessors(node):
                edge_data = self.graph.get_edge_data(pred, node)
                pred_end = schedule[pred]['end']
                pred_start = schedule[pred]['start']
                
                # Prise en compte du type de lien (Fin-à-Début ou Début-à-Début)
                if edge_data['type'] == 'FS':
                    start_from_pred = pred_end + edge_data['lag']
                else:
                    start_from_pred = pred_start + edge_data['lag']
                    
                early_start = max(early_start, start_from_pred)
            
            schedule[node] = {
                'id': task.id,
                'description': task.description,
                'start': early_start,
                'end': early_start + task.duration
            }
        return schedule