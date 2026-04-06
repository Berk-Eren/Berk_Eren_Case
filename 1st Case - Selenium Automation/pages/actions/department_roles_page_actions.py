from .main_actions import MainActions
from ..paths import DepartmentRolePagePaths as PATH

from selenium.webdriver.support import expected_conditions as EC

from src.logger import logger


class DepartmentRolesPage(MainActions):

    def get_list_of_job_openings(self):
        logger.info("Getting list of job openings")

        elements = self.driver.find_elements(*PATH.JOB_POSTINGS)

        job_titles = [el.text for el in elements]

        logger.info(f"There are {len(job_titles)} number of jobs")

        return job_titles

    def click_on_apply_by_title(self, title: str):
        logger.info(f"Applying for job {title}")

        apply_button_element = self.driver.find_element(
            PATH.JOB_POSTING_BY_TITLE[0],
            PATH.JOB_POSTING_BY_TITLE[1].format(job_name=title),
        )
        url_element = self.driver.find_element(
            PATH.JOB_POSTING_URL_BY_TITLE[0],
            PATH.JOB_POSTING_URL_BY_TITLE[1].format(job_name=title),
        )

        selected_role_link = url_element.get_attribute("href")
        logger.info(f"Role link is {selected_role_link}")

        apply_button_element.click()

        self.current_url_equals_to(selected_role_link)

    def set_location(self, location: str):
        logger.info(f"Setting job location as {location}")

        location_bar_element = self._wait(30).until(
            EC.visibility_of_element_located(PATH.LOCATION_FILTER_BAR)
        )
        location_bar_element.click()

        location_elements = location_bar_element.find_elements("xpath", "div/ul/li/a")

        for ele in location_elements:
            if location in ele.text:
                ele.click()
                break
        else:
            error_message = f"A location with '{location}' couldn't be found on list"
            logger.error(error_message)

            raise Exception(error_message)

    def is_department_name_equals_to(self, department_name: str):
        logger.info(f"Checking whether department name equals to {department_name}")

        self.ensure_given_element_has_expected_text_value(
            PATH.DROPDOWN_DEPARTMENTS_SELECTED_VALUE, department_name.upper()
        )

    def is_each_roles_location_equals_to(self, location: str):
        logger.info(f"Checking whether each role located in {location}")
        location = location.upper()

        posts_categories = self.driver.find_elements(*PATH.POSTING_CATEGORIES)
        posts_location = [
            el.find_element("xpath", "span[contains(@class, 'location')]").text
            for el in posts_categories
        ]

        non_location_indices = list(
            [ind for ind, po_lo in enumerate(posts_location) if po_lo != location]
        )

        try:
            assert len(non_location_indices) == 0
        except Exception as e:
            error_msg = (
                f"Not all job's location is '{location}'\n"
                "Following jobs: \n"
                "\n".join(
                    [
                        posts_categories[ind]
                        .find_element("xpath", "parent::div/preceding-sibling::h5")
                        .text
                        + " "
                        + posts_location[ind]
                        for ind in non_location_indices
                    ]
                )
            )
            logger.error(error_msg)
            raise AssertionError(error_msg)
