"""returns alerts based on input json"""
import time
import selenium
from selenium import webdriver
from errors import JsonError


def get_alerts(input_json):
    """main script"""
    alerts = []

    try:

        if "alerts" not in input_json:
            raise JsonError("'alerts' key not found.")

        if "chromeProfilePath" not in input_json:
            raise JsonError("'chromeProfilePath' key not found.")

        # initiate the Selenium-controlled browser
        browser = selenium_browser(input_json["chromeProfilePath"])

        for alert_trigger in input_json["alerts"]:

            if "keyword" not in alert_trigger:
                raise JsonError("'keyword' key not found.")

            keyword = alert_trigger["keyword"]
            results = []

            if "links" not in alert_trigger:
                raise JsonError("'links' key not found.")

            for url in alert_trigger["links"]:

                print(f"Searching for {keyword} in '{url}'...")
                result = parse_site(browser=browser, url=url, keyword=keyword)

                if result:
                    results.append(result)

            if len(results) > 0:
                alerts.append({"keyword": keyword, "results": results})

    except JsonError as error:
        print(error.message)

    except selenium.common.exceptions.NoSuchWindowException:
        print("ERROR - You closed the Chrome browser window that the script was using.")

    except selenium.common.exceptions.WebDriverException as error:
        print(
            f"ERROR - Something went wrong with Selenium and/or the browser it was using. Message: '{error}'"
        )

    except Exception as error:
        print(f"ERROR - Something went wrong.\nMessage: '{error}'")

    return alerts


def selenium_browser(path):
    """ retrieves selenium browser with the given chrome profile path """
    # tell selenium to access the right Chrome browser account
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=/home/jon/.config/google-chrome/")
    options.add_argument("profile-directory=Profile 3")
    return webdriver.Chrome(executable_path="./chromedriver", options=options)


def parse_site(browser, url, keyword):
    """uses Selenium to go through a website and check for keywords"""

    # the statement shouldn't render any errors that aren't catched one level above
    browser.get(url)

    try:
        time.sleep(5)
    except Exception as error:
        print(error)
    return False
