import pytest
import random

from src.helpers import build_url
from src.constants import BASE_URL, JOB_SEARCH_SITE

from urllib.parse import urlencode, urlparse


@pytest.mark.parametrize(
    "department_name, city", [("Quality Assurance", "Istanbul, Turkiye")]
)
def test_check_open_roles_under_given_department(
    driver,
    home_page,
    open_roles_page,
    department_role_page,
    role_details_page,
    role_application_page,
    department_name,
    city,
):
    driver.get(BASE_URL)  # main page

    # Go to main page and switch to careers URL
    home_page.wait_until_main_blocks_are_loaded()
    home_page.go_to_url(build_url(BASE_URL, path="careers/#open-roles"))

    # Ensure main elements are loaded and go to roles on 'Quality Assurance' department
    open_roles_page.wait_until_page_is_fully_loaded()
    open_roles_page.ensure_given_text_exists(text="Explore open roles")
    open_roles_page.show_all_teams()
    open_roles_page.go_to_given_department_positions(department_name=department_name)

    # Click on 'Apply' button of selected job
    department_role_page.set_location(city)
    department_role_page.is_department_name_equals_to(department_name)
    department_role_page.is_each_roles_location_equals_to(city)

    # Get list of jobs and select one of them by its title
    listed_job_openings: list = department_role_page.get_list_of_job_openings()
    random_job_title = random.choice(listed_job_openings)

    department_role_page.click_on_apply_by_title(random_job_title)

    # Ensure main elements are loaded under the page and click on 'Apply' button
    role_details_page.wait_until_main_blocks_are_loaded(random_job_title)
    role_details_page.click_on_apply_button()

    # Ensure main blocks are loaded on form page
    role_application_page.ensure_given_text_exists(text=random_job_title)
    role_application_page.wait_until_main_blocks_are_loaded()
