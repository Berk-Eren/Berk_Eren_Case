from .main_actions import MainActions
from ..paths import RoleDetailsPagePaths as PATH

from selenium.webdriver.support import expected_conditions as EC

from src.logger import logger


class RoleDetailsPage(MainActions):

    def wait_until_main_blocks_are_loaded(self, job_title: str):
        logger.info("Waiting until all main blocks are loaded for Role Details Page")

        path_type, path = PATH.HEADLINE_SECTION
        self._wait(timeout=15).until(
            EC.visibility_of_element_located(
                (path_type, path.format(job_title=job_title))
            )
        )
        self._wait(timeout=15).until(
            EC.visibility_of_element_located(PATH.JOB_DESCRIPTION)
        )
        self._wait(timeout=15).until(
            EC.visibility_of_element_located(PATH.APPLY_BUTTON)
        )

    def click_on_apply_button(self):
        logger.info("Clicking on apply button on Role Details Page")

        elements = self.driver.find_elements(*PATH.APPLY_BUTTON)
        header_apply_button = elements[0]  # Select the first 'Apply' button

        job_application_url = header_apply_button.get_attribute("href")

        logger.info(f"Job application URL is {job_application_url}")

        header_apply_button.click()

        self.current_url_equals_to(job_application_url)
