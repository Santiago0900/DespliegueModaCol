class MarcarLeidoUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, id):
        self.repo.marcar_leido(id)