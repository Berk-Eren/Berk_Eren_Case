from .main_actions import MainActions
from ..paths import HomePagePaths as PATH

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.logger import logger


class HomePageActions(MainActions):
    def wait_until_main_blocks_are_loaded(self):
        logger.info(f"Waiting until all main blocks are loaded for Home Page")

        self._wait(timeout=10).until(EC.visibility_of_element_located(PATH.HEADER_DIV))
        self._wait(timeout=10).until(
            EC.visibility_of_element_located(PATH.HOMEPAGE_DIFFERENTIATORS)
        )
        self._wait(timeout=10).until(
            EC.visibility_of_element_located(PATH.HOMEPAGE_MAIN_INFO)
        )
