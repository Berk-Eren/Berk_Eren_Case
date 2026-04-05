from selenium.webdriver.common.by import By


class RoleApplicationPaths:
    APPLY_BUTTON = (
        By.XPATH,
        "//form[@id='application-form']//button[@id='btn-submit']",
    )
    FULL_NAME_SECTION = (
        By.XPATH,
        "//form[@id='application-form']//div[text()='Full name']",
    )
    EMAIL_SECTION = (By.XPATH, "//form[@id='application-form']//div[text()='Email']")
    PHONE_SECTION = (By.XPATH, "//form[@id='application-form']//div[text()='Phone ']")
    LINKEDIN_URL_SECTION = (
        By.XPATH,
        "//form[@id='application-form']//div[text()='LinkedIn URL']",
    )
