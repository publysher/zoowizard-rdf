import datetime
import logging
import itertools
import os
import rdflib
from rdflib.namespace import RDF, RDFS
from rdflib.term import URIRef, Literal
import constants
from namespaces import ZOOCHAT, VOID, DC, SCHEMA, FOAF
import namespaces
import utils

__author__ = 'yigalduppen'

log = logging.getLogger(__name__)
DATASET = URIRef(ZOOCHAT)
DATADUMP = URIRef(ZOOCHAT['/all.nt'])

def describe_dataset(g):
    # describe dataset itself
    # See http://www.w3.org/TR/void/
    g.add((DATASET, RDFS.label, Literal("List of All Zoos Worldwide")))
    g.add((DATASET, RDF.type, VOID.Dataset))
    g.add((DATASET, DC.title, Literal("List of All Zoos Worldwide")))
    g.add((DATASET, DC.created, Literal(datetime.date(2012,8,19))))
    g.add((DATASET, DC.description, Literal(
        "RDF description extracted from http://www.zoochat.com/zoos")))
    g.add((DATASET, DC.source, URIRef('http://www.zoochat.com/zoos')))
    g.add((DATASET, DC.modified, Literal(datetime.date.today())))
    g.add((DATASET, DC.license, URIRef(
        'http://creativecommons.org/licenses/by-sa/3.0/')))
    g.add((DATASET, DC.subject, URIRef(
        'http://dbpedia.org/resource/List_of_zoos')))
    g.add((DATASET, VOID.feature, URIRef(
        'http://www.w3.org/ns/formats/RDF_XML')))

    # we could of course make a random selection, but I happen to like Artis
    g.add((DATASET, VOID.exampleResource, URIRef(
        'http://zoowizard.eu/datasource/zoochat/43')))

    g.add((DATASET, VOID.dataDump, DATADUMP))


    # provide back-references for each zoo
    for zoo in g.subjects(RDF.type, SCHEMA.Zoo):
        g.add((zoo, VOID.inDataset, DATASET))


def extract_filename(uri):
    ROOT = 'http://zoowizard.eu/'
    if not uri.startswith(ROOT):
        raise ValueError("Cannot extract filename", uri)

    return os.path.join(constants.WEBDIR, uri[len(ROOT):])


def ensure_directory_for(filename):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def create_subgraph(graph, item):
    g = rdflib.Graph()
    namespaces.init_bindings(g)

    for triple in graph.triples((item, None, None)):
        g.add(triple)

    for triple in graph.triples((URIRef(item + '#facebook'), None, None)):
        g.add(triple)

    for triple in graph.triples((URIRef(item + '#twitter'), None, None)):
        g.add(triple)

    for triple in graph.triples((None, None, item)):
        g.add(triple)

    return g


def write_rdf_files(g):
    items = itertools.chain(g.subjects(RDF.type, SCHEMA.Zoo),
                            g.subjects(RDF.type, VOID.Dataset))

    for item in items:
        document = item + '.rdf'
        g.add((item, FOAF.isPrimaryTopicOf, URIRef(document)))
        g.add((URIRef(document), FOAF.primaryTopic, item))

        filename = extract_filename(document)
        log.info("Writing %s", filename)
        ensure_directory_for(filename)

        create_subgraph(g, item).serialize(format='xml', destination=filename)


def write_dump(g):
    filename = extract_filename(DATADUMP)
    log.info("Writing data dump %s", filename)
    ensure_directory_for(filename)
    g.serialize(format='nt', destination=filename)


def publish():
    g = utils.read_graph(constants.ZOOCHAT_RDF)
    describe_dataset(g)
    write_rdf_files(g)
    write_dump(g)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    publish()
  