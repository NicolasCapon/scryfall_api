from scryfall import config
from scryfall.call import get_content
from urllib.parse import quote, urlencode


def get_cards_list(expansion):
    """Get list of cards from a set object"""
    url = expansion.get("search_uri", False)
    content = get_content(url)
    return content.get("data", None)


def get_card_image_url(card, size="normal"):
    """Return a list of normal sized urls for a card object (up to 2 urls for double faced cards)
       Possible sizes: small, normal, large, png, art_crop, border_crop"""
    urls = []
    single_image = card.get("image_uris", {}).get(size, None)
    if single_image:
        urls.append(single_image)
    else:
        for face in card.get("card_faces", []):
            urls.append(face.get("image_uris", {}).get(size, None))
    return urls


def get_named_card(name, set_code="", fuzzy=True):
    """Return a card object from a string cardname"""
    if not isinstance(name, str) or not isinstance(set_code, str):
        return None
    if fuzzy:
        query = "fuzzy=" + quote(name)
    else:
        query = "exact=" + quote(name)
    if set_code:
        query += "&set=" + quote(set_code)

    url = config.base_url + "/cards/named?{}".format(query)
    content = get_content(url)
    if not content.get("object", "error") == "error": 
        return content
    else:
        return None


def get_random_card():
    """Get random card. Include duplicates (basic lands for example), cards like Planes..."""
    url = config.base_url + "/cards/random"
    content = get_content(url)
    if not content.get("object", "error") == "error": 
        return content
    else:
        return {}


def get_card_names(card):
    """Return names of card object in list : [VO, VF]"""
    uri = card.get("uri", None)
    if uri:
        url = uri + "/fr"
        print(url)
        content = get_content(url)
    else:
        return None
    print(content.get("object", "error"))
    if not content.get("object", "error") == "error":
        card_names = [card.get("name", None), content.get("printed_name", None)]
        return card_names
    else:
        card_names = [card.get("name", None)]
        return card_names


def search_cards(**kwarg):
    """Search card with by different parameters in kwarg dict
       See https://scryfall.com/docs/api/cards/search"""

    url = "https://api.scryfall.com/cards/search?" + urlencode(kwarg)
    content = get_content(url)

    return content.get("data", None)

