"""returns alerts based on input json"""
from errors import JsonError
from selenium_browser import SeleniumBrowser
from gmail_custom import GmailAlert


class Alerts:
    def __init__(self, alerts, firefox_path):
        total_results = []

        try:

            # initiate the Selenium-controlled browser
            browser = SeleniumBrowser(firefox_path)

            for alert_trigger in alerts:

                if "url" not in alert_trigger:
                    raise JsonError("'url' key not found.")

                url = alert_trigger["url"]

                if "keywords" not in alert_trigger:
                    raise JsonError("'keyword' key not found.")

                keywords = alert_trigger["keywords"]

                url_results = []

                browser.load_page(url)

                browser.expand_results()

                for keyword in keywords:

                    keyword_results = browser.facebook_parse(keyword=keyword)

                    if len(keyword_results) > 0:
                        url_results.append(
                            {"keyword": keyword, "keyword_results": keyword_results}
                        )

                if len(url_results) > 0:
                    total_results.append({"url": url, "url_results": url_results})

            browser.quit()

        except JsonError as error:
            print(error.message)

        except Exception as error:
            print(f"ERROR - Something went wrong.\n'{error}'")

        self.results = total_results

    def count(self):
        """ counts number of results """
        count = 0
        alerts = self.results
        for url in alerts:
            url_results = url["url_results"]
            for keyword in url_results:
                count += len(keyword["keyword_results"])
        return count

    def convert_to_email(self):
        """ converts self from json to subject and content needed in email """
        count = self.count()
        subject = f"Facebook alert -> {count} results"
        text = f"You have {count} results.\n\n"

        alerts = self.results

        for url_dict in alerts:

            url = url_dict["url"]
            url_results = url_dict["url_results"]

            text += f"================= URL: {url} ================\n\n\n"

            for keyword_dict in url_results:

                keyword = keyword_dict["keyword"]
                keyword_results = keyword_dict["keyword_results"]

                text += f"---- Keyword: {keyword} ----\n\n\n"

                for keyword_result in keyword_results:
                    text += keyword_result + "\n\n"

        return {"subject": subject, "text": text}

    def email(self, sender, receiver):
        """ sends email with results """

        email_content = self.convert_to_email()

        gm = GmailAlert()

        email_encoded = gm.create_message(
            sender=sender,
            to=receiver,
            subject=email_content["subject"],
            message_text=email_content["text"],
        )

        gm.send_message(message=email_encoded, user_id=sender)
