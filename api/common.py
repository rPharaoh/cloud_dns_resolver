# common.py
from abc import ABC, abstractmethod


class APIBase(ABC):
    @abstractmethod
    def available_zones(self):
        pass

    @abstractmethod
    def resolve(self, domain_name, zone_id):
        pass

    @abstractmethod
    def query(self, domain_name):
        pass
