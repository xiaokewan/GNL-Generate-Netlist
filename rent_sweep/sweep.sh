#!/bin/bash

# This script facilitates the generation of BLIF files from GNl specifications
# and optionally runs VPR on them. It's designed to sweep over a range of Rent's
# exponent values, allowing for a comprehensive exploration of netlist characteristics.
#
# Example usage:
# ./rent_sweep/sweep.sh -p test1 -v on -r "0.3 0.98 0.02"
# ./rent_sweep/sweep.sh -p <output_dir_path> -v [on|off] -s [on|off] -r <p_start p_end p_step>
# keep the current path in the GNL level
#
# Parameters:
# -p --oupdir: Mandatory. The output directory path where generated files will be saved.
# -v --vpr: Optional. Whether VPR (Verilog-to-Routing) is run ('on') or not ('off'). Default is 'off'.
# -s --sweep: Optional. Sweep over Rent parameters using the GNL tool. Default is 'on'.
# -r --range: Optional. Range for Rent's exponents to sweep over, given as "start end step". Default is "0.3 0.98 0.02".


if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi
source "./config.sh"

export VTR_ROOT=~/Software/vtr-verilog-to-routing-master
VPR_RUN="off" #
FOLDER_NAME="temp" #
SWEEP_RUN="on"
P_RANGE="0.4 0.8 0.01"

if [ $# -eq 0 ]; then
    echo "Error: No arguments provided."
    echo "Usage: $0 -p <output_dir_path> -v [on|off] -s [on|off] -r <p_start p_end p_step>"
    exit 1
fi

# Parse command line options
TEMP=$(getopt -o v:p:s:r: --long vpr:,oupdir:,sweep:,range: -n 'script.sh' -- "$@")
if [ $? -ne 0 ]; then
    echo "Usage: $0 -p <output_dir_path> -v [on|off] -s [on|off] -r <p_start p_end p_step>"
    exit 1
fi
eval set -- "$TEMP"

while true; do
  case "$1" in
    -v | --vpr )
      VPR_RUN=$2
      shift 2
      ;;
    -p | --oupdir )
      FOLDER_NAME=$2
      shift 2
      ;;
    -s | --sweep )
      SWEEP_RUN=$2
      shift 2
      ;;
    -r | --range )
      P_RANGE=$2
      shift 2
      ;;
    -- )
      shift
      break
      ;;
    * )
      echo "Internal error!"
      exit 1
      ;;
  esac
done



#if [ -z "$FOLDER_NAME" ]; then
#    echo "Usage: $0 -p <output_dir_path> -vpr [on|off]"
#    exit 1
#fi

mkdir -p "$PROJECT_ROOT"/rent_sweep/"$FOLDER_NAME" || exit 1
cd "$PROJECT_ROOT"/rent_sweep/"$FOLDER_NAME" || exit 1



if [ "$SWEEP_RUN" == "on" ]; then
    read -r start end step <<< "$P_RANGE"
    for p in $(seq $start $step $end); do
        filename="rent_exp_${p}.gnl"
        echo "Generating $filename with p=$p"
        cat > $filename <<EOL
# rent's exponent = $p
# fixed all others parameters with sweeping p

[library]
name=lib
latch=latch   1 1
gate=inv    1 1
gate=and2   2 1
gate=nand3  3 1
gate=or4    4 1
gate=xor2   2 1

[circuit]
name=rent_exp_$p
libraries=lib
distribution=2000 6000 4000 4000 2000 2000

size=1
p=$p
sigmaG=0
sigmaT=0

size=20000
p=$p
#  meanG=0.5
sigmaG=0
sigmaT=0
EOL
    # generate blif file from gnl
        $PROJECT_ROOT/build/gnl -w blif $filename -sp
    done
fi

if [ "$VPR_RUN" == "on" ]; then
    mkdir vpr_files
    read -r start end step <<< "$P_RANGE"
    for p in $(seq $start $step $end); do
        filename="rent_exp_${p}.gnl"
        mkdir -p ./vpr_files/$filename
        cd ./vpr_files/$filename
        # run the vpr
        bliffile="rent_exp_${p}.blif"
        echo "Running VPR for $bliffile"
#        $VTR_ROOT/vpr/vpr $VTR_ROOT/vtr_flow/arch/timing/EArch.xml ../../$bliffile
        $VTR_ROOT/vpr/vpr /vtr_flow/arch/titan/stratixiv_arch.timing.xml ../../$bliffile
        cd ../..
    done
fi




echo "All sweep processes are done!"
