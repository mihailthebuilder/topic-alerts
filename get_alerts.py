"""returns alerts based on input json"""
from request_wrapper import request_wrapper
import errors


def get_alerts(input_json):
    """see main docstring"""

    alerts = []

    if "alerts" not in input_json:
        print("Error: No 'alerts' key in input.json")

    else:

        for alert_trigger in input_json["alerts"]:

            try:
                keyword = alert_trigger["keyword"]

                for url in alert_trigger["links"]:

                    response = request_wrapper(url)

                    if response["success"]:

                        print("success!")

                    else:
                        error_message = response["data"]
                        raise errors.AlertError(
                            f"Error: Unable to access {url}.\nMessage: {error_message}"
                        )

            except Exception as error:
                print(
                    f"Error: Something went wrong with processing the {keyword} alert.\nMessage: {error}"
                )

        return alerts
