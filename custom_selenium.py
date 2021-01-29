""" custom selenium object that handles all things"""
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumBrowser(webdriver.Firefox):
    """selenium webdriver extension with custom functions to extract
    data from facebook"""

    def __init__(self, firefox_path):
        """ Init selenium browser """
        print("Loading browser...")
        super().__init__(
            executable_path="./geckodriver",
            firefox_profile=webdriver.FirefoxProfile(firefox_path),
        )

    @staticmethod
    def remove_newlines(str_input):
        return re.sub(r"\n|\r", " ", str_input)

    def expand_results(self):
        """ expands search results by scrolling down 5 times """
        print("--scrolling down for more results...")
        body = self.find_element_by_tag_name("body")
        for _ in range(7):
            body.send_keys("webdriver" + Keys.END)
            time.sleep(7)

    def click_see_more_buttons(self):
        """ click all the "See more" buttons """
        print("--clicking 'See more' buttons...")
        body = self.find_element_by_tag_name("body")
        see_more_buttons = self.find_elements_by_xpath(
            "//*[contains(text(), 'See more')]"
        )

        # the 'see more' button needs to first be scrolled into view
        # usually we scroll it to center, but we can't do that
        # for the one on top so we click the home key
        body.send_keys("webdriver" + Keys.HOME)

        for button in see_more_buttons:
            try:

                # this is the only method that works
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

    def facebook_parse(self, url, keyword):
        """ go through a facebook group page's search results page and return the output"""

        print(f"Searching for '{keyword}' in '{url}'...")

        keyword_results = []

        try:

            # Open the page
            self.get(url + "?sorting_setting=CHRONOLOGICAL")

            self.expand_results()
            self.click_see_more_buttons()

            # get all posts
            print("--grabbing all posts...")
            posts = self.find_elements_by_css_selector(
                "div[role='article'][aria-posinset]"
            )

            # [role='article']
            # publisher - h2 strong
            # post - [data-ad-comet-preview='message']

            for post in posts:

                try:
                    publisher = post.find_element_by_css_selector("h2 a").get_attribute(
                        "innerText"
                    )

                    content_raw = post.find_element_by_css_selector(
                        "[data-ad-comet-preview='message']"
                    ).get_attribute("innerText")

                    # only add post if the keyword is mentioned in it
                    if keyword in content_raw.lower():

                        content = self.remove_newlines(content_raw)
                        keyword_results.append(publisher + " | " + content)

                except Exception as error:
                    post_text = self.remove_newlines(post.get_attribute("innerText"))
                    if len(post_text) > 20:
                        print(
                            f"----unable to get post with inner text '{post_text[:20]}...'. Error message: {error}"
                        )

            return keyword_results

        except Exception as error:
            print(
                f"ERROR - Something went wrong while processing '{keyword}' in '{url}'. {error}"
            )

        return keyword_results
