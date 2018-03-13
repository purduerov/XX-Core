#!/bin/bash
pxydir="pakfront"
outname="panzerkanone"
# Run executablees in panzerkanone
./$pxydir/bin/$outname > log.txt &
echo $! > pakfrontpid
