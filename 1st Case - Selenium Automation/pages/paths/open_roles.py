from selenium.webdriver.common.by import By


class OpenRolesPaths:
    EXTEND_ROLE_BUTTON = (By.XPATH, "//*[contains(text(), 'See all teams')]")
    EXPLORE_OPEN_ROLES_TEXT = (By.XPATH, "//*[contains(text(), 'Explore open roles')]")
    OPEN_POSITIONS_BUTTON = (
        By.XPATH,
        "//div[@data-department='{department_name}']/div/a",
    )
