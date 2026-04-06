import os
import pytest

from selenium import webdriver
from datetime import datetime

from pages.actions import (
    OpenRolesPageActions,
    HomePageActions,
    DepartmentRolePage,
    RoleDetailsPage,
    RoleApplicationPage,
)
from src.constants import OUTPUT_FOLDER
from src.logger import logger


def pytest_addoption(parser):
    """
    Command line arguments
    """
    parser.addoption("--headless", help="Whether to run tests on headless mode or not.")
    parser.addoption(
        "--no-sandbox",
        action="store_true",
        help="Whether to run tests on headless mode or not.",
    )
    parser.addoption(
        "--driver",
        default="chrome",
        choices=["firefox", "chrome"],
        help="Type of driver to run.",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    To get screenshot at the end of the tests
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        try:
            os.makedirs(f"{OUTPUT_FOLDER}/screenshots", exist_ok=True)
            driver = item.funcargs["driver"]

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"{OUTPUT_FOLDER}/screenshots/screenshot_{item.name}_{timestamp}.png"

            driver.save_screenshot(file_name)
            print(f"\nScreenshot saved as: {file_name}")
        except Exception as e:
            print(f"Failed to take screenshot: {e}")


@pytest.fixture(scope="function")
def driver(request):
    if request.config.getoption("--driver") == "chrome":
        logger.info("Chrome browser is being selected by user")

        from selenium.webdriver.chrome.options import Options

        options = Options()
        driver_class = webdriver.Chrome
    elif request.config.getoption("--driver") == "firefox":
        logger.info("Firefox browser is being selected by user")

        from selenium.webdriver.firefox.options import Options

        options = Options()
        driver_class = webdriver.Firefox

    if request.config.getoption("--headless"):
        logger.info("Browser will be started in headless mode")
        options.add_argument("--headless")
    if request.config.getoption("--no-sandbox"):
        options.add_argument("--no-sandbox")

    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")

    logger.info("Starting the browser")
    driver = driver_class(options=options)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def home_page(driver):
    return HomePageActions(driver=driver)


@pytest.fixture(scope="function")
def open_roles_page(driver):
    return OpenRolesPageActions(driver=driver)


@pytest.fixture(scope="function")
def department_role_page(driver):
    return DepartmentRolePage(driver=driver)


@pytest.fixture(scope="function")
def department_role_page(driver):
    return DepartmentRolePage(driver=driver)


@pytest.fixture(scope="function")
def role_details_page(driver):
    return RoleDetailsPage(driver=driver)


@pytest.fixture
def role_application_page(driver):
    return RoleApplicationPage(driver=driver)
