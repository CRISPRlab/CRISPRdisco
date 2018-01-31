#!/bin/bash
set -e

echo "___________Testing CLI (usage should print)___________"
./disco.sh --help

echo "___________Testing CRISPRdisco test run___________"
rm -Rf test/test_output/*.*
./disco.sh --workingdir test/temp_test_output --outdir test/test_output --refset typing --date TEST test/test_infile.csv

echo "___________Replication of CRISPRdisco output___________"
diff -s test/known_results test/test_output

echo "___________Tests pass___________"
