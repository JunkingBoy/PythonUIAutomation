import os
import yaml
from typing import Any, Dict, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException

from .abs import AbsTools

class Tools(AbsTools):
    def check_and_load(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            return "File not found: {}".format(path)
        else:
            try:
                with open(path, "r") as config_file:
                    config: Dict[str, Any] = yaml.safe_load(config_file)
                return config
            except yaml.YAMLError as e:
                return f"Error loading Yaml file: {e}"
            
    def wait_elem_appear(self, webdriver: object, elem_list: list[str] = []) -> Optional[list[WebElement]]:
        if elem_list:
            # 推导式
            temp_elem_tuple_list: list[tuple] = [(By.XPATH, item) for item in elem_list]
            wait: object = WebDriverWait(webdriver, timeout=10)
            result_elements: list[WebElement] = []
            for locator in temp_elem_tuple_list:
                try:
                    element = wait.until(EC.visibility_of_element_located(locator))
                    result_elements.append(element)
                except TimeoutException:
                    print("TimeOut!")
                    pass
            return result_elements
        return None