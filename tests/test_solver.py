import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from model import Task
from solver import solve_project



def test_film_project():
    tasks = {
        "A": Task("A", 30),
        "B": Task("B", 12, [("A", "finish", 15)]),
        "C": Task("C", 8, [("A", "finish", 20)]),
        "D": Task("D", 4, [("A", "finish", 0), ("C", "finish", 0)]),
        "E": Task("E", 7, [("C", "finish", 0), ("D", "finish", 0)]),
        "F": Task("F", 10, [("A", "finish", 0), ("B", "finish", 0), ("C", "finish", 0), ("D", "finish", 0)]),
        "G": Task("G", 12, [("D", "finish", 0), ("E", "finish", 0), ("F", "finish", 0)]),
        "H": Task("H", 3, [("F", "finish", 0), ("G", "finish", 0)]),
        "I": Task("I", 14, [("H", "finish", 0)]),
        "J": Task("J", 7, [("I", "start", 3), ("H", "finish", 0)]),
        "K": Task("K", 6, [("I", "finish", 0), ("J", "finish", 0)]),
        "L": Task("L", 1, [("K", "finish", 2)]),
    }

    tasks = solve_project(tasks)


    assert tasks["L"].end == 110


def test_simple_case():
    tasks = {
        "A": Task("A", 10),
        "B": Task("B", 5, [("A", "finish", 0)])
    }

    tasks = solve_project(tasks)

    assert tasks["A"].start == 0
    assert tasks["A"].end == 10
    assert tasks["B"].start == 10
    assert tasks["B"].end == 15