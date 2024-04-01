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
# Usage: ./script_name.sh <work_dir_path> -n [on|off] -r [on|off]
# Parameters:
#   <work_dir_path>: Mandatory. The path to the working directory containing BLIF files and where output files will be generated.
#   -n [on|off]: Optional. whether to run netlist2rent.py and rent2viz.py. Default is 'on'.
#   -r [on|off]: Optional. whether to run readvpr.py to process VPR results. Default is 'off'.

WORK_DIR=$1
NETLIST_RENT_VIZ="on"
READ_VPR="off"

shift # shift arguments

while getopts ":n:r:" opt; do
  case ${opt} in
    n )
      NETLIST_RENT_VIZ=$OPTARG
      ;;
    r )
      READ_VPR=$OPTARG
      ;;
    \? )
      echo "Usage: $0 <work_dir_path> -n [on|off] -r [on|off]"
      exit 1
      ;;
    : )
      echo "Usage: $0 <work_dir_path> -n [on|off] -r [on|off]"
      exit 1
      ;;
  esac
done

if [ -z "$WORK_DIR" ]; then
    echo "Usage: $0 <work_dir_path> -n [on|off] -r [on|off]"
    exit 1
fi

POST_PY_PATH="../../post-process"
HMETIS_PATH="../../hmetis-1.5-linux/hmetis"

cd "$WORK_DIR" || exit

# netlist2rent.py and rent2viz.py
if [ "$NETLIST_RENT_VIZ" == "on" ]; then
    for blif_file in *.blif; do
        echo "Processing $blif_file with netlist2rent.py"
        python3 "$POST_PY_PATH/netlist2rent.py" "$blif_file" "." "$HMETIS_PATH"
    done

    for rent_file in *.rent; do
        echo "Visualizing $rent_file with rent2viz.py"
        python3 "$POST_PY_PATH/rent2viz.py" "$rent_file"
    done
fi

# read vpr results (vpr_files)
if [ "$READ_VPR" == "on" ]; then
    echo "Processing VPR results with readvpr.py"
    python3 "../readvpr.py" "./vpr_files" "./"
fi

cd - > /dev/null || exit