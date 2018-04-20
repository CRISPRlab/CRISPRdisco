# Welcome to CRISPRdisco

CRISPRdisco (CRISPR discovery) will identify CRISPR repeat-spacer arrays and *cas* genes in genome data sets.  The input requirements are a csv file with a column called 'Path' that is the full path to the location of your genomes of interest. If the genomes are located in the same directory as the input csv, the path is not required and you can simply use the basename of the files.

Please see paper: 
A. Crawley, The AgBiome Team, J. R. Henriksen, and R. Barrangou. 2018. CRISPRdisco: an automated pipeline for the discovery and analysis of CRISPR-Cas systems. in press at The CRISPR Journal. 

The code and docker images reviewed for this paper are tagged "publication".  

## Program operation

A command line pipeline tool, a python library, and Jupyter Notebooks for optional visualization and analysis are provided, as well as Docker containers with all dependencies installed.  



```
Usage: disco [OPTIONS] INFILE

  INFILE is a csv file with a column called "Path" that has the full path to
  the genomes of #interest.  Do not include file extensions in this column.

Options:
  --workingdir TEXT       Path to working directory. Default = .
  --outdir TEXT           Path to final directory. Default = .
  --refset [full|typing]  full or subset for typing. Default = full
  --date TEXT             Date of analysis in YYYY-MM-DD format. Default is
                          today.
  --tax [no|yes]          If "yes", will merge taxonomic information. Include
                          columns titled "organism", "Taxonomic ID Kingdom",
                          "Taxonomic ID Phylum", "Taxonomic ID Class",
                          "Taxonomic ID Order", "Taxonomic ID Family",
                          "Taxonomic ID Genus". "organism" should match the
                          name of the file.
  --cas [T|F]             Perform BLAST search. Default is True
  --evalue TEXT           BLAST evalue. Default is 1e-6.
  --idcutoff INTEGER      Minimum % identity to reference protein to be
                          considered a positive hit. Default is 40%.
  --lengthcutoff INTEGER  Minimum % coverage of reference protein to be
                          considered a positive hit. Default is 50%.
  --repeats [T|F]         Perform CRISPR repeat search. Default is True
  --summary [T|F]         Generate master summary table with type analysis.
                          Default is True.
  --dbsearch TEXT         Provide the location of a protein database
  --prot TEXT             Provide the protein to search for.
  --domains TEXT          Provide the location of an HMM domain database that
                          is already compiled
  --temp [delete|keep]    Temporary files automatically deleted. Change to
                          --temp keep to retain temporary files
  --help                  Show this message and exit.
```
 
 
 
To run the program in a docker container (recommended):
 
 0. See first "Installation" option (below)
 1. Replace `disco` in the examples below with `./disco.sh`
 2. Run from the base directory and give paths below below that location (relative or full).  


To run the program, minimum input is:
```
disco input.csv
```
 
where input.csv looks like:
```
,Path
0,genome
```
For this example, in your working directory there should be two files: genome.fna and genome.faa.

genome.fna is a nucleotide fasta file of all of the contigs. genome.faa is the translated protein sequences from your genome in fasta format.
 
No periods are allowed in the names of the sequence files, only seperating the final extension! 

## Fancy additions to CRISPRdisco:
Add taxonomic information to master table: 
```
disco --tax yes infile.csv
```
In this case, infile.csv must have columns with the following columns: “organism", "Taxonomic ID Kingdom", "Taxonomic ID Phylum", "Taxonomic ID Class", "Taxonomic ID Order", "Taxonomic ID Family", "Taxonomic ID Genus". 
 
 
 
 
The default cas gene annotation looks for all cas genes. There are over 70 reference sets for all the cas proteins.  If you just want to bare minimum information for typing to speed up the pipeline, use:
```
disco --refset typing infile.csv
```
 
 
Once CRISPRdisco has identified all the cas proteins, you can perform some further analyses on them if you have databases on hand. To do these you MUST include location of database and explicitly tell the program which cas protein to search. Additionally, you must turn off the cas gene search, the repeat search, and the summary table generation. Those are done with the following flags:
```
--cas F
--repeats F
--summary F
```

 
You can search for your proteins in databases to see how distant they may be to known sequences. To search for found proteins in database use this code: 
```
disco --cas F --repeats F --summary F --dbsearch /dir/DB --prot cas# infile.csv
```
 
 
 
You can search for protein domains in your protein of choice. In order to do this, you must direct the program to a database that can be used with hmmscan (i.e. an .hmm that has already been prepared by hmmpress). Search for domains in proteins: 
```
disco --cas F --repeats F --summary F --domains /dir/DB --prot cas# infile.csv
```
 
 
 
You can also change where temporary and final output files are written to using the flags 
```
--workingdir 
```
and
```
--outdir
```
respectively.




# Installation - CLI

Use one of the following to install the CLI, from most to least recommended 

## To use docker containers:

0) On a Ubuntu or debian OS with make, git, and docker installed (use your package manager and see https://www.docker.com/get-docker):

1) Get code: `git clone https://github.com/CRISPRlab/CRISPRdisco.git; cd CRISPRdisco`

2) Run CLI inside a docker container: `./disco.sh --help`

This has to download a 3.4 GB image, which make take some time depending on your internet connection (2 min in our tests).  

See Docker Hub for past versions:

  https://hub.docker.com/r/crisprlab/crisprdisco/
  
  https://hub.docker.com/r/crisprlab/crisprdisco_notebook/

## To make your own docker image if the above code did not run properly:

0) On a Ubuntu or debian OS with make, git, and docker installed (use your package manager and see https://www.docker.com/get-docker):

1) Get code: `git clone https://github.com/CRISPRlab/CRISPRdisco.git; cd CRISPRdisco`

2) Log in to docker hub with `docker login` and make docker images for the CLI with `make setup`

3) Run CLI: `./disco.sh --help`

This has to download more than ~4 GB worth of binaries, which make take some time depending on your internet connection, as well as install the packages (4 min in our tests).  


## To install by hand:

0) On a Ubuntu or debian OS with make, git, and docker installed (either use your package manager and see https://www.docker.com/get-docker), or:

    `sudo apt-get update && sudo apt-get install -y make wget bzip2 git
    wget -qO- https://get.docker.com/ | sudo sh && sudo usermod -aG docker $USER`

1) Get code: `git clone https://github.com/CRISPRlab/CRISPRdisco.git; cd CRISPRdisco`

2) install binary prequisites (via miniconda, or install each manually)

    `sudo apt-get update --fix-missing && sudo apt-get install -y build-essential `

    `wget --quiet https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
    /bin/bash Miniconda2-latest-Linux-x86_64.sh -b -f`

    `conda install -y -c bioconda -c biocore python=2.7 conda install -y -c bioconda "python=2.7.12" "blast=2.6.0" "minced=0.2.0" "hmmer=3.1b2" "conda=4.1.11" `

3) You will need to change the main script to recognize the location of reference data sets. The current script is set up to access the reference sets in the Docker container - if you're not using the pipeline in the Docker container, it's a simple fix to point the code to the reference sets. You'll have to edit the script file CRISPRdisco/crisprdisco/cli/script.py. 

Find this bit of code in that script:

`if refset =='full':
    query_locations = glob.glob('/opt/app/data/fullrefs/*.fasta') 
elif refset =='typing':
    query_locations = glob.glob('/opt/app/data/typingrefs/*.fasta')`


Change the file path to the location where you cloned the github repo. For example, it should now look like this:

`if refset =='full':
    query_locations = glob.glob('/home/user/Desktop/CRISPRdisco/data/fullrefs/*.fasta') 
elif refset =='typing':
    query_locations = glob.glob('/home/user/Desktop/CRISPRdisco/data/typingrefs/*.fasta')`


4) install CRISPRdisco package with `pip install -e .`

5) You can then run CRISPRdisco with `disco --help`, as well as import it in python with `import CRISPRdisco`

6) (optional) Install jupyter notebook
    conda install -y -c anaconda jupyter
    conda install -y nb_conda


# Running in a Jupyter Notebook

Use one of the following to launch a jupyter notebook inside a Docker container with the CRISPRdisco python and all dependencies installed, from most to least recommended 

## To use docker containers:

0) On a Ubuntu or debian OS with make, git, and docker installed (use your package manager and see https://www.docker.com/get-docker):

1) Get code: `git clone https://github.com/CRISPRlab/CRISPRdisco.git; cd CRISPRdisco`

2) Run Jupyter inside a docker container: `./run_jupyter.sh`

3) Go to the URL displayed after the container starts and look at the file in the `notebooks/` directory for examples.  

This has to download a 9 GB image, which make take some time depending on your internet connection (8 min in our tests).  


## To make your own docker image if the above code did not run properly:

0) On a Ubuntu or debian OS with make, git, and docker installed (use your package manager and see https://www.docker.com/get-docker):

1) Get code: `git clone https://github.com/CRISPRlab/CRISPRdisco.git; cd CRISPRdisco`

2) Log in to docker hub with `docker login` and make docker images for the CLI with `make setup_nb`

3) Run Jupoyter inside a docker container: `./run_jupyter.sh`

4) Go to the URL displayed after the container starts and look at the file in the `notebooks/` directory for examples.  

This has to download a 6.5 GB base Jupyter image and ~4GB additional binary files, which make take some time depending on your internet connection, as well as install the packages (a total of 10 min in our tests).  


# Testing

After installation, you should be able to run `disco --help` (or `./disco.sh --help` for the docker versions

for the docker installation method, you can run `make test` or `./test.sh` to compare example input and expected output.


# Filetree 


to run dockerised CRISPRdisco or dockerised jupyter notebooks

    disco.sh

    run_jupyter.sh

dirs:

    CRISPRdisco/		python library

    notebooks/			jupyter lab notebooks

    data/		reference sets

build and deploy system

    Makefile

docker images

    Dockerfile

    Dockerfile.notebook

python library install files
    setup.py

testing files and examples

    test/

    test.sh


# Requirements:

avoid caring about this by using docker containers (see above)

binary requirements:

  python 2.7 (tested on 2.7.12)

  blast+ (tested on 2.6.0+)

  minced (tested on 0.2.0)

  hmmer (tested on 3.1b2)

python library dependences (automatically fulfilled if installed with pip or using docker):

  pandas (tested on 0.22.0)

  biopython (tested on 1.70)

  click (tested on 6.7)

  numpy (tested on 1.14.0)

interactive notebook also needs:

  jupyter (tested on 4.2.1)

  seaborn (tested on 0.7.1)

  matplotlib (tested on 1.5.3)

development and deploy stack:

  docker (tested on 17.05.0-ce, build 89658be)

  miniconda (tested on 4.2.12)

  pip (tested on version 1.9.1)

  make (tested on version 3.81)

  git (tested on version 1.9.1)



