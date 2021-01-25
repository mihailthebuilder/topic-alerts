"""main script"""
from os import path
import json


def main():
    """main script"""
    print("----STARTED TOPIC ALERTS----")

    try:
        with open("input.json", "r") as input_file:
            input_json = json.load(input_file)

            for alert in input_json["alerts"]:
                keyword = alert["keyword"]

                for url in alert["links"]:
                    print(keyword, url)

    except FileNotFoundError:
        print("Error: Unable to find 'input.json' file in the current directory.")

    print("----FINISHED TOPIC ALERTS----")


if __name__ == "__main__":
    main()
