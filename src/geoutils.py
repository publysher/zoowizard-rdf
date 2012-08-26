"""
Utilities for finding Geonames data.
"""
import json
import logging
import urllib
import urllib2

GEONAMES_WS = "http://sws.geonames.org/%s/"
log = logging.getLogger(__name__)

def get_geonames_json(query):
    """
    Given a query string, returns the JSON in geonames.
    """
    url = "http://ws.geonames.org/searchJSON?%s" % (urllib.urlencode(dict(
        name = query
    )))
    log.debug("Querying %s", url)

    page = urllib2.urlopen(url).read()
    log.debug("Retrieved %s", page)

    doc = json.loads(page)

    return doc.get('geonames')[0]


def find_geonames_country_uri(country_name):
    """
    Given a country name, find the geonames uri for that country.
    """
    json = get_geonames_json(country_name)
    result = GEONAMES_WS % json['geonameId']
    log.info("Found %s => %s", country_name, result)
    return result
