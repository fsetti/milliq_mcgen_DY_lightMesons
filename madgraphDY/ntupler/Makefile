CC=g++ -Wno-deprecated
LDFLAGS=
LIBS=
SOURCES = $(wildcard *.cc MCPTree/*.cc)
INCLUDES = $(wildcard *.h MCPTree/*.h)
OBJECTS  = $(SOURCES:.cc=.o)
LINKERFLAGS  = $(shell root-config --ldflags --cflags --libs) -lGenVector
CFLAGS = $(shell root-config --cflags)

run: $(OBJECTS)
	$(CC) -o $@ $^ $(LINKERFLAGS)

%.o: %.cc
	$(CC) -c -o $@ $< $(CFLAGS) 

clean:
	rm -f $(OBJECTS) run

all: run
