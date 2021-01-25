"""a wrapper for requests package to ensure access to site"""
import requests


def request_wrapper(url):
    """main script"""
    # add https if not in there at start
    if url[0:8] != "https://":
        url = "https://" + url

    try:
        my_session = requests.session()
        for_cookies = requests.get(url).cookies
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
        }

        response = my_session.get(url, headers=headers, cookies=for_cookies)
        return {"success": True, "data": response}

    except requests.exceptions.ConnectionError as error:
        return {
            "success": False,
            "data": f"An error occurred when trying to access the '{url}' URL. Error message: '{error}'",
        }