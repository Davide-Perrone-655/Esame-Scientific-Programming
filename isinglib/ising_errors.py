#!/usr/bin/env python3

'''Error classes'''

import typing as tp

class InitializationError(Exception):
    '''Handles errors in lattice initialization '''
    def __init__(self, name: str, msg: tp.Optional[str] =None) -> tp.NoReturn :
        if msg is None:
            msg = 'Error in lattice initialization: %s' % name
        super().__init__(msg)

class LoadError(Exception):
    '''Handles errors in loading parameters from file '''
    def __init__(self, name: str, msg: tp.Optional[str] =None) -> tp.NoReturn:
        if msg is None:
            msg = 'Error in loading simulation parameters: %s' % name
        super().__init__(msg)

class OptionError(Exception):
    '''Handles errors in options'''
    def __init__(self, name: str, msg: tp.Optional[str] =None) -> tp.NoReturn:
        if msg is None:
            msg = 'Error in option: %s' % name
        super().__init__(msg)
