import inspect
import logging
import types
from abc import ABC, abstractmethod
from enum import Enum
import orchestrator.models

mappingMessages = dict()
mappingRequests = {
    orchestrator.models.Server.__name__: (orchestrator.models.Server, orchestrator.models.ServerRequest),
    orchestrator.models.CloudService.__name__: (orchestrator.models.CloudService, orchestrator.models.CloudServiceRequest)
}

def fullname(obj):
    klass = object.__class__
    module = klass.__module__
    if module == 'builtins':
        return klass.__qualname__ # avoid outputs like 'builtins.str'
    return module + '.' + klass.__qualname__


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
            mappingMessages[f'{self.message.__module__}.{self.message.__name__}'] = cls
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
        self.kargs = (karg for karg in inspect.signature(func).parameters)

    def __call__(self, actor, **kwargs):
        filtered_kwargs ={k: kwargs[k] for k in self.kargs if kwargs.get(k)}
        res = self.func(actor, **filtered_kwargs)
        return res


    def __get__(self, instance, cls=None):
        """
        Wraps the function with 'self'
        :param instance:
        :param cls:
        :return:
        """
        if instance is None:
            func = self.func
            if not hasattr(func, "__call__"):
                self.func = func.__get__(None, cls)
            return self
        else:
            return types.MethodType(self, instance)


class Actor(ABC):
    COMPLETED = 'completed'

    def __init__(self):
        self.data = dict()
        self.input = dict()
        self.context = dict()
        self.main_object = None

    @abstractmethod
    def first_step(self):
        pass

    def before_all(self):
        pass

    def before_step(self):
        pass

    def next(self, func, delay=Delay.NONE):
        return (func, delay)

