"""returns alerts based on input json"""
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from errors import JsonError


def get_alerts(input_json):
    """main script"""
    alerts = []

    try:

        if "alerts" not in input_json:
            raise JsonError("'alerts' key not found.")

        if "firefox_profile_path" not in input_json:
            raise JsonError("'firefox_profile_path' key not found.")

        # initiate the Selenium-controlled browser
        browser = selenium_browser(input_json["firefox_profile_path"])

        for alert_trigger in input_json["alerts"]:

            if "keyword" not in alert_trigger:
                raise JsonError("'keyword' key not found.")

            keyword = alert_trigger["keyword"]
            results = []

            if "links" not in alert_trigger:
                raise JsonError("'links' key not found.")

            for url in alert_trigger["links"]:

                result = parse_site(browser=browser, url=url, keyword=keyword)

                if result:
                    results.append(result)

            if len(results) > 0:
                alerts.append({"keyword": keyword, "results": results})

    except JsonError as error:
        print(error.message)

    except selenium.common.exceptions.NoSuchWindowException:
        print("ERROR - You closed the browser window that the script was using.")

    except selenium.common.exceptions.WebDriverException as error:
        print(
            f"ERROR - Something went wrong with Selenium and/or the browser it was using. Message: '{error}'"
        )

    except Exception as error:
        print(f"ERROR - Something went wrong.\nMessage: '{error}'")

    return alerts


def selenium_browser(path):
    """ retrieves selenium browser with the given profile path """
    print("Loading browser...")
    profile = webdriver.FirefoxProfile(path)
    return webdriver.Firefox(executable_path="./geckodriver", firefox_profile=profile)


def parse_site(browser, url, keyword):
    """uses Selenium to go through a website and check for keywords"""

    print(f"Searching for {keyword} in '{url}'...")

    # the statement shouldn't render any errors that aren't catched one level above
    browser.get(url)

    body = browser.find_element_by_tag_name("body")

    try:
        time.sleep(1)
        body.send_keys("webdriver" + Keys.END)
        time.sleep(2)
        body.send_keys("webdriver" + Keys.END)
        time.sleep(2)
    except Exception as error:
        print(error)
    return False


def scroll_down(self):
    """ A method for scrolling to the page bottom """

    # Get scroll height
    last_height = self.driverr