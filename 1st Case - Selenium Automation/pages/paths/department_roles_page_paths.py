from selenium.webdriver.common.by import By


class DepartmentRolePagePaths:
    JOB_POSTINGS = (By.XPATH, "//div[@class='posting']//h5[@data-qa='posting-name']")
    JOB_POSTING_URL_BY_TITLE = (
        By.XPATH,
        "//a[@class='posting-title']/descendant-or-self::*[text()='{job_name}']/parent::a",
    )
    JOB_POSTING_BY_TITLE = (
        By.XPATH,
        "//a[@class='posting-title']/descendant-or-self::*[text()='{job_name}']",
    )
    JOB_APPLY_BUTTON = (By.XPATH, "//a[text()='Apply']")
    DROPDOWN_DEPARTMENTS_SELECTED_VALUE = (
        By.XPATH,
        "//div[@class='filter-bar']/div[@role='button' and contains(@aria-label, 'Filter by Team:')]/div[contains(@class, 'has-selected-filter')]",
    )
    POSTING_CATEGORIES = (
        By.XPATH,
        "//div[@class='posting-categories']",
    )
    LOCATION_FILTER_BAR = (
        By.XPATH,
        "//div[@class='filter-bar']/div[@role='button' and contains(@aria-label, 'Filter by Location:')]",
    )
