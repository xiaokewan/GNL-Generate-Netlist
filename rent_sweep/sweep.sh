#!/bin/bash


if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

export VTR_ROOT=~/Software/vtr-verilog-to-routing-master

mkdir sweep
cd ./sweep
mkdir vpr_files
for p in $(seq 0.4 0.1 1.0); do
    filename="rent_exp_${p}.gnl"
    echo "Generating $filename with p=$p"
    cat > $filename <<EOL
# rent's exponent = $p
# fixed all others parameters with sweeping p

[library]
name=lib
latch=latch 1 1
gate=inv    1 1
gate=and2   2 1
gate=nand3  3 1

[circuit]
name=rent_exp_$p
libraries=lib
distribution=100 200 300 300

size=1
  p=$p
  q=0.4
size=900
  I=350
  O=150
EOL


    gnl -w blif $filename
    
    cd ./vpr_files
    # run VPR
    bliffile="rent_exp_${p}.blif" 
    echo "Running VPR for $bliffile"
    $VTR_ROOT/vpr/vpr $VTR_ROOT/vtr_flow/arch/timing/EArch.xml ../$bliffile
    cd ..	
done

echo "All processes are done!"

