#!/bin/bash

echo "Testing CLI"
time ./disco.sh --help

echo "Testing CRISPRdisco test run"
time ./disco.sh --workingdir test/temp_test_output --outdir test/test_output --refset typing --date 2017-12-20 test/test_infile.csv

echo "Replication of CRISPRdisco output (differences)"
diff test/test_output test/known_results

rm -Rf test/test_output/*.* 
