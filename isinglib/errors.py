import numpy as np
import os
import sys


class InitializationError(Exception):
    def __init__(self, name, msg=None):
        if msg is None:
            msg = 'Error in lattice initialization: %s' % name
        super().__init__(msg)