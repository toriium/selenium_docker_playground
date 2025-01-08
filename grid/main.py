from grid.get_driver import get_driver, Browser


def main():
    browser = Browser.CHROME
    stk = get_driver(browser=browser)

    stk.goto("https://www.google.com/")

    print()

    stk.quit()

if __name__ == '__main__':
    main()