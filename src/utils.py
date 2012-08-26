from StringIO import StringIO
import logging
import rdflib
from rdflib.graph import Graph
from rdflib.namespace import RDF
from rdflib.term import BNode, URIRef
import namespaces

__author__ = 'yigalduppen'

log = logging.getLogger(__name__)


def concise_bounded_description(graph, uri):
    """
    Given a particular node (the starting node) in a particular RDF graph
    (the source graph), a subgraph of that particular graph, taken to comprise
    a concise bounded description of the resource denoted by the starting node,
    can be identified as follows:

    * Include in the subgraph all statements in the source graph where the
      subject of the statement is the starting node;
    * Recursively, for all statements identified in the subgraph thus far having
      a blank node object, include in the subgraph all statements in the source
      graph where the subject of the statement is the blank node in question and
      which are not already included in the subgraph.
    * Recursively, for all statements included in the subgraph thus far, for all
      reifications of each statement in the source graph, include the concise
      bounded description beginning from the rdf:Statement node of each
      reification.
    """
    subgraph = Graph()

    for ns in graph.namespaces():
        subgraph.bind(ns[0], ns[1], override=False)

    blank_nodes = []
    for p, o in graph.predicate_objects(uri):
        subgraph.add((uri, p, o))
        if isinstance(o, BNode):
            blank_nodes.append(o)

    while blank_nodes:
        s = blank_nodes.pop()
        print "adding bnode", s
        for p, o in graph.predicate_objects(s):
            print "(", s, p, o, ")"
            subgraph.add((s, p, o))
            if isinstance(o, BNode):
                blank_nodes.append(o)

    for s in graph.subjects(RDF.subject, uri):
        for p, o in graph.predicate_objects(s):
            subgraph.add((s, p, o))


    return subgraph


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

