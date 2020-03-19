# PYTHIA configuration file.

# Install directory prefixes.
PREFIX_BIN=$(PWD)/bin
PREFIX_INCLUDE=$(PWD)/include
PREFIX_LIB=$(PWD)/lib
PREFIX_SHARE=

# Compilation flags (see ./configure --help for further documentation).
ENABLE_SHARED=false
FC=gfortran
CXX=gfortran
#CXX_COMMON=-g  -pedantic -W -Wall -Wshadow 
#-fPIC
#CXX_SHARED=-dynamiclib
#CXX_SONAME=-Wl,-dylib_install_name,@rpath/
LIB_SUFFIX=.a

# EVTGEN configuration.
EVTGEN_USE=false
EVTGEN_BIN=
EVTGEN_INCLUDE=
EVTGEN_LIB=

# FASTJET3 configuration.
FASTJET3_USE=false
FASTJET3_BIN=
FASTJET3_INCLUDE=
FASTJET3_LIB=

# HEPMC2 configuration.
HEPMC2_USE=true
HEPMC2_BIN=/usr/local/bin
HEPMC2_INCLUDE=/usr/local/include
HEPMC2_LIB=/usr/local/lib

# HEPMC3 configuration.
HEPMC3_USE=false
HEPMC3_BIN=
HEPMC3_INCLUDE=
HEPMC3_LIB=

# LHAPDF5 configuration.
LHAPDF5_USE=false
LHAPDF5_BIN=
LHAPDF5_INCLUDE=
LHAPDF5_LIB=

# LHAPDF6 configuration.
LHAPDF6_USE=false
LHAPDF6_BIN=
LHAPDF6_INCLUDE=
LHAPDF6_LIB=

# POWHEG configuration.
POWHEG_USE=false
POWHEG_BIN=
POWHEG_INCLUDE=
POWHEG_LIB=

# PROMC configuration.
PROMC_USE=false
PROMC_BIN=
PROMC_INCLUDE=
PROMC_LIB=

# ROOT configuration.
ROOT_USE=false
ROOT_BIN=
ROOT_LIBS=
CXX_ROOT=

# GZIP configuration.
GZIP_USE=false
GZIP_BIN=
GZIP_INCLUDE=
GZIP_LIB=

# BOOST configuration.
BOOST_USE=false
BOOST_BIN=
BOOST_INCLUDE=
BOOST_LIB=

# PYTHON configuration.
PYTHON_USE=false
PYTHON_BIN=
PYTHON_INCLUDE=
PYTHON_LIB=
