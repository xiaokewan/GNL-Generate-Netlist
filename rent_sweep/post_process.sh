#!/usr/bin/bash
# -*- coding: utf-8 -*-
# @Time    : 3/21/24 
# @Author  : Marieke Louage, Xiaoke Wang
# @Group   : UGent HES
# @File    : post_process.py
# @Software: PyCharm, Ghent

WORK_DIR="./sweep_and2_q0/"
POST_PY_PATH="../../post-process"
HMETIS_PATH="../../hmetis-1.5-linux/hmetis"

 
cd $WORK_DIR

# netlist2rent.py
for blif_file in *.blif; do
    echo "Processing $blif_file with netlist2rent.py"
    python3 "$POST_PY_PATH/netlist2rent.py" "$blif_file" "." "$HMETIS_PATH"
done

# rent2viz.py
for rent_file in *.rent; do
    echo "Visualizing $rent_file with rent2viz.py"
    python3 "$POST_PY_PATH/rent2viz.py" "$rent_file"
done

# read vpr results
python3 "../readvpr.py" "./vpr_files" "./"


cd - || exit
