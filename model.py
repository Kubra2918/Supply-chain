from typing import List, Tuple


class Task:
    def __init__(
        self,
        name: str,
        duration: int,
        dependencies: List[Tuple[str, str, int]] = None,
    ):
        self.name: str = name
        self.duration: int = duration
        self.dependencies: List[Tuple[str, str, int]] = dependencies if dependencies else []

        self.start: int = 0
        self.end: int = 0

    def __repr__(self) -> str:
        return f"{self.name} (start={self.start}, end={self.end})"