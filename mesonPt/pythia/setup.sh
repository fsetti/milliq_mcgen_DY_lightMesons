#! /bin/bash

ver=pythia8243

if [ ! -d ${ver} ]; then
    wget http://home.thep.lu.se/~torbjorn/pythia8/${ver}.tgz
    tar xf ${ver}.tgz
    rm ${ver}.tgz
fi

cd $ver
./configure --with-root=$ROOTSYS
make -j12
export PYTHIA8DATA=`pwd`/share/Pythia8/xmldoc

cd ..

