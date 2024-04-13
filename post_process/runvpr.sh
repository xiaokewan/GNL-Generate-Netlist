#!/bin/bash

# README:
# This script is designed to run VPR (Verilog-to-Routing) tool on BLIF files.
#
# Usage:
# ./script.sh <work_dir_path> <vpr_run_status> [<blif_file1> <blif_file2> ...]
#
# Parameters:
# <work_dir_path>: Path to the directory containing BLIF files or a single BLIF file.
# <vpr_run_status>: "on" to run VPR, "off" to skip VPR execution.
# [<blif_file1> <blif_file2> ...]: Optional list of BLIF files to process. If not provided, all BLIF files in the specified directory will be processed.
#
# Example:
# ./script.sh /path/to/work_dir on blif_file1.blif blif_file2.blif

# Accepts the working directory path and VPR run status as input parameters
WORK_DIR=$1
VPR_RUN=$2
PAR="on"
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

export VTR_ROOT=~/Software/vtr-verilog-to-routing-master
source "./config.sh"

if [ -z "$WORK_DIR" ]; then
    echo "Usage: $0 <work_dir_path> <vpr_run_status> [<blif_file1> <blif_file2> ...]"
    exit 1
fi

# If no BLIF file parameters are provided, process all BLIF files
if [ -z "$3" ]; then
    BLIF_FILES="*.blif"
else
    BLIF_FILES=${@:3}
fi

if [ "$VPR_RUN" == "on" ] && [ "$PAR" != "on" ]; then
    if [ -d "$WORK_DIR" ]; then
        cd $PROJECT_ROOT/$WORK_DIR
        mkdir -p vpr_files

        for blif_file in $BLIF_FILES; do
            mkdir -p $PROJECT_ROOT/$WORK_DIR/vpr_files/$blif_file
            cd $PROJECT_ROOT/$WORK_DIR/vpr_files/$blif_file
            echo "Running VPR for $blif_file"
            $VTR_ROOT/vpr/vpr $VTR_ROOT/vtr_flow/arch/titan/stratixiv_arch.timing.xml $PROJECT_ROOT/$WORK_DIR/$blif_file
        done

    elif [ -f "$WORK_DIR" ]; then
        echo "When providing individual BLIF files, the WORK_DIR argument should be the directory where the BLIF files are located."
        exit 1
    else
        echo "Invalid input. Please provide either a directory containing BLIF files or individual BLIF files."
        exit 1
    fi
fi

# Still no clue why the env will change of $VTR_ROOT, update your own path to vpr and vtr here👇, also make sure $PAR="on" defined before
vtr="/home/xiaokewan/Software/vtr-verilog-to-routing-master"
vpr="/home/xiaokewan/Software/vtr-verilog-to-routing-master/vpr/vpr"
if [ "$VPR_RUN" == "on" ] && [ "$PAR" == "on" ]; then
    parallel "cd $PROJECT_ROOT/$WORK_DIR/vpr_files/{} && $vpr $vtr/vtr_flow/arch/titan/stratixiv_arch.timing.xml $PROJECT_ROOT/$WORK_DIR/{}" ::: $BLIF_FILES
fi
