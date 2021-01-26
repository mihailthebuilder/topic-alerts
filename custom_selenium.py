""" custom selenium object that handles all things"""
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class SeleniumBrowser(webdriver.Firefox):
    def __init__(self, firefox_path):
        """ Init selenium browser """
        print("Loading browser...")
        super().__init__(
            executable_path="./geckodriver",
            firefox_profile=webdriver.FirefoxProfile(firefox_path),
        )

    def facebook_parse(self, url, keyword):
        """ go through a facebook group page's search results page and return the output"""

        print(f"Searching for '{keyword}' in '{url}'...")

        keyword_results = []

        try:

            # Open the page
            self.get(url + "/search?q=" + keyword)
            time.sleep(4)

            # click for most recent results
            print("--clicking 'Most recent' button...")
            self.find_element_by_css_selector("input[aria-label='Most recent']").click()
            time.sleep(4)

            # press end key 4 times
            print("--expanding results...")
            body = self.find_element_by_tag_name("body")
            for _ in range(5):
                body.send_keys("webdriver" + Keys.END)
                time.sleep(5)

            # click all the "See more" buttons
            print("--clicking 'See more' buttons...")
            see_more_buttons = self.find_elements_by_xpath(
                "//*[contains(text(), 'See more')]"
            )
            for button in see_more_buttons:
                try:
                    # is actually correct
                    scroll_to_middle_script = (
                        "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);"
                        + "var elementTop = arguments[0].getBoundingClientRect().top;"
                        + "window.scrollBy(0, elementTop-(viewPortHeight/2));"
                    )
                    self.execute_script(scroll_to_middle_script, button)
                    time.sleep(2)
                    button.click()
                except Exception:
                    print("----unable to click 'See more' button")
            time.sleep(15)

            """
            posts = self.driver.find_elements_by_tag_name(2)

            for post in posts:
                post_text = post.get_attribute("innerText")
                if keyword in post_text.lower():
                    print(post_text)
                    keyword_results.append(post_text)
            """
            return keyword_results

        except Exception as error:
            print(
                f"ERROR - Something went wrong while processing '{keyword}' in '{url}'. {error}"
            )

        return keyword_results