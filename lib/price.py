"""
Alvin Lee

A module for obtaining the total price of customers from a schedule sheet as a json
"""

import json


class BadSheetJSON(Exception):
    pass


def getPrice(json_dict):
    """
    Returns the total price from all customers in a schedule sheet json
    """
    dictionary = json.loads(json_dict)
    try:
        items_list = list(map(lambda x: x["items"], dictionary["columns"]))
        services_list = list(map(lambda x: x[1]["services"], sum(items_list, [])))
        prices = list(map(lambda x: x["price"], sum(services_list, [])))
        return sum(prices)
    except KeyError:
        raise BadSheetJSON
