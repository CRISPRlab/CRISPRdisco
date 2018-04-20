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

import glob
import multiprocessing
import os, subprocess
import pandas as pd
from Bio import SeqIO
import datetime

def makeBLASTdb(subject, workingdir = os.getcwd(), dry_run=False):
    '''This function generates the blast database.  "subject" should be the full path to the subject file (to be used as DB)."workingdir" is the directory where the db will be written. Default output directory location is working directory.'''
    #blastpath = '/opt/blast_latest/ncbi-blast-2.2.29+/bin/'
    subject_file = os.path.basename(subject)
    FNULL = open(os.devnull, 'w')
    blastdb_cmd = ['makeblastdb', '-in', subject, '-dbtype', 'prot', '-out', os.path.join(workingdir, subject_file)]
    blastdb_str = " ".join(blastdb_cmd)
    if dry_run==True:
        pass
        #print blastdb_str
    if dry_run==False:
        #blastdb_out, blastdb_err = subprocess.Popen(blastdb_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        blastdb_out, blastdb_err = subprocess.Popen(blastdb_str, shell=True, stderr=FNULL).communicate()

def protBLAST(subject, query, blastevalue, workingdir = os.getcwd(), dry_run=False):
    '''This function performs blastp.  "subject" should be the full path to the subject file as used in the makeBLASTdb function. query should be the full path to the query file (ex: a .fasta file with the refernce set of proteins to use); include the file extenstion in the name. Default evaule is 1e-6. "workingdir" is the directory where the db is written. Default directory locations are working directory.'''
    CPU = multiprocessing.cpu_count()
    blastpath = '/opt/blast_latest/ncbi-blast-2.2.29+/bin/'
    query_fasta_file = os.path.basename(query)
    subject_file = os.path.basename(subject)
    blastoutfile = query_fasta_file + '.VS.' + subject_file + '.blastp'
    blast_results_file_path = os.path.join(workingdir, blastoutfile)
    blast_cmd = ['blastp',
            '-query', query,
            '-db', os.path.join(workingdir, subject_file),
            '-evalue', str(blastevalue),
            '-outfmt', "'7 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovs qcovhsp staxids'",
            '-num_threads', str(CPU),
            '-out', blast_results_file_path
            ]
    blast_str = " ".join(blast_cmd)
    if dry_run == False:
        #blast_out, blast_err = subprocess.Popen(blast_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        #assert len(blast_err)<1, 'There is a BLAST error: %r' % blast_err
        _ = subprocess.Popen(blast_str, shell=True).communicate()
    if dry_run ==True:
        print blast_str

def protDBBLAST(subject, query, blastevalue, workingdir = os.getcwd(), dry_run=False):
    '''This function performs blastp.  "subject" should be the full path to the subject file as used in the makeBLASTdb function. query should be the full path to the query file (ex: a .fasta file with the refernce set of proteins to use); include the file extenstion in the name. Default evaule is 1e-6. "workingdir" is the directory where the db is written. Default directory locations are working directory.'''
    CPU = multiprocessing.cpu_count()
    blastpath = '/opt/blast_latest/ncbi-blast-2.2.29+/bin/'
    query_fasta_file = os.path.basename(query)
    subject_file = os.path.basename(subject)
    blastoutfile = query_fasta_file + '.VS.' + subject_file + '.blastp'
    blast_results_file_path = os.path.join(workingdir, blastoutfile)
    blast_cmd = ['blastp',
            '-query', query,
            '-db', subject,
            '-evalue', int(blastevalue),
            '-outfmt', "'7 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovs qcovhsp staxids'",
            '-num_threads', str(CPU),
            '-out', blast_results_file_path
            ]
    blast_str = " ".join(blast_cmd)
    if dry_run == False:
        #blast_out, blast_err = subprocess.Popen(blast_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        #assert len(blast_err)<1, 'There is a BLAST error: %r' % blast_err
        _ = subprocess.Popen(blast_str, shell=True).communicate()
    if dry_run ==True:
        print blast_str

        
        
def prot_filter(query, today, ID_cutoff, coverage_cutoff, workingdir=os.getcwd(),  output_dir=os.getcwd(),  dry_run=False):
    '''This function will gather the blastp files from the query defined, and filter blastp output files. workingdir is the folder where the blastp results are located. output_dir is where the results of the filtering will be put. The default % ID is 40% and the default coverage is 50%.'''
    query_fasta_file = os.path.basename(query)
    files = glob.glob(os.path.join(workingdir, query_fasta_file) + '*.blastp')
    if dry_run == True:
        print files
    #starting df for summary chart
    ref_set = query_fasta_file
    Cas_dict = {'cas9_':'TypeII', 'cas3_':'TypeI', 'cas3f_':'TypeI-F', 'cas10_':'TypeIII', 'csf4_':'TypeIV', 'cas12a_':'TypeV-A', 'cas12b_':'TypeV-B', 'cas12c_':'TypeV-C', 'cas13a_':'TypeVI-A', 'cas13b_':'TypeVI-B', 'cas13c_':'TypeVI-C', '2OG_':'TypeI,TypeIII', 'DEDDh_': 'TypeI', 'DinG_':'TypeIV', 'PD-DExK_':'TypeI,TypeIII', 'PrimPol_':'TypeI,TypeIII', 'WYL_':'TypeI,TypeIII', 'cas10d_':'TypeI-D', 'cas11_':'TypeI', 'cas1_':'universal', 'cas2_':'universal', 'cas4_':'TypeI,TypeII-B,TypeV', 'cas5_':'TypeI', 'cas6_':'TypeI,TypeIII,TypeIV', 'cas7_':'TypeI', 'cas8a_':'TypeI-A', 'cas8b_':'TypeI-B', 'cas8c_':'TypeI-C', 'cas8e_':'TypeI-E', 'cas8f_':'TypeI-F', 'cas8u_':'TypeI-U', 'casR_':'TypeI', 'cmr1g':'TypeIII', 'cmr3g':'TypeIII', 'cmr4g':'TypeIII', 'cmr5g':'TypeIII', 'cmr6g':'TypeIII', 'cmr7_':'TypeIII', 'cmr8g':'TypeIII', 'csa3_':'TypeI-A', 'csa5g':'TypeI-A', 'csb1g':'TypeI-U', 'csb2g':'TypeI-U', 'csb3_':'TypeI-U', 'csc1g':'TypeI-D', 'csc2g':'TypeI-D', ' cse2g':'TypeI-E', 'csf1g':'TypeIV', 'csf2g':'TypeIV', 'csf3g':'TypeIV', 'csf4g':'TypeIV', 'csf5g':'TypeIV', 'csm2g':'TypeIII', 'csm3g':'TypeIII', 'csm4g':'TypeIII', 'csm5g':'TypeIII', 'csm6_':'TypeIII', 'csn2_':'TypeII-A', 'csx10g':'TypeIII', 'csx15_':'TypeIII', 'csx16_':'TypeIII', 'csx18_':'TypeIII', 'csx19_':'TypeIII', 'csx1_':'TypeIII', 'csx20_':'TypeIII', 'csx21_':'TypeIII', 'csx22_':'TypeIII', 'csx23_':'TypeIII', 'csx24_':'TypeIII', 'csx25_':'TypeIII', 'csx26_':'TypeIII', 'csx3_':'TypeIII', 'c2c9_':'TypeV-U', 'c2c8_':'TypeV-U', 'c2c5_':'TypeV-U', 'c2c10_':'TypeV-U', 'c2c4_':'TypeV-U', 'CasX_':'class2', 'CasY_':'class2'}
    for cas_keys in Cas_dict:
        if cas_keys in query_fasta_file:
            ref_set = cas_keys[:-1]
    df_summary = pd.DataFrame(columns=['organism', 'No. Cas Proteins from ' + ref_set])
    #starting df for blastp results
    df_Cas_blast_result = pd.DataFrame(columns=['query id', 'subject id', '% identity', 'alignment length', 'mismatches', 'gap opens', 'q. start', 'q. end', 's. start', 's. end', 'evalue', 'bit score', '% query coverage per subject', '% query coverage per hsp', 'subject tax ids'])
    #read in blastp file, filter by 40% ID and 50% coverage, output two csv files: one with Number of Cas proteins, one with the blastp files condensed into a single chart
    for blastfile in files:
        colheaders=['query id', 'subject id', '% identity', 'alignment length', 'mismatches', 'gap opens', 'q. start', 'q. end', 's. start', 's. end', 'evalue', 'bit score', '% query coverage per subject', '% query coverage per hsp', 'subject tax ids']
        blast = pd.read_csv(blastfile, sep = "\t", comment = "#", names = colheaders, index_col=False)
        genome_number = os.path.basename(blastfile)
        blastfile_strsplit = genome_number.split('.')
        organism = blastfile_strsplit[3]
        if dry_run == True:
            print organism
            print len(blastfile)
        else:
            pass
        ID_filter = blast[blast['% identity'] > int(ID_cutoff)]
        ID_cov_filter = ID_filter[ID_filter['% query coverage per hsp'] > int(coverage_cutoff)]
        grouped=ID_cov_filter.groupby('subject id')
        df_Cas_by_groups = pd.DataFrame(columns=['query id', 'subject id', '% identity', 'alignment length', 'mismatches', 'gap opens', 'q. start', 'q. end', 's. start', 's. end', 'evalue', 'bit score', '% query coverage per subject', '% query coverage per hsp', 'subject tax ids'])
        for n, group in grouped: 
            Cas=group.sort_values(by='bit score', ascending=False).head(1)
            if dry_run == True:
                print Cas
            else:
                pass
            for index, row in Cas.iterrows():
                protname = row['subject id']
                if '_' in protname:
                    protname = protname.split('_')[-1]
                filename = genome_number.split('.')[-3]
                Cas.loc[index, 'subject id'] = filename + '_' + protname
            df_Cas_by_groups = df_Cas_by_groups.append(Cas)
        numberCas = len(df_Cas_by_groups)
        df1 = pd.DataFrame([[organism, numberCas]], columns =['organism', 'No. Cas Proteins from ' + ref_set])
        df_Cas_blast_result = df_Cas_blast_result.append(df_Cas_by_groups)
        df_summary = df_summary.append(df1)
    no_duplicates = df_Cas_blast_result.drop_duplicates()
    if dry_run == True:
        print no_duplicates
    if dry_run == False:
        output_file_str = ref_set + '_blast_results_Seqs_' + today + '.csv'
        no_duplicates.to_csv(os.path.join(output_dir, output_file_str))
        output_summary_str = ref_set + '_summary_list_' + today + '.csv'
        df_summary.to_csv(os.path.join(output_dir, output_summary_str))
        return no_duplicates

def get_prots(subject_locations, query, today, sequence_type='.faa', dry_run=False, output_dir = os.getcwd()):
    '''Query is the full path to the query used in blast and filter. For date_of_analysis, date format is YYYY-MM-DD. "subject_directory" path to directory where genomes are located. Sequence type can be '.faa' for amino acids or '.ffn' of nucleotides. "protfilter_location" is the output_dir from protFilter function. "output_dir" is where the protein sequences should be written. '''
    Cas_dict = {'cas9_':'TypeII', 'cas3_':'TypeI', 'cas3f_':'TypeI-F', 'cas10_':'TypeIII', 'csf4_':'TypeIV', 'cas12a_':'TypeV-A', 'cas12b_':'TypeV-B', 'cas12c_':'TypeV-C', 'cas13a_':'TypeVI-A', 'cas13b_':'TypeVI-B', 'cas13c_':'TypeVI-C', '2OG_':'TypeI,TypeIII', 'DEDDh_': 'TypeI', 'DinG_':'TypeIV', 'PD-DExK_':'TypeI,TypeIII', 'PrimPol_':'TypeI,TypeIII', 'WYL_':'TypeI,TypeIII', 'cas10d_':'TypeI-D', 'cas11_':'TypeI', 'cas1_':'universal', 'cas2_':'universal', 'cas4_':'TypeI,TypeII-B,TypeV', 'cas5_':'TypeI', 'cas6_':'TypeI,TypeIII,TypeIV', 'cas7_':'TypeI', 'cas8a_':'TypeI-A', 'cas8b_':'TypeI-B', 'cas8c_':'TypeI-C', 'cas8e_':'TypeI-E', 'cas8f_':'TypeI-F', 'cas8u_':'TypeI-U', 'casR_':'TypeI', 'cmr1g':'TypeIII', 'cmr3g':'TypeIII', 'cmr4g':'TypeIII', 'cmr5g':'TypeIII', 'cmr6g':'TypeIII', 'cmr7_':'TypeIII', 'cmr8g':'TypeIII', 'csa3_':'TypeI-A', 'csa5g':'TypeI-A', 'csb1g':'TypeI-U', 'csb2g':'TypeI-U', 'csb3_':'TypeI-U', 'csc1g':'TypeI-D', 'csc2g':'TypeI-D', ' cse2g':'TypeI-E', 'csf1g':'TypeIV', 'csf2g':'TypeIV', 'csf3g':'TypeIV', 'csf4g':'TypeIV', 'csf5g':'TypeIV', 'csm2g':'TypeIII', 'csm3g':'TypeIII', 'csm4g':'TypeIII', 'csm5g':'TypeIII', 'csm6_':'TypeIII', 'csn2_':'TypeII-A', 'csx10g':'TypeIII', 'csx15_':'TypeIII', 'csx16_':'TypeIII', 'csx18_':'TypeIII', 'csx19_':'TypeIII', 'csx1_':'TypeIII', 'csx20_':'TypeIII', 'csx21_':'TypeIII', 'csx22_':'TypeIII', 'csx23_':'TypeIII', 'csx24_':'TypeIII', 'csx25_':'TypeIII', 'csx26_':'TypeIII', 'csx3_':'TypeIII', 'c2c9_':'TypeV-U', 'c2c8_':'TypeV-U', 'c2c5_':'TypeV-U', 'c2c10_':'TypeV-U', 'c2c4_':'TypeV-U', 'CasX_':'TypeV-E', 'CasY_':'TypeV-D'}
    ref_set=os.path.basename(query)
    for cas_keys in Cas_dict:
         if cas_keys in query:
            ref_set = cas_keys[:-1]
    file_input = ref_set + '_blast_results_Seqs_' + today + '.csv'
    if dry_run==True:
        print file_input
    prots = pd.read_csv(os.path.join(output_dir, file_input))
    results_list = []
    for subject in subject_locations:
        for index, row in prots.iterrows():
            GeneOfInterest = row['subject id']
            if subject in GeneOfInterest:
                AIMnumber = GeneOfInterest.split('_')[:-1]
                proteinID = GeneOfInterest.split('_')[-1]
                LocationString = os.path.join(subject + '*' + sequence_type)
                if dry_run==True:
                    print LocationString
                genome_list = glob.glob(LocationString)
                genome = genome_list[0]
                if dry_run==True:
                    print genome_list 
                handle = open(genome)
                for record in SeqIO.parse(handle, 'fasta'):
                    if proteinID in record.name:
                        if dry_run==True:
                            print True
                        results_list.append(record)
    if dry_run==True:
        print results_list
    if dry_run==False:
        outdir_location_str = 'Prots_from_' + ref_set +'_' + today + '.fasta'
        SeqIO.write(results_list, os.path.join(output_dir, outdir_location_str), "fasta")

def casSearch(query_locations, file_locations, today, blastevalue, ID_cutoff, coverage_cutoff, working_outdir=os.getcwd(), final_outdir=os.getcwd(), dry_run_setting=False):
    '''"query_locations" locations is the folder where the reference sets are located. "file_locations" is a list of genomes to search - use the function csvFileInput or *.fasta in working directory.  "working_outdir" can be a folder for temporary files. "final_outdir" is where the final files will be written.'''
    #query_options = glob.glob(query_locations +'*.fasta')
    print "Searching using " + str(len(query_locations)) + " reference sets"
    for i, f in enumerate(file_locations):
        #if i > 100:
        #    break
        subject = str(f) + '.faa'
        makeBLASTdb(subject, workingdir=working_outdir,dry_run=dry_run_setting)
        for query in query_locations:
            protBLAST(subject, query, blastevalue, workingdir=working_outdir, dry_run=dry_run_setting)
        path = os.path.join(working_outdir, os.path.basename(subject))
        if os.path.isfile(path + '.pin'):
            os.remove(path + '.pin')
        else:
            pass
        if os.path.isfile(path + '.phr'):
            os.remove(path + '.phr')
        else:
            pass
        if os.path.isfile(path + '.psq'):
            os.remove(path + '.psq')
        else:
            pass
    for query in query_locations:
        prot_filter(query,today, ID_cutoff, coverage_cutoff, workingdir=working_outdir, dry_run=dry_run_setting, output_dir=working_outdir)
        temp_blast_file_path = os.path.join(working_outdir, os.path.basename(query))
        temp_blast_files = glob.glob(temp_blast_file_path + '*.blastp')
        for t in temp_blast_files:
            if os.path.isfile(t):
                os.remove(t)
    for query in query_locations:
        get_prots(file_locations, query, today, sequence_type='.faa', dry_run=False, output_dir=working_outdir)

def domainSearch(HMM_location, SEQ_location, working_outdir=os.getcwd(),dry_run=False):
    HMMNAME = os.path.basename(HMM_location)
    SEQNAME = os.path.basename(SEQ_location)
    tblout_str = HMMNAME +'.VS.' +SEQNAME +'.seq.tsv'
    hmmscan_cmd ='hmmscan', '--cpu 10 --tblout',os.path.join(working_outdir, tblout_str), '--domtblout', os.path.join(working_outdir, HMMNAME + '.VS.'+ SEQNAME + '.dom.tsv'), HMM_location, SEQ_location
    if dry_run == True:
        print " ".join(hmmscan_cmd)
    else:
        _ = subprocess.Popen(" ".join(hmmscan_cmd), shell=True).communicate()

def csvFileInput(path_to_file):
    '''Can use a csv file with column named 'Path' for input list of files. '''
    #print os.getcwd()
    #print os.listdir(os.getcwd())
    df_single_AIMs = pd.read_csv(path_to_file)
    df_single_AIMs_Paths = df_single_AIMs[['Path']]
    filtered_file_locations = df_single_AIMs_Paths.dropna()
    file_locations = filtered_file_locations['Path'].tolist()
    return file_locations
