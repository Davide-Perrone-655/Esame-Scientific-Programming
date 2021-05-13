class InitializationError(Exception):
    def __init__(self, name, msg=None):
        if msg is None:
            msg = 'Error in lattice initialization: %s' % name
        super().__init__(msg)

class LoadError(Exception):
    def __init__(self, name, msg=None):
        if msg is None:
            msg = 'Error in loading simulation parameters: %s' % name
        super().__init__(msg)

class OptionError(Exception):
    def __init__(self, name, msg=None):
        if msg is None:
            msg = 'Error in option: %s' % name
        super().__init__(msg)
