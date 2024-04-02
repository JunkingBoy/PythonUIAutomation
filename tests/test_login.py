import pytest
import time

from selenium.webdriver.common.by import By
from typing import Any, Dict

class Test:
    def test_login(self, webdriver: object, config: Dict[str, Any]) -> None:
        url: str = config["Arguments"]["url"]
        webdriver.get(url)

        assert webdriver.current_url == url

    def test_login_button(self, webdriver: object, config: Dict[str, Any]) -> None:
        input_username_box: str = config["Arguments"]["Login_Arguments"]["input_username"]
        input_password_box: str = config["Arguments"]["Login_Arguments"]["input_password"]
        username: str = config["Account"]["username"]
        password: str = config["Account"]["password"]
        login_button: str = config["Arguments"]["Login_Arguments"]["login_button"]
        webdriver.find_element(By.XPATH, input_username_box).send_keys(username)
        webdriver.find_element(By.XPATH, input_password_box).send_keys(password)
        webdriver.find_element(By.XPATH, login_button).click()

        successfully_url: str = config["Arguments"]["Login_Arguments"]["login_success_url"]
        # 因为登录进行了跨域请求,所以使用显示等待
        time.sleep(5)
        assert webdriver.current_url == successfully_url

    def test_change_language(self, webdriver: object, config: Dict[str, Any]) -> None:
        language: str = config["Buy"]["language"]
        english_language: str = config["Buy"]["english_Language"]
        webdriver.find_element(By.XPATH, language).click()
        webdriver.find_element(By.XPATH, english_language).click()
        
    def test_add(self, webdriver: object, config: Dict[str, Any]) -> None:
        potato: str = config["Buy"]["potato"]
        webdriver.find_element(By.XPATH, potato).click()
        webdriver.implicitly_wait(5)
        option: str = config["Buy"]["option"]
        webdriver.find_element(By.XPATH, option).click()
        # 鼠标滚轮
        webdriver.execute_script("window.scrollBy(0, 800);")
        time.sleep(7)
        close: str = config["Buy"]["close"]
        webdriver.find_element(By.XPATH, close).click()
        add: str = config["Buy"]["add_to_car"]
        webdriver.find_element(By.XPATH, add).click()
        time.sleep(7)
        to_buy_car: str = config["Buy"]["buy_car"]
        webdriver.find_element(By.XPATH, to_buy_car).click()
        time.sleep(7)
        select: str = config["Buy"]["select"]
        webdriver.find_element(By.XPATH, select).click()
        time.sleep(7)
        webdriver.execute_script("window.scrollBy(0, 800);")
        time.sleep(7)
        continue_button: str = config["Buy"]["continue"]
        webdriver.find_element(By.XPATH, continue_button).click()
        time.sleep(7)

    def test_save_after(self, webdriver: object, config: Dict[str, Any]) -> None:
        webdriver.execute_script("window.scrollBy(0, -1500);")
        time.sleep(5)
        select_addr: str = config["After_Order"]["select_address"]
        webdriver.find_element(By.XPATH, select_addr).click()
        time.sleep(5)
        select_button: str = config["After_Order"]["select_button"]
        webdriver.find_element(By.XPATH, select_button).click()
        time.sleep(5)
        webdriver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(5)
        last_button: str = config["After_Order"]["last_button"]
        webdriver.find_element(By.XPATH, last_button).click()
        time.sleep(5)

    def test_pay_after(self, webdriver: object, config: Dict[str, Any]) -> None:
        payment_dian: str = config["Pay"]["pay_button"]
        webdriver.find_element(By.XPATH, payment_dian).click()
        time.sleep(5)
        fangshi_dian: str =config["Pay"]["zhifu_button"]
        button = webdriver.find_element(By.XPATH, fangshi_dian)
        webdriver.execute_script("arguments[0].click();",  button)
        time.sleep(5)
        pay_js_path: str = config["Pay"]["dian_button_js_path"]
        try:
            webdriver.execute_script(f"document.querySelector('{pay_js_path}').click();")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(10)