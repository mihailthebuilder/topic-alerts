""" checks whether json file in correct format """
import validators
import errors


def check_json(input_json):
    """main script"""
    try:
        alerts = input_json["alerts"]

        for trigger in alerts:

            keyword = trigger["keyword"]
            if len(keyword) <= 2:

                raise errors.JsonError(f"Keyword {keyword} too short.")

            for url in trigger["links"]:

                if not validators.url(url):
                    raise errors.JsonError(f"Incorrect URL: {url}")

    except KeyError as error:
        raise errors.JsonError(f"Incorrect JSON structure. Detailed message: {error}")
