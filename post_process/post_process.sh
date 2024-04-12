#!/usr/bin/bash
# -*- coding: utf-8 -*-
# @Time    : 3/21/24 
# @Author  : Xiaoke Wang
# @Group   : UGent HES
# @File    : post_process.py
# @Software: PyCharm, Ghent

#!/bin/bash

# This script processes BLIF files in a specified working directory using netlist2rent.py and rent2viz.py,
# and optionally reads VPR results with readvpr.py. It supports enabling or disabling specific parts of the process.
# Usage: ./post_process.sh <work_dir_path> -n [on|off] -v [on|off] -r [on|off] 


# Parameters:
#   <work_dir_path>: Mandatory. The path to the working directory containing BLIF files and where output files will be generated.
#   -n --net2rent [on|off]: blif to rent hypergraph, default 'on'. Optional. whether to run netlist2rent.py.
#   -v --viz [on|off]: rent hypergraph to figure, default 'on'. Optional. whether to run rent2viz.py.
#                recommend: <work_dir_path> will search .rent files in the current folder and sub-folder
#   -r -- read [on|off]: Read VPR results for runtime critical pathlength ..., default is 'off'. Optional. whether to run readvpr.py to process VPR results. Default is 'off'.
#   -m --norm [on|off]: Using normalization rent_graph. Default is off.
#   -h help
WORK_DIR=$1
RUN_NETLIST2RENT="on"
RUN_RENT2VIZ="on"
READ_VPR="off"
NORM="off"
usage() {
  echo "Usage: $0 <work_dir_path> -n [*on*|off] -v [*on*|off] -r [on|*off*] -m [on|off]"
  echo "  -n  [on|off]: blif to rent hypergraph, default 'on'."
  echo "  -v  [on|off]: rent hypergraph to figure, default 'on'."
  echo "  -r  [on|off]: Read VPR results for runtime critical pathlength ..., default is 'off'."
  echo "  -m  [on|off]: Using normalization rent_graph. Default is off."
  exit 0
}
if [ $# -eq 0 ] || [ "$1" == "-h" ]; then
  usage
fi

source "./config.sh"


shift # shift arguments

while getopts ":n:v:r:m" opt; do
  case ${opt} in
    n | net2rent)
      RUN_NETLIST2RENT=$OPTARG
      ;;
    v | viz)
      RUN_RENT2VIZ=$OPTARG
      ;;
    r | read)
      READ_VPR=$OPTARG
      ;;
    m | norm)
      NORM=$OPTARG
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
        if [ "$NORM" == "off" ]; then
            echo "Processing $blif_file with netlist2rent.py"
            python3 "$POST_DIR/netlist2rent.py" "$blif_file" "$PROJECT_ROOT/$WORK_DIR/rent_files" "$HMETIS_DIR"
        else
            echo "Processing $blif_file with nl2norm_rent.py"
            python3 "$POST_DIR/rent_norm/nl2norm_rent.py" "$blif_file" "$PROJECT_ROOT/$WORK_DIR/rent_files" "$HMETIS_DIR"
        fi
    done
fi

# rent2viz.py: visualized partitioned netlist (rent graph)
if [ "$RUN_RENT2VIZ" == "on" ]; then
#    if ls *.rent */*.rent >/dev/null 2>&1; then
        for rent_file in *.rent */*.rent; do
            if [ "$NORM" == "off" ]; then
                echo "Visualizing $rent_file with rent2viz.py"
                echo "$rent_file"
                python3 "$POST_DIR/rent2viz.py" "$rent_file" "$PROJECT_ROOT/$WORK_DIR/rent_figures"
            else
                echo "Visualizing $rent_file with rent_norm2viz.py"
                echo "$rent_file"
                python3 "$POST_DIR/rent_norm/rent_norm2viz.py" "$rent_file" "$PROJECT_ROOT/$WORK_DIR/rent_figures"
            fi
        done
#    fi
fi


# read vpr results (vpr_files)
if [ "$READ_VPR" == "on" ]; then
    echo "Processing VPR results with readvpr.py from $POST_DIR working in $WORK_DIR"
    python3 "$POST_DIR/readvpr.py" "$PROJECT_ROOT/$WORK_DIR/vpr_files" "$PROJECT_ROOT/$WORK_DIR"
fi

cd - > /dev/null || exit
