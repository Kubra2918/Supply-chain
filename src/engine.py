import networkx as nx
from .models import Project

class ProjectEngine:
    """Calculateur de planning utilisant la méthode du chemin critique."""
    
    def __init__(self, project: Project):
        self.project = project
        self.graph = nx.DiGraph()
        self._build_graph()

    def _build_graph(self):
        """Construit le réseau de tâches."""
        for task in self.project.tasks:
            self.graph.add_node(task.id, duration=task.duration)
            for dep in task.dependencies:
                self.graph.add_edge(dep.task_id, task.id, lag=dep.lag, type=dep.type)

    def calculate_earliest_dates(self) -> dict:
        """Calcule les dates au plus tôt (Forward Pass)."""
        earliest_start = {task.id: 0.0 for task in self.project.tasks}
        
        # On parcourt le graphe dans l'ordre logique (topologique)
        for node in nx.topological_sort(self.graph):
            current_task = next(t for t in self.project.tasks if t.id == node)
            
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