"""returns alerts based on input json"""
import selenium
from errors import JsonError
from custom_selenium import SeleniumBrowser


def get_alerts(input_json):
    """main script"""
    total_results = []

    try:

        if "alerts" not in input_json:
            raise JsonError("'alerts' key not found.")

        if "firefox_profile_path" not in input_json:
            raise JsonError("'firefox_profile_path' key not found.")

        # initiate the Selenium-controlled browser
        browser = SeleniumBrowser(input_json["firefox_profile_path"])

        for alert_trigger in input_json["alerts"]:

            if "url" not in alert_trigger:
                raise JsonError("'url' key not found.")

            url = alert_trigger["url"]

            if "keywords" not in alert_trigger:
                raise JsonError("'keyword' key not found.")

            keywords = alert_trigger["keywords"]

            url_results = []

            for keyword in keywords:

                keyword_results = browser.facebook_parse(url=url, keyword=keyword)

                if len(keyword_results) > 0:
                    url_results.append(
                        {"keyword": keyword, "keyword_results": keyword_results}
                    )

            if len(url_results) > 0:
                total_results.append({"url": url, "url_results": url_results})

        browser.quit()

        return total_results

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

    return total_results