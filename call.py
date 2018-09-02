import requests
import json
import logging
from time import sleep

"""API Doc : https://scryfall.com/docs/api"""


def get_content(url, delay=0.1):
    """Extract data from API json file. If there is multiple pages, gather them."""
    if not url: return False
    # Time limit of API, recommended 0.1s per request
    sleep(delay)
    r = requests.get(url)
    data = {}
    if r.status_code == requests.codes.ok:
        data = json.loads(r.content.decode('utf-8'))
        if data.get("object", False) == "error": 
            logging.info("API respond an error to url : {0}".format(url))
            return False
        if data.get("has_more", None) and data.get("next_page", None):
            content = get_content(data["next_page"])
            data["data"] += content.get("data", [])
    else:
        logging.info("Wrong status code: {}".format(r.status_code))

    return data

