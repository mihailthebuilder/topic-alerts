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
        print("--browser loaded.")

    def facebook_parse(self, url, keyword):
        """ go through a facebook group page and check  for results """

        print(f"Searching for '{keyword}' in '{url}'...")

        # Open the page
        self.get(url + "/search?q=" + keyword)
        time.sleep(4)

        # click for most recent results
        self.find_element_by_css_selector("input[aria-label='Most recent']").click()
        time.sleep(4)

        # press end key 4 times
        body = self.find_element_by_tag_name("body")
        for _ in range(4):
            print("--scrolled to page end to load more content")
            body.send_keys("webdriver" + Keys.END)
            time.sleep(4)

        # click all the "See more" buttons

        keyword_results = []

        try:

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
                f"Something went wrong while processing '{keyword}' in '{url}'. Message : {error}"
            )

        return keyword_results