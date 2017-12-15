#!/bin/bash

echo "Testing CLI"
#time docker run -it --rm crisprdisco disco --help
time ./disco.sh --help

echo "Testing CRISPRdisco test run"
time ./disco.sh --workingdir test/temp_test_output --outdir test/test_output --refset typing --temp keep test/test_infile.csv

