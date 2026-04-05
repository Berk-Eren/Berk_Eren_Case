import time

from .main_actions import MainActions
from ..paths import OpenRolesPaths as PATH

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

from src.logger import logger


class OpenRolesPageActions(MainActions):

    def show_all_teams(self):
        logger.info("Clicking on 'Show all teams' button")

        element = self.driver.find_element(*PATH.EXTEND_ROLE_BUTTON)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

        time.sleep(1)

        self._wait(
            timeout=20, ignored_exceptions=[ElementClickInterceptedException]
        ).until(EC.element_to_be_clickable(PATH.EXTEND_ROLE_BUTTON)).click()

    def go_to_given_department_positions(self, department_name: str):
        logger.info(f"Clicking on the department '{department_name}'")

        path_type, path = PATH.OPEN_POSITIONS_BUTTON
        path = path.format(department_name=department_name)

        self._wait(timeout=20).until(
            EC.text_to_be_present_in_element_attribute(
                (path_type, path), "href", "team="
            )
        )

        ele = self.driver.find_element(path_type, path)
        selected_department_url = ele.get_attribute("href")
        ele.click()

        self.current_url_equals_to(selected_department_url)
