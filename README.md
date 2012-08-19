zoowizard-rdf
=============

Manages an RDF repository for Zoo Wizard.

The current version creates an initial RDF datasource for the http://www.zoochat.com/zoos/ list of zoos.


Setup
-----

Bootstrap the project with 

	python bootstrap.py && ./bin/buildout

Then, run the following scripts:

	./bin/py -m zoochat2py		# use webscraping to create a cached list of dicts
	./bin/py -m zoochat2rdf		# convert the cached list to an initial RDF graph
	./bin/py -m publish		# create RDF files for all the concepts
