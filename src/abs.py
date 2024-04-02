from typing import Any, Dict
from abc import ABC, abstractmethod

class AbsTools(ABC):
    @abstractmethod
    def check_and_load(self, path: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def wait_elem_appear(self, webdriver: object, elem_list: list[str]) -> bool:
        pass