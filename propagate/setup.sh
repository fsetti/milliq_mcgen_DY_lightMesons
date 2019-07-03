#! /bin/bash

if [ ! -d MilliqanSim ]; then
    git clone https://github.com/bjmarsh/MilliqanSim.git
    pushd MilliqanSim
    git checkout reorganization
    popd
fi

pushd MilliqanSim
. setup.sh
popd


