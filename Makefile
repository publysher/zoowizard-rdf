DB     = data/db
WWW    = data/www
ARCHIVE= data/www.tar.gz

ZC_IN  = data/zoochat/input/zoolist.html
ZC_MED = data/zoochat/intermediate/zoolist.pickle
ZC_OUT = data/zoochat/output/zoolist.rdf

ZC_RDF = $(WWW)/datasource/zoochat
ZC_DS  = $(ZC_RDF).rdf
ZC_DUMP= $(ZC_RDF)/all.nt
VOID   = $(WWW)/.wellknown/void

ZWBASIC= data/zoowizard/zoos-basic.xml
ZWGEO  = data/zoowizard/zoo-geo.xml



.PHONY: all dataclean

all:    $(ARCHIVE)

dataclean:
	rm -f $(ZC_MED) $(ZC_OUT) $(ARCHIVE)
	rm -rf $(WWW) $(DB)

# ZooChat files
$(ZC_MED): $(ZC_IN)
	./bin/py -m zoochat.webparser $< > $@

$(ZC_OUT): $(ZC_MED)
	./bin/py -m zoochat.rdfcreator $< > $@

$(ZC_RDF) $(ZC_DUMP) $(ZC_DS): $(ZC_OUT)
	./bin/py -m zoochat.publish $<


# ZooWizard repository
$(ZWBASIC): $(ZC_DUMP)
	./bin/py -m zoowizard.db $(DB) zoochat $< nt
	mkdir -p $(dir $@)
	./bin/py -m zoowizard.collect > $@


$(ZWGEO): $(ZWBASIC)
	# todo: import $< into db
	# todo: use geonames from collect script
	false 


# Publishing

$(VOID): $(ZC_DS)
	mkdir -p $(dir $@)
	./bin/py -m dspublish $^ > $@

$(ARCHIVE): $(VOID) $(ZC_RDF) $(ZC_DUMP) $(ZWGEO)
	tar czf $(ARCHIVE) -s'|data/www/||' $^


