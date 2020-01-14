from abc import ABC, abstractmethod
import re

class Condition(ABC):
    @abstractmethod
    def is_attained(self, sent):
        pass


class ConditionArray:
    def __init__(self, conds):
        self.conditions = conds
    @abstractmethod
    def are_all_attained(self, sent):
        a = True
        for cond in self.conditions:
            a = a and cond.is_attained(sent)
        return a


class ConditionEndsWith(Condition):
    def __init__(self, ending):
        self.end = ending
    def is_attained(self, sent):
        return re.match(self.end + "$", sent) is not None
