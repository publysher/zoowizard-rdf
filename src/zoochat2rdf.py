#!/usr/bin/env python
import os
import pickle

import rdflib
import logging
from rdflib.namespace import RDF, RDFS, SKOS
from rdflib.term import Literal, URIRef
import constants
from namespaces import ZOOCHAT, SCHEMA, FOAF
import namespaces

log = logging.getLogger(__name__)
DATASET = URIRef(ZOOCHAT)


def add_account(g, id, provider, profile, type):
    account = URIRef(id + '#' + type)
    g.add((id, FOAF.account, account))
    g.add((account, RDF.type, FOAF.OnlineAccount))
    g.add((account, FOAF.accountServiceHomePage, provider))
    g.add((account, FOAF.accountProfilePage, profile))


def fill_graph(zoolist, g):
    for zoo in zoolist:
        name = zoo['name']
        id = URIRef(ZOOCHAT['/' + zoo['zoochat_id']])

        g.add((id, RDFS.label, Literal(name)))
        g.add((id, SKOS.prefLabel, Literal(name)))
        g.add((id, SCHEMA.name, Literal(name)))

        g.add((id, RDF.type, SCHEMA.Zoo))
        g.add((id, RDF.type, FOAF.Organization))

        for alt in zoo['alternative_names']:
            g.add((id, SKOS.altLabel, Literal(alt)))

        g.add((id, FOAF.based_near, Literal(zoo['country'])))
        g.add((id, SCHEMA.addressCountry, Literal(zoo['country'])))

        if zoo['website']:
            g.add((id, FOAF.homepage, zoo['website']))

        if zoo['wikipedia']:
            g.add((id, FOAF.isPrimaryTopicOf, zoo['wikipedia']))

        if zoo['facebook']:
            add_account(g, id, 'http://www.facebook.com', zoo['facebook'],
                        'facebook')

        if zoo['twitter']:
            add_account(g, id, 'http://www.twitter.com', zoo['twitter'],
                        'twitter')

        if zoo['map']:
            g.add((id, SCHEMA.map, zoo['map']))

    return g


def init_graph():
    g = rdflib.Graph()
    namespaces.init_bindings(g)

    return g


def main(input=constants.ZOOCHAT_PICKLE, output=constants.ZOOCHAT_RDF):
    zoolist = []
    try:
        with open(input) as f:
            zoolist = pickle.load(f)
    except IOError, e:
        log.error("You need to generate the pickled file by using zoochat2py.")
        log.exception(e)

    g = init_graph()
    fill_graph(zoolist, g)

    if not os.path.exists(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))
    g.serialize(output, format='xml')
    log.info("RDF Graph written to %s", output)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()