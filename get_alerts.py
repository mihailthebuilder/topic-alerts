"""returns alerts based on input json"""
import errors
from selenium import webdriver


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

    except Exception as error:
        print(f"Error - Something went wrong with Selenium.\nMessage: '{error}'")

    return alerts


def parse_site(browser, url, keyword):
    """uses Selenium to go through a website and check for keywords"""
    return False
