from selenium.webdriver.common.by import By


class RoleDetailsPagePaths:
    HEADLINE_SECTION = (
        By.XPATH,
        "//div[contains(@class, 'section')]/div[@class='posting-headline']/h2[text()='{job_title}']",
    )
    APPLY_BUTTON = (By.XPATH, "//a[contains(text(), 'apply for this job')]")
    JOB_DESCRIPTION = (By.XPATH, "//div[@data-qa='job-description']")
