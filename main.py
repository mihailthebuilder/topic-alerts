"""main script"""
import json
from get_alerts import get_alerts
from check_json import check_json
from errors import JsonError


def main():
    """main script"""
    print("----STARTED TOPIC ALERTS----")

    print("Loading input.json...")

    try:
        with open("input.json", "r") as input_file:
            input_json = json.load(input_file)

            # check if json input in correct format
            print("Checking input.json in correct format...")
            check_json(input_json)

            alerts = get_alerts(input_json)

            print(alerts)

    except FileNotFoundError:
        print("Error: Unable to find 'input.json' file in the current directory.")

    except JsonError as error:
        print(f"Error: Incorrect format for 'input.json'. {error.message}")

    print("----FINISHED TOPIC ALERTS----")


if __name__ == "__main__":
    main()
