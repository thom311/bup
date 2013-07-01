#!/bin/bash

die() {
    echo "$@" >&2
    exit 1
}

D="$(readlink -f "$(dirname "$0")")"

echo "Run test in $D"

cd "$D" || die "Error changing into directory $D"

export BUP_DIR="$D/.bup"

bup="$D/../bup"

echo "#### Prepare \$BUP_DIR $BUP_DIR"
rm -rf "$BUP_DIR"
"$bup" init

echo "#### bup index && bup save"
"$bup" index -vu "$D/base" 
"$bup" save -v -n test "$D/base"

echo "#### Recursivly list filenames"
"$bup" walk-vfs 1 /test/latest/opt/src/bup/make_test/base/NAME1/NAME1/D1 2>&1


