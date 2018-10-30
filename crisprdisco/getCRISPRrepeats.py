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

#import shutil
from Bio import AlignIO, SeqIO
from Bio.Align import MultipleSeqAlignment, AlignInfo
import glob
import multiprocessing
import os, subprocess
import pandas as pd
import datetime
import numpy as np

def minced(file_path, workingdir=os.getcwd(),dry_run=False):
    file_name = os.path.basename(file_path)
    minced_str = 'minced -gffFull', file_path, os.path.join(workingdir, file_name + '.crispr')
    #minced_str = ['minced -gffFull -minNR 2', file_path, os.path.join(workingdir, file_name + '.crispr')]   
    minced_cmd = ' '.join(minced_str)
    if dry_run == True:
        print minced_cmd
    elif dry_run ==False:
        #minced_out, minced_err = subprocess.Popen(minced_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
         _ = subprocess.Popen(minced_cmd, shell=True).communicate()

def globFilesTOFrame(workingdir, file_locations):
    file_locations_frame = pd.DataFrame(file_locations,columns=['Path'])
    for index, row in file_locations_frame.iterrows():
        genome = os.path.basename(row['Path'])
        minced_location = os.path.join(workingdir,genome)
        file_locations_frame.loc[index, 'genome']= genome
        file_locations_frame.loc[index, 'minced location'] = minced_location+'.fna.crispr'
    #print files_frame
    return file_locations_frame

def getCRISPRnumber(mincedoutput):
    CRISPR_locus = mincedoutput.split(';')[0]
    DRnumber = mincedoutput.split(';')[-1]
    return str(CRISPR_locus +',' + DRnumber)

def filterMINCED(loaded_gff, local_location):
    colheaders = ['seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes']
    repeat_df = pd.DataFrame(columns=colheaders)
    #genome_name = local_location.split('.')[0]
    for name, group in loaded_gff.groupby(by='CRISPR locus number'):
        results_list = list()
        lengths_list = list()
        unique_reps = list()
        uniq_rep_nums =list()
        repeat_num = 0
        number_reps = len(group)
        if name == '':
            pass
        else:
            for index, row in group.iterrows():
                contig_ID = row['seqid']
                source = row['source']
                type_col = row['type']
                seq_start = row['start']
                seq_end = row['end']
                strand = row['strand']
                phase = row['phase']
                GeneOfInterest = row["DR number"]
		initial_start = row['start']
                if 'CRISPR' in type_col:
                    initial_start = row['start']
                    final_end = row['end']
                    #numDRs = row['score']
                else:
                    repeat_num += 1
                    LocationString = local_location + '.fna'
                    for record in SeqIO.parse(open(LocationString), 'fasta'):
                        if contig_ID in record.name:
                            record.seq = record.seq[int(seq_start):int(seq_end)]
                            record.id = GeneOfInterest
                            record.name = GeneOfInterest
                            results_list.append(record)
                            lengths_list.append(len(record.seq))
                            if record.seq not in unique_reps:
                                unique_reps.append(record.seq)
                                uniq_rep_nums.append(repeat_num)
                            repeat_Seq = record.seq
            if len(lengths_list) >0:
                avgrep = np.mean(uniq_rep_nums)
                dist1st = avgrep -1
                distlast = number_reps - avgrep
                if distlast > dist1st:
                    strand = '-'
                else:
                    strand = '+'
                #print name, avgrep, number_reps, dist1st, distlast, strand
                if max(lengths_list) == min(lengths_list):
                    alignment = MultipleSeqAlignment(results_list)
                    summary_align = AlignInfo.SummaryInfo(alignment)
                    consensus = summary_align.gap_consensus()
                    if strand == '-':
                        consensus = consensus.reverse_complement()
                    summary_line = pd.DataFrame(columns=colheaders, data=[[os.path.basename(local_location), source, type_col, initial_start, final_end, number_reps, strand, name.split('=')[-1], str(consensus)]])
                    #return 'equal lengths'
                    if 'ID' not in name:
                        repeat_df = repeat_df.append(summary_line)
                    else:
                        pass
                else:
                    consensus = repeat_Seq
                    if strand == '-':
                        consensus = consensus.reverse_complement()
                    summary_line = pd.DataFrame(columns=colheaders, data=[[os.path.basename(local_location), source, type_col, initial_start, final_end, number_reps, strand, name.split('=')[-1], str(consensus)]])
                    if 'ID' not in name:
                        repeat_df = repeat_df.append(summary_line)
                    else:
                        pass
    return repeat_df

def filterMINCEDwrapper(input_frame, output_dir, today):
    colheaders = ['seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes']
    final_df = pd.DataFrame(columns=colheaders)
    No_CRISPR_list = list()
    for index, row in input_frame.iterrows():
        minced_location = input_frame.loc[index, 'minced location']
        local_location = input_frame.loc[index, 'Path']
	#print minced_location
        loaded_gff = pd.read_csv(minced_location, sep = "\t", comment = "#", names = colheaders, index_col=False)
        #print len(loaded_gff)
        if len(loaded_gff) > 0:
            loaded_gff['CRISPR locus number'], loaded_gff['DR number']= loaded_gff['attributes'].apply(getCRISPRnumber).str.split(',', 1).str
            #print loaded_gff.head()
            #assert type(local_location) is str
            org_CRISPRS = filterMINCED(loaded_gff, local_location)
            print 'Searching for CRISPRs in ', os.path.basename(local_location)
            final_df = final_df.append(org_CRISPRS)
            #os.remove(x)
        else:
            organism_name = row['genome']
            No_CRISPR_list.append(organism_name)
            #if os.path.isfile(minced_location):
            #    os.remove(minced_location)
    final_df.to_csv(os.path.join(output_dir, 'CRISPR_repeat_seqs_'+today+'.csv'))
    No_CRISPR_list = pd.DataFrame(No_CRISPR_list, columns=['organism'])
    No_CRISPR_list.to_csv(os.path.join(output_dir,'Genomes_without_CRISPR_' +today+'.csv'))

def repeatSummaryTbls(output_dir, today):
    AIMs_without_CRISPR = pd.read_csv(os.path.join(output_dir,'Genomes_without_CRISPR_'+today+'.csv'),index_col=0)
    AIMs_without_CRISPR = AIMs_without_CRISPR.reset_index(drop=True)
    location_of_CRISPR_loci = pd.read_csv(os.path.join(output_dir,'CRISPR_repeat_seqs_'+today+'.csv'), index_col=0)
    location_of_CRISPR_loci.reset_index(inplace=True)
    AIMs_with_CRISPR = pd.DataFrame(columns=['organism', 'Number of CRISPRs'])
    #AIMs_with_CRISPR = AIMs_with_CRISPR.reset_index(drop=True)
    for index, row in AIMs_without_CRISPR.iterrows():
        AIMs_without_CRISPR.loc[index, 'Number of CRISPRs'] = 0
    if len(location_of_CRISPR_loci)>0:
        location_of_CRISPR_loci = location_of_CRISPR_loci.rename(columns={'seqid':'organism'})
        for name, group in location_of_CRISPR_loci.groupby(by='organism'):
            number_of_loci = len(group)
            summary_numbers = pd.DataFrame([[name, number_of_loci]],columns=['organism','Number of CRISPRs'])
            AIMs_with_CRISPR = AIMs_with_CRISPR.append(summary_numbers)
        #assert list(AIMs_with_CRISPR.columns.values) ==list(AIMs_without_CRISPR.columns.values)
        frames = [AIMs_with_CRISPR, AIMs_without_CRISPR]
        repeat_summary = pd.concat(frames)
        #assert len(repeat_summary) == len(AIMs_with_CRISPR) + len(AIMs_without_CRISPR)
    elif len(location_of_CRISPR_loci)<1:
        repeat_summary = AIMs_without_CRISPR
    repeat_summary.to_csv(os.path.join(output_dir, 'repeat_summary_table_'+today+'.csv'))
    return repeat_summary

def repeatAnalysis(file_locations, today, working_outdir=os.getcwd(), final_outdir=os.getcwd(), dry_run_setting=False, inhouse_setting=True,col1='minced location', col2='mnt location'):
    for x in file_locations:
        minced(x+'.fna', working_outdir,dry_run=dry_run_setting)
    output_frame = globFilesTOFrame(working_outdir, file_locations)
    filterMINCEDwrapper(output_frame, final_outdir, today)
    summary_table = repeatSummaryTbls(final_outdir, today)
