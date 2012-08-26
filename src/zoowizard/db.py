"""
Models the Conjunctive Graph DB for ZooWizard purposes.
"""
import logging
from rdflib import plugin
from rdflib.graph import ConjunctiveGraph, Graph
from rdflib.store import Store, NO_STORE, VALID_STORE
from rdflib.term import URIRef
import sys
import namespaces

store = None
graph_uri = URIRef("http://zoowizard.eu/rdfstore")
log = logging.getLogger(__name__)

def init_store(path):
    """
    Initialize the Conjunctive Graph
    """
    global store

    if store is not None:
        raise RuntimeError("Don't initialize the graph more than once")

    store = plugin.get('Sleepycat', Store)('rdfstore')
    graph = ConjunctiveGraph(store=store, identifier=graph_uri)

    rt = graph.open(path)
    if rt == NO_STORE:
        graph.open(path, create=True)
    else:
        assert rt == VALID_STORE


def _get_graph(uri):
    if store is None:
        raise RuntimeError("Don't forget to call init_graph ")
    graph = Graph(store=store, identifier=URIRef(uri))
    namespaces.init_bindings(graph)
    return graph


def get_zoochat_graph():
    return _get_graph(namespaces.ZOOCHAT_GRAPH)


def get_geonames_graph():
    return _get_graph(namespaces.GEONAMES_GRAPH)

def get_temp_graph():
    return _get_graph(namespaces.TMP_GRAPH)


def main(path, type, input, format='xml'):
    init_store(path)
    if type == 'zoochat':
        g = get_zoochat_graph()
        g.parse(input, format=format)
        g.commit()
    else:
        raise ValueError("Unknown graph type: " + type)

    log.info("Stored %s data %s into database %s", type, input, path)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    main(*sys.argv[1:])
