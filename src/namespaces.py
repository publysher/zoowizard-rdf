from rdflib.namespace import Namespace, SKOS

__author__ = 'yigalduppen'

# See http://www.w3.org/2011/rdfa-context/rdfa-1.1

ZOOCHAT = Namespace("http://zoowizard.eu/datasource/zoochat")
SCHEMA = Namespace("http://schema.org/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
DC = Namespace("http://purl.org/dc/terms/")
CC = Namespace("http://creativecommons.org/ns#")
OG = Namespace("http://ogp.me/ns#")
VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
VOID = Namespace("http://rdfs.org/ns/void#")

DEFAULTS = dict(
    foaf=FOAF,
    schema=SCHEMA,
    zoochat=ZOOCHAT,
    dc=DC,
    cc=CC,
    vcard=VCARD,
    skos=SKOS,
    void=VOID,
)

def init_bindings(graph):
    for k, v in DEFAULTS.items():
        graph.bind(k, v)

