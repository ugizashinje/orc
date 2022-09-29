import logging
from enum import Enum


def fullname(obj):
    klass = object.__class__
    module = klass.__module__
    if module == 'builtins':
        return klass.__qualname__ # avoid outputs like 'builtins.str'
    return module + '.' + klass.__qualname__

mapping = dict()

class Handle:
    def __init__(self, message):
        self.logger = logging.getLogger(__name__)
        self.logger = logging.getLogger(__name__)
        self.message = message
        self.actor = None

    def __call__(self, cls):
        if self.message is None:
            raise SystemExit(f"Actor {self} does not define message property")
        if self.actor is None:
            self.actor = cls
            mapping[f'{self.message.__module__}.{self.message.__name__}'] = cls
            self.logger.debug(f'Imported actor class {cls.__name__} to process message {self.message.__name__}')
        return cls # applied at class lever, should return class


class Step:
    def __init__(self,
                 timeout=None,
                 on_timeout=None,
                 ):
        self.logger = logging.getLogger(__name__)
        self.timeout=timeout
        self.on_timeout=on_timeout

    def __call__(self, func):
        return StepFunction(func, self)


class Delay(Enum):
    NONE = 0
    ONE = 1
    FIVE = 5
    FIFTEEN = 15
    THIRTY = 30
    MINUTE = 60
    FIVE_MINUTES = 5 * 60
    FIFTEEN_MINUTES = 15 * 60
    HOUR = 60 * 60


class StepFunction:
    def __init__(self, func, step):
        self.logger = logging.getLogger(__name__)
        self.func = func
        self.step = step

    def __call__(self):
        res = self.func(self)
        return res


class Actor:
    def __init__(self, request):
        pass

