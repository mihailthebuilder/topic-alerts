"""main script"""
import json
from get_alerts import get_alerts


def main():
    """main script"""
    print("----STARTED TOPIC ALERTS----")

    print("Loading input.json...")

    try:

        with open("input.json", "r") as input_file:
            input_json = json.load(input_file)

            alerts = get_alerts(input_json)

            print(f"\n{len(alerts)} matches were found.")

            if len(alerts) > 0:
                print(alerts)
                print("Check 'summary.txt' for the results.")

    except FileNotFoundError:
        print("ERROR - Unable to find 'input.json' file in the current directory.")
    except json.decoder.JSONDecodeError:
        print("ERROR - 'input.json' contents aren't JSON.")

    print("----FINISHED TOPIC ALERTS----")


if __name__ == "__main__":
    main()
