"""
Collects information from the ZooChat repository and the surrounding internets
into the primary Zoo Wizard collection of zoos.
"""
import logging
import sys
from rdflib import plugin
from rdflib.graph import Graph, ConjunctiveGraph
from rdflib.namespace import RDF, RDFS, OWL, SKOS
from rdflib.store import Store
import unicodedata
from rdflib.term import URIRef, BNode
import geoutils
import namespaces
from zoowizard import db

__author__ = 'yigalduppen'
log = logging.getLogger(__name__)

def clean_label(label):
    """
    Convert a label to something suitable for clean URIs
    """
    def printable(c):
        return unicodedata.category(c) in ('Ll', 'Zs')

    def as_char(c):
        if unicodedata.category(c) == 'Ll':
            return c
        if unicodedata.category(c) == 'Zs':
            return '_'
        raise ValueError()


    normalized_label = unicodedata.normalize('NFD', label.lower())
    return ("".join([as_char(c) for c in normalized_label if printable(c)])).replace('__', '_').title()


def create_resources(from_graph, to_graph):
    """
    For each zoo in from_graph, create an appropriately named zoo in to_graph.
    """
    for subject in from_graph.subjects(RDF.type, namespaces.SCHEMA.Zoo):
        label = from_graph.value(subject, RDFS.label)
        cleaned_label = clean_label(label)
        if cleaned_label.lower().endswith("_closed"):
            continue

        identifier = namespaces.ZOO[cleaned_label]

        if list(to_graph.predicate_objects(identifier)):
            raise ValueError("Duplicate identifier", identifier)

        to_graph.add((identifier, RDF.type, namespaces.SCHEMA.Zoo))
        to_graph.add((identifier, OWL.sameAs, subject))


def copy_simple_fact(from_graph, to_graph, predicate):
    """
    Copy a simple fact from from_graph to to_graph:

    for :from owl.sameAs :to

    :from :predicate :x -> :to :predicate :x
    """
    for to_subject, from_subject in to_graph.subject_objects(OWL.sameAs):
        for object in from_graph.objects(from_subject, predicate):
            to_graph.add((to_subject, predicate, object))

def copy_resource_fact(from_graph, to_graph, predicate):
    """
    Copy a complex fact from from_graph to to_graph:

    for :from owl.sameAs :to

    :from :predicate :x -> :to :predicate :BNode()
    :x :p2 :y              :BNode() :p2 :y
    """
    for to_subject, from_subject in to_graph.subject_objects(OWL.sameAs):
        for object in from_graph.objects(from_subject, predicate):
            hash_index = unicode(object).find('#')
            resource = URIRef(unicode(to_subject) + unicode(object)[hash_index:])

            to_graph.add((to_subject, predicate, resource))
            for p, o in from_graph.predicate_objects(object):
                to_graph.add((resource, p, o))



def copy_simple_facts(from_graph, to_graph):
    """
    Copy all simple facts in from_graph to to_graph
    """
    copy_simple_fact(from_graph, to_graph, RDFS.label)
    copy_simple_fact(from_graph, to_graph, SKOS.altLabel)
    copy_simple_fact(from_graph, to_graph, namespaces.FOAF.homepage)
    copy_resource_fact(from_graph, to_graph, namespaces.FOAF.account)



def get_and_store_country(geonames_graph, country_name):
    # do we know this country by name?
    for s in geonames_graph.subjects(namespaces.GEONAMES.officialName, country_name):
        return s

    # do we know this country by alternate name?
    for s in geonames_graph.subjects(namespaces.GEONAMES.alternateName, country_name):
        return s


    # retrieve from the internet :)
    geonames_uri = geoutils.find_geonames_country_uri(country_name)
    log.info("Found %s on the internet: %s", country_name, geonames_uri)

    if not URIRef(geonames_uri) in geonames_graph.subjects():
        log.info("Parsing %s", geonames_uri)
        geonames_graph.parse(location=geonames_uri)

    geonames_graph.add((geonames_uri, namespaces.GEONAMES.alternateName, country_name))
    geonames_graph.commit()

    return geonames_uri


def find_country_references(from_graph, to_graph, geonames_graph):
    """
    Given natural-language names in the from graph, create references to
    geonames in the to_graph.

    Copies the relevant information from Geonames to geonames_graph,

    for :from owl.sameAs :to
        :from schema.addressCountry :country

    :to geonames.inCountry [geonames version of :country]
    """
    from_pred = namespaces.SCHEMA['addressCountry']
    to_pred = namespaces.GEONAMES['parentCountry']
    for (from_uri, country_name) in from_graph.subject_objects(from_pred):
        country_uri = get_and_store_country(geonames_graph, country_name)

        to_uri = to_graph.value(subject=None, predicate=OWL.sameAs, object=from_uri)
        log.info("Adding (%s, %s, %s)", to_uri, to_pred, country_uri)
        to_graph.add((to_uri, to_pred, country_uri))


def derive_dbpedia(zoochat, zoowizard):
    topics = zoochat.subject_objects(namespaces.FOAF.isPrimaryTopicOf)
    for (id, wikipage) in topics:
        wikipage = unicode(wikipage)
        if wikipage.find("wikipedia") < 0:
            continue

        dbpage = (wikipage
                  .replace("en.wikipedia", "dbpedia")
                  .replace("wikipedia", "dbpedia")
                  .replace("wiki", "resource"))

        zoowizard_id = zoowizard.value(None, OWL.sameAs, id)
        zoowizard.add((zoowizard_id, OWL.sameAs, dbpage))


def main(output):
    db.init_store("data/db")

    zoochat = db.get_zoochat_graph()
    print "Loaded zoochat graph", zoochat, "containing", len(zoochat), "triples"

    zoowizard = Graph(identifier=namespaces.ZOO_GRAPH)
    namespaces.init_bindings(zoowizard)

    create_resources(zoochat, zoowizard)
    copy_simple_facts(zoochat, zoowizard)
    derive_dbpedia(zoochat, zoowizard)
    
#    geonames = db.get_geonames_graph()
#    print "Loaded geonames graph", geonames, "containing", len(geonames), "triples"
#    find_country_references(zoochat, zoowizard, geonames)

    zoowizard.serialize(destination=output)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main(sys.stdout)