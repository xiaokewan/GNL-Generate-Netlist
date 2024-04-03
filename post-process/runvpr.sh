
WORK_DIR=$1
VPR_RUN="on"


if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

export VTR_ROOT=~/Software/vtr-verilog-to-routing-master
source "./config.sh"

if [ -z "$WORK_DIR" ]; then
    echo "Usage: $0 <work_dir_path>"
    exit 1
fi

cd $PROJECT_ROOT/$WORK_DIR
if [ "$VPR_RUN" == "on" ]; then
    mkdir vpr_files
    for blif_file in *.blif; do
        mkdir -p $PROJECT_ROOT/$WORK_DIR/vpr_files/$blif_file
        cd $PROJECT_ROOT/$WORK_DIR/vpr_files/$blif_file
        # run the vpr
        echo "Running VPR for $bliffile"
        # pay attention to the architecture!!
        $VTR_ROOT/vpr/vpr $VTR_ROOT/vtr_flow/arch/titan/stratixiv_arch.timing.xml $PROJECT_ROOT/$WORK_DIR/$blif_file
    done
fi


