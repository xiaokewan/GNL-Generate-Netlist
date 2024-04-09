#!/bin/bash

# 
PROJECT_ROOT=$(dirname "$(realpath "$0")")
while [[ $PROJECT_ROOT != / && ! -e "$PROJECT_ROOT/.gitignore" ]]; do
    PROJECT_ROOT=$(dirname "$PROJECT_ROOT")
done
#PROJECT_ROOT=$(dirname "$(realpath "$0")")
echo "Current Project Path is set to: $PROJECT_ROOT"

# 
SRC_DIR="$PROJECT_ROOT/src"
POST_DIR="$PROJECT_ROOT/post_process"
SWEEP_DIR="$PROJECT_ROOT/rent_sweep"
HMETIS_DIR="$PROJECT_ROOT/hmetis-1.5-linux/hmetis"


