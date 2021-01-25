"""main script"""
import json
from get_alerts import get_alerts


def main():
    """main script"""
    print("----STARTED TOPIC ALERTS----")

    try:
        with open("input.json", "r") as input_file:
            input_json = json.load(input_file)

            alerts = get_alerts(input_json)

            print(alerts)

    except FileNotFoundError:
        print("Error: Unable to find 'input.json' file in the current directory.")

    print("----FINISHED TOPIC ALERTS----")


if __name__ == "__main__":
    main()
