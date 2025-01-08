import json

import yaml

from grid.browser import Browser


def get_browsers_versions() -> dict[Browser, list[str]]:
    browsers_path = "browsers.json"
    with open(browsers_path) as json_file:
        browsers = json.load(json_file)

    browsers_versions = dict()
    for browser_name, versions in browsers.items():
        browsers_versions[Browser(browser_name)] = []
        for version in versions["versions"]:
            browsers_versions[browser_name].append(version)

    return browsers_versions
