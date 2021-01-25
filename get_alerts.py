"""returns alerts based on input json"""
from selenium import webdriver
import selenium
import time


def get_alerts(input_json):
    """main script"""
    alerts = []

    try:
        browser = webdriver.Chrome("./chromedriver")

        for alert_trigger in input_json["alerts"]:
            keyword = alert_trigger["keyword"]
            results = []

            for url in alert_trigger["links"]:

                print(f"Searching for {keyword} in '{url}'...")
                result = parse_site(browser=browser, url=url, keyword=keyword)

                if result:
                    results.append(result)

            if len(results) > 0:
                alerts.append({"keyword": keyword, "results": results})

    except selenium.common.exceptions.NoSuchWindowException:
        print("ERROR - You closed the Chrome browser window that the script was using.")

    except selenium.common.exceptions.WebDriverException:
        print("ERROR - You closed the Chrome browser that the script was using.")

    except KeyError as error:
        print(f"ERROR - Something went wrong.\nMessage: '{error}'")

    return alerts


def parse_site(browser, url, keyword):
    """uses Selenium to go through a website and check for keywords"""

    browser.get(url)
    time.sleep(5)
    return False
