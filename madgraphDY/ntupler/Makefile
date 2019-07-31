CC=g++ -Wno-deprecated
LDFLAGS=
LIBS=
SOURCES = $(wildcard *.cc ../../decayMCP/MCPTree/*.cc)
INCLUDES = $(wildcard *.h ../../decayMCP/MCPTree/*.h)
OBJECTS  = $(SOURCES:.cc=.o)
LINKERFLAGS  = $(shell root-config --ldflags --cflags --libs) -lGenVector
CFLAGS = $(shell root-config --cflags)

run: $(OBJECTS)
	$(CC) -o $@ $^ $(LINKERFLAGS)

%.o: %.cc
	$(CC) -c -o $@ $< $(CFLAGS) 

clean:
	rm -f $(OBJECTS)

all: run
