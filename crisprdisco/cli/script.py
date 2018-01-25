#!/usr/bin/python
"""
CRISPRdisco: CRISPR discovery pipeline
Copyright (C) 2017 AgBiome, Inc., All rights reserved

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""


__version__ = '0.1'

description = """
CRISPRdisco, version %s
(C) AgBiome, Inc., All rights reserved
Alexandra Crawley, 2017

Identify CRISPR-Cas systems in bacteria and archaeal genomes.

This is free software and comes with ABSOLUTELY NO WARRANTY. You are welcome 
to redistribute it under certain conditions; for details see LISENCE.txt
""" % __version__



if __name__ == "__main__": print(description)


import click
import os, subprocess
import glob
import datetime
from ..casPROTidentification import *
from ..generateMasterTbl import *
from ..getCRISPRrepeats import *

@click.command()
@click.option('--workingdir', nargs=1, default =os.getcwd(), type=click.STRING, help='Path to working directory. Default = .')
@click.option('--outdir', nargs=1, default =os.getcwd(), type=click.STRING, help='Path to final directory. Default = .')
@click.option('--refset', default='full', type=click.Choice(['full','typing']), help='full or subset for typing. Default = full')
@click.option('--date', default=str(datetime.date.today()), type=click.STRING, help='Date of analysis in YYYY-MM-DD format. Default is today.')
@click.option('--tax', default='no', type=click.Choice(['no','yes']), help='If "yes", will merge taxonomic information. Include columns titled "organism", "Taxonomic ID Kingdom", "Taxonomic ID Phylum", "Taxonomic ID Class", "Taxonomic ID Order", "Taxonomic ID Family", "Taxonomic ID Genus". "organism" should match the name of the file.')
@click.option('--cas', default='T', type=click.Choice(['T','F']), help='Perform BLAST search. Default is True')
@click.option('--evalue', default='1e-6', type=click.STRING, help='BLAST evalue. Default is 1e-6.')
@click.option('--idcutoff', default=40.0, type=click.INT, help='Minimum % identity to reference protein to be considered a positive hit. Default is 40%.')
@click.option('--lengthcutoff', default=50.0, type=click.INT, help='Minimum % coverage of reference protein to be considered a positive hit. Default is 50%.')
@click.option('--repeats', default='T', type=click.Choice(['T','F']), help='Perform CRISPR repeat search. Default is True')
@click.option('--summary', nargs=1, default='T', type=click.Choice(['T','F']), help='Generate master summary table with type analysis. Default is True.')
@click.option('--dbsearch', nargs=1, type=click.STRING, help='Provide the location of a protein database')
@click.option('--prot', nargs=1, type=click.STRING, help='Provide the protein to search for.')
@click.option('--domains', nargs=1, type=click.STRING, help='Provide the location of an HMM domain database that is already compiled')
@click.option('--temp', nargs=1, default='delete', type=click.Choice(['delete','keep']), help='Temporary files automatically deleted. Change to --temp keep to retain temporary files')
@click.argument('infile')
def disco(workingdir, outdir, refset, date, tax, cas, evalue, idcutoff, lengthcutoff, repeats, summary, dbsearch, prot, domains, temp, infile):
    """INFILE is a csv file with a column called "Path" that has the full path to the genomes of #interest.  Do not include file extensions in this column."""   
    subject_locations = csvFileInput(infile)
    
    if workingdir == os.getcwd():
        if os.path.isdir('raw_files'):
            pass
        else:
            os.mkdir('raw_files/')
        workingdir = 'raw_files/'
    if refset =='full':
        query_locations = glob.glob('/opt/app/data/fullrefs/*.fasta') 
    elif refset =='typing':
        query_locations = glob.glob('/opt/app/data/typingrefs/*.fasta')
    if cas =='T':
        print 'Searching for Cas proteins'
        casSearch(query_locations, subject_locations, date, evalue, idcutoff, lengthcutoff, working_outdir=workingdir, final_outdir=outdir)
    else:
        pass
    
    if repeats == 'T':   
        print 'Searching for CRISPRs'
        repeatAnalysis(subject_locations, date, working_outdir=workingdir, final_outdir=outdir, inhouse_setting=False)
    else:
        pass
    
    if summary =='T': 
        print 'Generating Master table'
        if tax == 'no':
            typeAnalysis(date, final_outdir=outdir, working_outdir=workingdir)
        elif tax == 'yes':
            taxinfofile = infile
            masterTblWithStrain(taxinfofile,tax, date, finaloutputdir=outdir,workdir=workingdir)
    
    
    if dbsearch:
        print 'Looking for DB'
        #assert os.path.isabs(dbsearch)
        query_options = glob.glob(os.path.join(workingdir, 'Prots_from_'+ prot +'*.fasta'))
        print ' '
        for query in query_options:
            protDBBLAST(dbsearch, query, evalue, workingdir=outdir)
    
    if domains:
        print 'using domains'
        query_options = glob.glob(os.path.join(workingdir, 'Prots_from_'+ prot +'*.fasta'))
        for query in query_options:
            domainSearch(domains, query, working_outdir=outdir)
            
    if temp == 'delete':
        for x in glob.glob((os.path.join(workingdir,'*'))):
            if os.path.isfile(x):
                os.remove(x)
        os.rmdir(workingdir)
    else:
        pass
