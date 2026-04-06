import time
from functools import partial

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.logger import logger


class MainActions:

    def __init__(self, *, driver):
        self.driver = driver
        self.driver.implicitly_wait(15)
        self._wait = partial(WebDriverWait, self.driver)

    def current_url_equals_to(self, url: str):
        logger.info(f"Checking whether current url equals to {url}")
        try:
            self._wait(20).until(EC.url_to_be(url))
        except Exception as e:
            error_msg = f"Expected URL: {url}\nCurrent URL: {self.driver.current_url}"

            logger.error(error_msg)
            raise AssertionError(error_msg)

    def ensure_given_element_has_expected_text_value(
        self, path: tuple[str, str], expected_text_value: str
    ):
        logger.info(
            f"Ensuring whether given element '{path[1]}' has expected text value '{expected_text_value}'"
        )
        element = self.driver.find_element(*path)

        assert (
            element.text == expected_text_value
        ), f"For element {path[1]} expected text value is '{expected_text_value}', but actual value is {element.text}."

    def ensure_given_text_exists(self, text: str):
        logger.info(f"Ensuring given text '{text}' exists on page")
        self.driver.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")

    def wait_until_page_is_fully_loaded(self):
        logger.info(f"Waiting the page is fully loaded")

        self._wait(timeout=15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        logger.info(f"Page is fully loaded")

    def go_to_url(self, url: str = None):
        logger.info(f"Going to the URL '{url}'")

        self.driver.get(url)
        self.current_url_equals_to(url)
