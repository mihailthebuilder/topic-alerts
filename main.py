"""main script"""
import json
from alerts import Alerts
from errors import JsonError


def main():
    """main script"""
    print("----STARTED TOPIC ALERTS----")

    try:
        print("Loading input.json...")

        with open("input.json", "r") as input_file:
            input_json = json.load(input_file)

        if "alerts" not in input_json:
            raise JsonError("'alerts' key not found.")

        if "firefox_profile_path" not in input_json:
            raise JsonError("'firefox_profile_path' key not found.")

        alerts = Alerts(
            alerts=input_json["alerts"], firefox_path=input_json["firefox_profile_path"]
        )

        print(f"\n{alerts.count()} matches were found.")

        if len(alerts.results) > 0:
            alerts.email(
                sender=input_json["gmail"]["sender"],
                receiver=input_json["gmail"]["receiver"],
            )

    except FileNotFoundError:
        print("ERROR - Unable to find 'input.json' file in the current directory.")
    except json.decoder.JSONDecodeError:
        print("ERROR - 'input.json' contents aren't JSON.")

    print("----FINISHED TOPIC ALERTS----")


if __name__ == "__main__":
    main()
