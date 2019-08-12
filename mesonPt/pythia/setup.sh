#! /bin/bash

ver=pythia8243

wget http://home.thep.lu.se/~torbjorn/pythia8/${ver}.tgz
tar xf ${ver}.tgz
rm ${ver}.tgz

cd $ver
./configure --with-root=$ROOTSYS

make -j12

cd ..

