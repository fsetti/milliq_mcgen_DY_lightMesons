#! /bin/bash

tar -chJf input.tar.xz write_cards_metis.py extract_kinematics_metis.py \
    ../MG5_aMC_v2_6_5 ../models ../patches ../ntupler/run ../setup.sh ../write_cards.py \
    ../extract_kinematics.py ../ntupler/run ../ntupler/MCPTree

