CC=g++ -Wno-deprecated
LDFLAGS=
LIBS=
SOURCES  = $(wildcard *.cc ../decayMCP/MCPTree/*.cc ../utils/*.cc)
INCLUDES = $(wildcard *.h ../decayMCP/MCPTree/*.h ../utils/*.h)
OBJECTS  = $(SOURCES:.cc=.o)
LINKERFLAGS  = $(shell root-config --ldflags --cflags --libs) -lGenVector
CFLAGS = $(shell root-config --cflags)

runMuons: $(OBJECTS)
	$(CC) -o $@ $^ $(LINKERFLAGS)

%.o: %.cc
	$(CC) -c -o $@ $< $(CFLAGS) 

clean:
	rm -f $(OBJECTS)

all: runMuons
