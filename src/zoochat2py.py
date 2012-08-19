#!/usr/bin/env python
"""
Generates a pickled list of dictionaries by parsing the ZooChat HTML.
"""
import os
import pickle
import bs4
import logging
import constants

log = logging.getLogger(__name__)

def parse_zoolist(inp):
    log.info("Parsing %s", inp)
    with open(inp, 'r') as f:
        soup = bs4.BeautifulSoup(f)

    log.info("Collecting tables")
    table_headers = soup.find_all('h2', 'hometitle')
    tables = [h.find_next_sibling("table") for h in table_headers]

    log.info("Found %d tables", len(tables))
    zoolist = []
    for table in tables:
        country = None
        for tr in table.find_all('tr'):
            head = tr.find('td', 'thead')
            if head:
                links = head.find_all('a')
                country = links[-1].text
                continue

            cells = tr.find_all('td')

            def get_href(cell, base=''):
                link = cell.find('a')
                if not link:
                    return None
                href = link.get('href')
                if href:
                    return base + href
                return None

            zoo = dict(
                country=country,
                zoochat_id=cells[0].text,
                name=cells[1].text,
                alternative_names=[name.strip() for name in
                                   cells[2].text.split(';') if name.strip()],
                website=get_href(cells[3]),
                wikipedia=get_href(cells[4]),
                facebook=get_href(cells[5]),
                twitter=get_href(cells[6]),
                map=get_href(cells[7], 'http://www.zoochat.com'),
                )
            log.info("Found %s", zoo)
            zoolist.append(zoo)

    return zoolist


def main(input=constants.ZOOCHAT_INPUT, output=constants.ZOOCHAT_PICKLE):
    zoolist = parse_zoolist(input)

    if not os.path.exists(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))
    os.makedirs(os.path.dirname(output))
    with open(output, 'w') as f:
        pickle.dump(zoolist, f)

    log.info("Written zoo list to %s", output)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
