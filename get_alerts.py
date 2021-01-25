"""returns alerts based on input json"""
from request_wrapper import request_wrapper


def get_alerts(input_json):
    """see main docstring"""

    alerts = []

    if "alerts" not in input_json:
        print("Error: No 'alerts' key in input.json")

    else:

        for alert_trigger in input_json["alerts"]:
            keyword = alert_trigger["keyword"]

            for url in alert_trigger["links"]:

                response = request_wrapper(url)

                if response == False:

                    print(keyword, url)

        return alerts
