# Set the shell.
SHELL=/usr/bin/env bash

PREFIX_LIB=./pythia8243/lib
PREFIX_INCLUDE=./pythia8243/include

# Compilation flags (see ./configure --help for further documentation).
CXX=g++
CXX_COMMON=-O2  -pedantic -W -Wall -Wshadow -fPIC

CXX_COMMON:=-I$(PREFIX_INCLUDE) $(CXX_COMMON)
CXX_COMMON+= -L$(PREFIX_LIB) -Wl,-rpath,$(PREFIX_LIB) -lpythia8 -ldl 

# All targets (no default behavior).
all: main

# ROOT (turn off all warnings for readability).
main: main.cc $(PREFIX_LIB)/libpythia8.a
	$(CXX) $< -o $@ -w $(CXX_COMMON) \
	  $(shell root-config --cflags) \
	  -Wl,-rpath $(shell root-config --glibs)

# Clean.
clean:
	rm -f main;
