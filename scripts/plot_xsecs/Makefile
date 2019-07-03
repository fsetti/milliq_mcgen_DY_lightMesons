CC=g++ -Wno-deprecated
LDFLAGS=
LIBS=
SOURCES  = $(wildcard *.cc ../../decayMCP/MCPTree/*.cc ../../utils/*.cc ../../decayMCP/DecayGen.cc)
INCLUDES = $(wildcard *.h ../../decayMCP/MCPTree/*.h ../../utils/*.h ../../decayMCP/DecayGen.o)
OBJECTS  = $(SOURCES:.cc=.o)
LINKERFLAGS  = $(shell root-config --ldflags --cflags --libs) -lGenVector
CFLAGS = $(shell root-config --cflags)

getXsecs: $(OBJECTS)
	$(CC) -o $@ $^ $(LINKERFLAGS)

%.o: %.cc
	$(CC) -c -o $@ $< $(CFLAGS) 

clean:
	rm -f $(OBJECTS)

all: getXsecs
