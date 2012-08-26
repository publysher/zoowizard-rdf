from rdflib.namespace import Namespace, SKOS, OWL

__author__ = 'yigalduppen'

ZOO_GRAPH = "http://zoowizard.eu/zoo/"
ZOOCHAT_GRAPH = "http://zoowizard.eu/datasource/zoochat"
GEONAMES_GRAPH = "http://geonames.org/"
TMP_GRAPH = "http://example.com/tmp"

# See http://www.w3.org/2011/rdfa-context/rdfa-1.1

TMP = Namespace(TMP_GRAPH)
ZOO = Namespace(ZOO_GRAPH)
ZOOCHAT = Namespace(ZOOCHAT_GRAPH)
SCHEMA = Namespace("http://schema.org/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
DC = Namespace("http://purl.org/dc/terms/")
CC = Namespace("http://creativecommons.org/ns#")
OG = Namespace("http://ogp.me/ns#")
VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
VOID = Namespace("http://rdfs.org/ns/void#")
GEONAMES = Namespace("http://www.geonames.org/ontology#")

DEFAULTS = dict(
    foaf=FOAF,
    schema=SCHEMA,
    zoochat=ZOOCHAT,
    dc=DC,
    cc=CC,
    vcard=VCARD,
    skos=SKOS,
    void=VOID,
    zoo=ZOO,
    owl=OWL,
    geonames=GEONAMES,
)

def init_bindings(graph):
    for k, v in DEFAULTS.items():
        graph.bind(k, v)


