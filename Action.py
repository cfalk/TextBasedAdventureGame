from importlib import import_module
from abc import ABC, abstractmethod


class ActionBuilder:
    def __init__(self, action_json):
        self.action_id = action_json.get("Id")
        module = import_module(action_json.get("Module"))
        self.classDefinition = getattr(module, action_json.get("ClassName"))

    def get_id(self):
        return self.action_id

    def build(self, **kwargs):
        return self.classDefinition(**kwargs)


class Action(ABC):
    description_id = "???"

    def __init__(self, **kwargs):
        self.stored_kwargs = kwargs or {}

    @abstractmethod
    def enact(self):
        pass