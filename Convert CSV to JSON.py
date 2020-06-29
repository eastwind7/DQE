import argparse
import csv
import json
from pprint import pprint
from typing import Dict, List


def parse_arguments():
    """
        Parses incoming arguments.
    """
    parser = argparse.ArgumentParser(description='Parses incoming arguments for csv to json converter.')
    parser.add_argument('-csv', type=str, help='path to csv')
    parser.add_argument('-json', type=str, help='path to create json')
    return parser.parse_args()


def remove_password(user_details: Dict[str, str]) -> Dict[str, str]:
    """
        Takes dictionary with user info and if there is element with key 'password' removes it.
              :param user_details: dictionary that contains information about user.
              :return the same dictionary without password element.
    """
    if 'password' in user_details.keys():
        del user_details['password']
    return user_details


def get_records_from_file(filename: str) -> List[Dict[str, str]]:
    """
          Extracts data from file and removes sensitive information.
                :param filename: path to csv file
                :return list of dictionaries with information about user.
    """
    with open(filename) as csvfile:
        users_details = csv.DictReader(csvfile)
        user_without_password = [remove_password(user) for user in users_details]
    return user_without_password


def write_to_json(users_details: List[Dict[str, str]], filename: str):
    """
          Puts data in json format and than writes it to file
                :param users_details: list of dictionaries with information about user
                :param filename: the path to file to write in
    """
    users_data_json = json.dumps(users_details)
    pprint(users_data_json)
    with open(filename, 'w') as f:
        json.dump(users_data_json, f)


if __name__ == "__main__":
    args = parse_arguments()
    users = get_records_from_file(args.csv)
    write_to_json(users, args.json)
