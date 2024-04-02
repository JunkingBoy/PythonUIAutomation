import pytest
import time

from selenium.webdriver.common.by import By
from typing import Any, Dict
from src.tools import Tools

temp_tools_elem: object = Tools()

class Test:
    def test_login(self, webdriver: object, config: Dict[str, Any]) -> None:
        url: str = config["Arguments"]["url"]
        webdriver.get(url)

    def test_login_button(self, webdriver: object, config: Dict[str, Any]) -> None:
        input_username_box: str = config["Arguments"]["Login_Arguments"]["input_username"]
        input_password_box: str = config["Arguments"]["Login_Arguments"]["input_password"]
        username: str = config["Account"]["username"]
        password: str = config["Account"]["password"]
        login_button: str = config["Arguments"]["Login_Arguments"]["login_button"]
        elem_list: list[str] = [input_username_box, input_password_box, login_button]
        get_elements = temp_tools_elem.wait_elem_appear(webdriver, elem_list)
        if get_elements:
            get_elements[0].send_keys(username)
            get_elements[1].send_keys(password)
            get_elements[2].click()
        else:
            print("Error: get_elements is none")

    def test_change_language(self, webdriver: object, config: Dict[str, Any]) -> None:
        language: str = config["Buy"]["language"]
        english_language: str = config["Buy"]["english_Language"]
        elem_list: list[str] = [language, english_language]
        get_elements = temp_tools_elem.wait_elem_appear(webdriver, elem_list)
        if get_elements:
            get_elements[0].click()
            get_elements[1].click()
        else:
            print("Error: get_elements is none")
        
    def test_add(self, webdriver: object, config: Dict[str, Any]) -> None:
        potato: str = config["Buy"]["potato"]
        option: str = config["Buy"]["option"]
        close: str = config["Buy"]["close"]
        add: str = config["Buy"]["add_to_car"]
        to_buy_car: str = config["Buy"]["buy_car"]
        select: str = config["Buy"]["select"]
        continue_button: str = config["Buy"]["continue"]
        elem_list: list[str] = [potato, option, close, add, to_buy_car, select, continue_button]
        get_elements = temp_tools_elem.wait_elem_appear(webdriver, elem_list)
        if len(get_elements) == 7:
            get_elements[0].click()
            webdriver.implicitly_wait(5)
            get_elements[1].click()
            webdriver.execute_script("window.scrollBy(0, 800);")
            get_elements[2].click()
            get_elements[3].click()
            get_elements[4].click()
            get_elements[5].click()
            webdriver.execute_script("window.scrollBy(0, 800);")
            get_elements[6].click()
        else:
            print("Error: get_elements is none")

    def test_save_after(self, webdriver: object, config: Dict[str, Any]) -> None:
        select_addr: str = config["After_Order"]["select_address"]
        select_button: str = config["After_Order"]["select_button"]
        last_button: str = config["After_Order"]["last_button"]
        elem_list: list[str] = [select_addr, select_button, last_button]
        get_elements = temp_tools_elem.wait_elem_appear(webdriver, elem_list)
        if len(get_elements) == 3:
            webdriver.execute_script("window.scrollBy(0, -1500);")
            get_elements[0].click()
            get_elements[1].click()
            webdriver.execute_script("window.scrollBy(0, 1000);")
            get_elements[2].click()
        else:
            print("Error: get_elements is none")

    def test_pay_after(self, webdriver: object, config: Dict[str, Any]) -> None:
        payment_dian: str = config["Pay"]["pay_button"]
        fangshi_dian: str =config["Pay"]["zhifu_button"]
        pay_js_path: str = config["Pay"]["dian_button_js_path"]
        elem_list: list[str] = [payment_dian, fangshi_dian, pay_js_path]
        get_elements = temp_tools_elem.wait_elem_appear(webdriver, elem_list)
        if len(get_elements) == 3:
            get_elements[0].click()
            get_elements[1].click()
            webdriver.execute_script("window.scrollBy(0, 1000);")
            get_elements[2].click()
        else:
            print("Error: get_elements is none")