import freezerstate.config


class MssqlArchiver():

    def __init__(self):
        self.module = '[MSSQL]'
        self.enabled = freezerstate.CONFIG.MSSQL_ENABLED

    def update(self, updateRecord):
        # TODO: complete this method

        return True
