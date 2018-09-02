from scryfall import config
from scryfall.call import get_content
from datetime import datetime


def get_expansion_list():
    """Get list of all MTG expansion objects"""
    url = config.base_url + "/sets"
    content = get_content(url)
    return content.get("data", None)


def get_future_expansions(include_digital=False):
    """Get list of all futur expansion objects until the last expansion with a past release date"""
    now = datetime.now()
    expansions = get_expansion_list()
    future_expansions = []
    i = 0
    while datetime.strptime(expansions[i].get("released_at", "3000-01-01"), '%Y-%m-%d') > now and i < len(expansions):
        # Doesn't include Magic Online expansions
        expansion = expansions[i]
        i += 1
        if not expansions[i].get("digital", False) == include_digital:
            continue
        future_expansions.append(expansion)
        
    return future_expansions


def get_card_expansion(card):
    """Return expansion object from a Card object"""
    expansion_code = card.get("code", None)
    if not expansion_code: return None

    url = config.base_url + "/sets/{}".format(expansion_code)
    return get_content(url)


def get_expansion(expansion_code):
    """Return expansion object from a expansion_code"""
    if not expansion_code: return None
    url = config.base_url + "/sets/{}".format(expansion_code)
    return get_content(url)


if __name__ == "__main__":
    print([s["name"] for s in get_future_expansions()])
