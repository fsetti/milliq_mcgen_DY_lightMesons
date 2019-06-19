#! /bin/bash

if [ -f package.tar.xz ]; then
    rm ./package.tar.xz
fi

tar -hcJf package.tar.xz --exclude='.git' --exclude='*.root'  --exclude='*.tar*' --exclude='batchsubmit*' ../../../../../$CMSSW_VERSION

