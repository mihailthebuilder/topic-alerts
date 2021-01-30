""" custom selenium object that handles all things"""
import time
from functions import remove_newlines
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

    def load_page(self, url):
        """ Go to Facebook page and wait until posts are loaded """
        print(f"Opening URL: {url} ...")
        load_url = url + "?sorting_setting=CHRONOLOGICAL"
        self.get(load_url)

        print("--waiting for posts to load...")
        WebDriverWait(self, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "[data-pagelet='DiscussionRootSuccess']")
            )
        )
        time.sleep(6)

    def expand_results(self):
        """ expands search results by scrolling down 5 times """
        # you need to click the "See more" buttons/links
        # every time before you move to another section of the web page
        # when go past that section, Facebook's website hides the posts
        # and Selenium can't see them anymore
        self.click_see_more_buttons()
        body = self.find_element_by_tag_name("body")
        for _ in range(7):
            print("--scrolling down for more results...")
            body.send_keys("webdriver" + Keys.END)
            time.sleep(10)
            self.click_see_more_buttons()

    def click_see_more_buttons(self):
        """ click all the "See more" buttons """
        see_more_buttons = self.find_elements_by_xpath(
            "//*[contains(text(), 'See more')]"
        ) + self.find_elements_by_xpath("//*[contains(text(), 'See More')]")

        for button in see_more_buttons:
            try:
                print("----clicking 'See more' button...")

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
                print("------unable to click 'See more' button")

    def facebook_parse(self, keyword):
        """ go through a facebook group page's search results page and return the output"""

        keyword_results = []

        try:

            # get all posts
            print(f"--grabbing all posts with the keyword '{keyword}'...")
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
                        "div[dir='auto']"
                        # "[data-ad-comet-preview='message']"
                    ).get_attribute("innerText")

                    # only add post if the keyword is mentioned in it
                    if keyword.lower() in content_raw.lower():

                        content = remove_newlines(content_raw)
                        keyword_results.append(publisher + " | " + content)

                except Exception as error:
                    post_text_raw = post.get_attribute("innerText")
                    if isinstance(post_text_raw, str) and len(post_text_raw) > 20:
                        post_text = remove_newlines(post_text_raw)
                        print(
                            f"----unable to get post with inner text '{post_text[:20]}...'. Error message: {error}"
                        )

            return keyword_results

        except Exception as error:
            print(
                f"ERROR - Something went wrong while processing keyword '{keyword}'. {remove_newlines(error)}"
            )

        return keyword_results
