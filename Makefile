ZC_IN  = data/zoochat/input/zoolist.html
ZC_MED = data/zoochat/intermediate/zoolist.pickle
ZC_OUT = data/zoochat/output/zoolist.rdf

ZC_RDF = data/www/datasource/zoochat
ZC_DS  = $(ZC_RDF).rdf
ZC_DUMP= $(ZC_RDF)/all.nt
VOID   = data/www/.wellknown/void


ARCHIVE = data/www.tar.gz

.PHONY: all dataclean

all:    $(ARCHIVE)

dataclean:
	rm -f $(ZC_MED) $(ZC_OUT) $(ARCHIVE)
	rm -rf data/www

# ZooChat files
$(ZC_MED): $(ZC_IN)
	./bin/py -m zoochat.webparser $< > $@

$(ZC_OUT): $(ZC_MED)
	./bin/py -m zoochat.rdfcreator $< > $@

$(ZC_RDF) $(ZC_DUMP) $(ZC_DS): $(ZC_OUT)
	./bin/py -m zoochat.publish $<

# Publishing

$(VOID): $(ZC_DS)
	mkdir -p $(dir $@)
	./bin/py -m dspublish $^ > $@

$(ARCHIVE): $(VOID) $(ZC_RDF)
	tar czf $(ARCHIVE) -s'|data/www/||' $^


