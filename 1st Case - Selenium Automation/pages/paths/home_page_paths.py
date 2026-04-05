from selenium.webdriver.common.by import By


class HomePagePaths:
    HEADER_DIV = (By.XPATH, "//header[@id='navigation']/div[@class='header-wrapper']")
    HOMEPAGE_MAIN_INFO = (
        By.XPATH,
        "//main[@class='flexible-layout']/section[@class='homepage-hero']",
    )
    HOMEPAGE_DIFFERENTIATORS = (
        By.XPATH,
        "//main[@class='flexible-layout']/section[@class='homepage-core-differentiators__style-2']",
    )
