#! /bin/bash

ver=pythia8243

if [ ! -d ${ver} ]; then
    wget http://home.thep.lu.se/~torbjorn/pythia8/${ver}.tgz
    tar xf ${ver}.tgz
    rm ${ver}.tgz
fi

cd $ver

./configure --with-root=$ROOTSYS \
    --with-lhapdf6-lib=/cvmfs/cms.cern.ch/slc6_amd64_gcc630/external/lhapdf/6.2.1-fmblme/lib \
    --with-lhapdf6-include=/cvmfs/cms.cern.ch/slc6_amd64_gcc630/external/lhapdf/6.2.1-fmblme/include \
    --with-lhapdf6-bin=/cvmfs/cms.cern.ch/slc6_amd64_gcc630/external/lhapdf/6.2.1-fmblme/bin
#    --with-lhapdf6 \

make -j12
export PYTHIA8DATA=`pwd`/share/Pythia8/xmldoc

cd ..

