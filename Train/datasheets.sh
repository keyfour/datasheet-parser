#!/bin/bash

URL=https://github.com/KiCad/kicad-library.git
TMP_DIR=$HOME/work/kicad-library

if [ ! -d $TMP_DIR ]; then
    git clone $URL $TMP_DIR
fi
grep -r -E "F[[:blank:]]https*.*.pdf" --include *.dcm $TMP_DIR | awk '!visited[$0]++ {print $2}'
