from selenium import webdriver

class Chrome_test:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()

    def browser(self) -> object:
        return self.driver
    
    def __del__(self) -> None:
        self.driver.quit()