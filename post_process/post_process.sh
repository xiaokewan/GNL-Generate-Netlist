#!/usr/bin/bash
# -*- coding: utf-8 -*-
# @Time    : 3/21/24 
# @Author  : Marieke Louage, Xiaoke Wang
# @Group   : UGent HES
# @File    : post_process.py
# @Software: PyCharm, Ghent

#!/bin/bash

# This script processes BLIF files in a specified working directory using netlist2rent.py and rent2viz.py,
# and optionally reads VPR results with readvpr.py. It supports enabling or disabling specific parts of the process.
# Usage: ./post_process.sh <work_dir_path> -n [on|off] -r [on|off]
# Parameters:
#   <work_dir_path>: Mandatory. The path to the working directory containing BLIF files and where output files will be generated.
#   -n [on|off]: Optional. whether to run netlist2rent.py. Default is 'on'. 
#   -v [on|off]: Optional. whether to run rent2viz.py. Default is 'on'.
#   -r [on|off]: Optional. whether to run readvpr.py to process VPR results. Default is 'off'.
WORK_DIR=$1
RUN_NETLIST2RENT="on"
RUN_RENT2VIZ="on"
READ_VPR="off"

source "./config.sh"


shift # shift arguments

while getopts ":n:v:r:" opt; do
  case ${opt} in
    n )
      RUN_NETLIST2RENT=$OPTARG
      ;;
    v )
      RUN_RENT2VIZ=$OPTARG
      ;;
    r )
      READ_VPR=$OPTARG
      ;;
    \? )
      echo "Usage: $0 <work_dir_path> -n [*on*|off] -v [*on*|off] -r [on|*off*]"
      exit 1
      ;;
    : )
      echo "Usage: $0 <work_dir_path> -n [*on*|off] -v [*on*|off] -r [on|*off*]"
      exit 1
      ;;
  esac
done

if [ -f "$WORK_DIR" ]; then
  WORK_DIR=$(dirname "${WORK_DIR}")
fi

if [ ! -d "$WORK_DIR" ]; then
    echo "Error: $WORK_DIR is not a valid directory"
    exit 1
fi

#$WORK_DIR="$PROJECT_ROOT/$WORK_DIR"
cd "$PROJECT_ROOT/$WORK_DIR" || exit


# netlist2rent.py: Transfer the .blif to Hypergraph
if [ "$RUN_NETLIST2RENT" == "on" ]; then
    for blif_file in *.blif; do
        echo "Processing $blif_file with netlist2rent.py"
        python3 "$POST_DIR/netlist2rent.py" "$blif_file" "$PROJECT_ROOT/$WORK_DIR/rent_files" "$HMETIS_DIR"
    done
fi

# rent2viz.py: visualized partitioned netlist (rent graph)
if [ "$RUN_RENT2VIZ" == "on" ]; then
    for rent_file in *.rent; do
        echo "Visualizing $rent_file with rent2viz.py"
        python3 "$POST_DIR/rent2viz.py" "$rent_file" "./rent_figures"
    done
fi

# read vpr results (vpr_files)
if [ "$READ_VPR" == "on" ]; then
    echo "Processing VPR results with readvpr.py"
    python3 "$POST_DIR/readvpr.py" "$WORK_DIR/vpr_files" "."
fi

cd - > /dev/null || exit
