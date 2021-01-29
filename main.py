"""main script"""
import json
from alerts import Alerts


def main():
    """main script"""
    print("----STARTED TOPIC ALERTS----")

    try:
        print("Loading input.json...")

        with open("input.json", "r") as input_file:
            input_json = json.load(input_file)

        alerts = Alerts(input_json)

        print(f"\n{alerts.count()} matches were found.")

        if len(alerts.results) > 0:
            alerts.email()

    except FileNotFoundError:
        print("ERROR - Unable to find 'input.json' file in the current directory.")
    except json.decoder.JSONDecodeError:
        print("ERROR - 'input.json' contents aren't JSON.")

    print("----FINISHED TOPIC ALERTS----")


if __name__ == "__main__":
    main()
