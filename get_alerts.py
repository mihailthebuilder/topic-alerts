"""returns alerts based on input json"""
from errors import JsonError
from selenium_browser import SeleniumBrowser


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

            print(f"Accessing URL: {url} ...")
            browser.get(url + "?sorting_setting=CHRONOLOGICAL")

            browser.expand_results()
            browser.click_see_more_buttons()

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

    except Exception as error:
        print(f"ERROR - Something went wrong.\n'{error}'")

    return total_results


def count_alerts(alerts):
    """ counts number of results """
    count = 0
    for url in alerts:
        url_results = url["url_results"]
        for keyword in url_results:
            count += len(keyword["keyword_results"])
    return count
