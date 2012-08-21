import logging
import rdflib
import namespaces

__author__ = 'yigalduppen'

log = logging.getLogger(__name__)

def read_graph(*rdfs):
    """
    Read multiple RDF-files and combine them into one graph.
    """
    g = rdflib.Graph()
    namespaces.init_bindings(g)

    for rdf in rdfs:
        log.info("Reading graph %s", rdf)
        g.parse(rdf)

    log.info("Read %d tuples", len(g))
    return g