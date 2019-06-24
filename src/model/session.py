class Session:
    _database = None
    _actions = None

    def __init__(self, database):
        self._database = database
        self._actions = list()

    def add_action(self, action):
        self._actions.append(action)

    def run(self):
        for a in self._actions:
            a(database=self._database)
