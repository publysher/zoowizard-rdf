"""
Create a voidfile based on the specified input files
"""
import logging
import sys
from rdflib.graph import Graph
from rdflib.namespace import RDF
from namespaces import VOID
import namespaces
import utils

log = logging.getLogger(__name__)

def write_resource(graph, dataset_uri, out, include_backlinks=True,
                    format='xml'):
    """
    Writes a single dataset
    """
    subgraph = Graph()
    namespaces.init_bindings(subgraph)

    for p, o in graph.predicate_objects(dataset_uri):
        subgraph.add((dataset_uri, p, o))

    if include_backlinks:
        for s, p in graph.subject_predicates(dateset_uri):
            subgraph.add((s, p, dataset_uri))

    subgraph.serialize(destination=out, format=format)


def generate_void(graph, out):
    """
    Writes a VoID file containing all the datasets in `graph` to `out`.
    """
    datasets = graph.subjects(RDF.type, VOID.Dataset)
    for ds in datasets:
        log.info("Serializing %s", ds)
        write_resource(graph, ds, out, include_backlinks=False)


def main(out, *rdfs):
    g = utils.read_graph(*rdfs)
    generate_void(g, out)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main(sys.stdout, *sys.argv[1:])
