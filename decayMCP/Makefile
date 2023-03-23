# Uses the gnu version of getopt that is not on the mac
# If you are using a MAC "brew install gnu-getopt"
# and then
# export PATH="/usr/local/opt/gnu-getopt/bin:$PATH"
CC=g++ -Wno-deprecated
LDFLAGS=
LIBS=
SOURCES  = $(wildcard *.cc MCPTree/*.cc ../utils/*.cc)
INCLUDES = $(wildcard *.h MCPTree/*.h ../utils/*.h)
OBJECTS  = $(SOURCES:.cc=.o)
LINKERFLAGS  = $(shell root-config --ldflags --cflags --libs) -lGenVector
CFLAGS = $(shell root-config --cflags)

runDecays: $(OBJECTS)
	$(CC) -o $@ $^ $(LINKERFLAGS)

%.o: %.cc
	$(CC) -c -o $@ $< $(CFLAGS) 

clean:
	rm -f $(OBJECTS)

all: runDecays
