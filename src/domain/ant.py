class Ant:
    def __init__(self, id: str, path: list[str]) -> None:
        self.id = id
        self.path = path
        self.position: str | None = path[0] if path else None

    def move(self) -> None:
        if self.path:
            self.position = self.path.pop(0)