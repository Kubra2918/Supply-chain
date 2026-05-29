from model import Task
from solver import solve_project
import matplotlib.pyplot as plt


def build_film_example():
    return {
        "A": Task("A", 30),
        "B": Task("B", 12, [("A", "finish", 15)]),
        "C": Task("C", 8, [("A", "finish", 20)]),
        "D": Task("D", 4, [("A", "finish", 0), ("C", "finish", 0)]),
        "E": Task("E", 7, [("C", "finish", 0), ("D", "finish", 0)]),
        "F": Task("F", 10, [
            ("A", "finish", 0),
            ("B", "finish", 0),
            ("C", "finish", 0),
            ("D", "finish", 0)
        ]),
        "G": Task("G", 12, [
            ("D", "finish", 0),
            ("E", "finish", 0),
            ("F", "finish", 0)
        ]),
        "H": Task("H", 3, [
            ("F", "finish", 0),
            ("G", "finish", 0)
        ]),
        "I": Task("I", 14, [("H", "finish", 0)]),
        "J": Task("J", 7, [
            ("I", "start", 3),
            ("H", "finish", 0)
        ]),
        "K": Task("K", 6, [
            ("I", "finish", 0),
            ("J", "finish", 0)
        ]),
        "L": Task("L", 1, [("K", "finish", 2)]),
    }


def display_table(tasks):
    print("\nPlanning du projet :\n")
    print(f"{'Tâche':<10}{'Début':<10}{'Fin':<10}")

    for name, task in tasks.items():
        print(f"{name:<10}{task.start:<10}{task.end:<10}")

    print("\nDurée totale du projet :", tasks["L"].end, "jours")
    print("Chemin critique : A -> C -> D -> F -> G -> H -> I -> K -> L")


def plot_gantt(tasks):
    fig, ax = plt.subplots()

    y = 0
    for name, task in tasks.items():
        ax.barh(y, task.duration, left=task.start)
        ax.text(task.start, y, name, va='center', ha='right')
        y += 1

    ax.set_xlabel("Temps (jours)")
    ax.set_ylabel("Tâches")
    ax.set_title("Diagramme de Gantt")

    plt.show()


def main():
    print("=== PLANIFICATION DE PROJET ===")
    print("1 - Résoudre l'exemple du film")
    print("2 - Quitter")

    choice = input("Choisissez une option : ")

    if choice == "1":
        tasks = build_film_example()
        tasks = solve_project(tasks)

        display_table(tasks)
        plot_gantt(tasks)

    elif choice == "2":
        print("Fin du programme.")
    else:
        print("Option invalide.")


if __name__ == "__main__":
    main()