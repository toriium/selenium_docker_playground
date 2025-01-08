import os
from pathlib import Path

from stealthenium import stealth
from selenium import webdriver
from selenium_toolkit import SeleniumToolKit
import enum

from grid.browser import Browser
from grid.versions import get_browsers_versions, get_latest_version

USER_DATA_PATH = "/home/toriium/.config/google-chrome"
PROFILE_NAME = "Profile 1"
WEBDRIVER_URL = "http://localhost:4444/wd/hub"

BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEBDRIVER_DOWNLOAD_PATH = str(Path(f"{BASE_DIR}/webdriver_downloads"))


def get_driver(browser: Browser, browser_version: str = None, headless: bool = False,
               profile: bool = False, file_dir: str = None) -> SeleniumToolKit:
    use_stealth = False

    if not browser_version:
        browser_version = get_latest_version(browser=browser)

    browsers_versions = get_browsers_versions()
    if not browser_version in browsers_versions[browser]:
        raise ValueError(f"Browser {browser}:{browser_version} is not supported")

    if browser == Browser.CHROME:
        use_stealth = True
        options = webdriver.ChromeOptions()
        extra_capabilities = {
            "goog:loggingPrefs": {"performance": "ALL"},
            # "acceptInsecureCerts": True,
        }

    elif browser == Browser.FIREFOX:
        use_stealth = False
        options = webdriver.FirefoxOptions()
        extra_capabilities = {}

    else:
        raise ValueError(f"Unknown browser: {browser}")



    # Options
    options.browser_version = browser_version
    options.add_argument("--start-maximized")

    # SSL related
    # options.add_argument('ignore-certificate-errors')
    # options.add_argument('--ignore-ssl-errors=yes')
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--allow-insecure-localhost')
    # options.add_argument('--allow-running-insecure-content')

    # Save machine resources
    options.add_argument('--no-sandbox')  # Disable the sandbox for all software features
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-plugins')

    if headless:
        options.add_argument("--disable-gpu")  # GPU hardware acceleration isn't needed for headless
        # options.add_argument("--headless")
        options.headless = True

    # For now only works with chrome
    if profile:
        # Cant run more than one instance using the same profile
        # Don't work in places that need to be logged in chrome
        user_data_path = USER_DATA_PATH
        profile_name = PROFILE_NAME

        options.add_argument('--remote-debugging-port=9222')
        options.add_argument(f"--user-data-dir={user_data_path}")
        options.add_argument(f'--profile-directory={profile_name}')

    # For now only works with chrome
    if file_dir:
        download_path = str(Path(f'{WEBDRIVER_DOWNLOAD_PATH}/{file_dir}'))
        prefs = {"download.default_directory": download_path}
        options.add_experimental_option("prefs", prefs)

    capabilities = {
        "browserName": browser.value,
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVideo": False,  # Will record screen
            "enableVNC": True,
        }
    }

    capabilities.update(extra_capabilities)

    [options.set_capability(name=k, value=v) for k, v in capabilities.items()]

    driver = webdriver.Remote(command_executor=WEBDRIVER_URL, options=options)

    # Start Maximized for better analysis
    driver.maximize_window()

    # For now only works with chrome
    if use_stealth:
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

    stk = SeleniumToolKit(driver)
    stk.change_wait_time(range_time=(2, 3))

    return stk
