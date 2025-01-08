from webdriver_manager.chrome import ChromeDriverManager


def get_latest_driver_path() -> str:
    latest_driver_path = ChromeDriverManager().install()
    return latest_driver_path