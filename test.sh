#!/bin/bash
set -e

echo "___________Testing CLI (usage should print)___________"
time ./disco.sh --help

echo "___________Testing CRISPRdisco test run___________"
time ./disco.sh --workingdir test/temp_test_output --outdir test/test_output --refset typing --date 2017-12-20 test/test_infile.csv

echo "___________Replication of CRISPRdisco output (differences)___________"
diff test/known_results test/test_output 

rm -Rf test/test_output/*.* 

echo "___________Tests pass___________"
