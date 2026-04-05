from .main_actions import MainActions
from ..paths import RoleApplicationPaths as PATH

from selenium.webdriver.support import expected_conditions as EC
from src.logger import logger


class RoleApplicationPage(MainActions):

    def wait_until_main_blocks_are_loaded(self):
        logger.info(
            "Waiting until all main blocks are loaded for Role Application Page"
        )
        for path in [
            PATH.APPLY_BUTTON,
            PATH.FULL_NAME_SECTION,
            PATH.EMAIL_SECTION,
            PATH.PHONE_SECTION,
            PATH.LINKEDIN_URL_SECTION,
        ]:
            self._wait(timeout=20).until(EC.visibility_of_element_located(path))
            logger.info(f"{path[1]} is loaded")
