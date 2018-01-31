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
import os
import pandas as pd
import datetime

def getIsolatesTble(directory_location='/mnt/TT_PROD/isolate_exports/'):
    isolates_tables = glob.glob(os.path.join(directory_location,'*.csv'))
    dates = list()
    for x in isolates_tables:
        date = os.path.basename(x).split('_')[-1]
        YYYYMMDD = date.split('.')[0]
        dates.append(int(YYYYMMDD))
    latest= max(dates)
    return os.path.join(directory_location,'isolates_'+str(latest)+'.csv')

def generateMASTERtbl(working_outdir, final_outdir, today):
    summary_files = glob.glob(os.path.join(working_outdir,'*summary_list*'+today+'.csv'))
    repeat_summary_table = os.path.join(final_outdir,'repeat_summary_table_'+ today +'.csv')
    master_summary_table = pd.read_csv(repeat_summary_table,index_col=0)
    master_summary_table = master_summary_table.reset_index(drop=True)
    for summ in summary_files:
        read_file = pd.read_csv(summ, index_col=0)
        read_file = read_file.reset_index(drop=True)
        master_summary_table = pd.merge(master_summary_table, read_file, on='organism', how='left')
    column_names = list(master_summary_table.columns.values)
    columns_with_numbers =list()
    for headers in column_names:
        if 'No. Cas Proteins' in headers:
            columns_with_numbers.append(headers)
    for index, row in master_summary_table.iterrows():
        CasVU_dict = {'c2c9':'TypeV-U','c2c8':'TypeV-U','c2c5':'TypeV-U','c2c10':'TypeV-U', 'c2c4':'TypeV-U'}
        total_count =0
        non_VU_count=0
        organism = row['organism']
        test_loop = 0
        value_count =0
        systems_list =list()
        for x in columns_with_numbers:
            cas_prot = x.split(' ')[-1]
            #print cas_prot
            if cas_prot not in CasVU_dict.keys():
                test_loop = row[x]
                #if test_loop > 0:
                #    print cas_prot, row[x]
                #print x, test_loop
                non_VU_count += test_loop
            if cas_prot != 'RSAs':
                value_count = row[x]
                if value_count > 0:
                    systems_list.append(cas_prot)
                total_count += value_count
        master_summary_table.loc[index,'Total Cas Prots'] = total_count
        master_summary_table.loc[index,'Total non V-U Prots'] = non_VU_count
        #make order of delimiter systems deterministic for testing
        master_summary_table.loc[index, 'Genes present'] = '|'.join(sorted(systems_list))
    master_summary_table_subset = master_summary_table[['organism','Number of CRISPRs','Total Cas Prots', 'Total non V-U Prots','Genes present']]
    master_summary_table_subset.to_csv(os.path.join(working_outdir,'Master_CRISPR_summary_table_'+today+ '.csv'))
    return master_summary_table_subset

def findType(cas_prot_string):
    if type(cas_prot_string) is float:
        return ',,,,'
    elif cas_prot_string =='':
        return ',,,,'
    else:
        signature_genes = {'cas9':'TypeII','cas3':'TypeI','cas10':'TypeIII','DinG':'TypeIV','csf4':'TypeIV','cas12':'TypeV','cas13':'TypeVI','c2c':'TypeV-U','casX':'TypeV','casY':'TypeV'}
        TypeI_subtype_genes = {'cas8a':'TypeI-A','cas8b':'TypeI-B','cas8c':'TypeI-C','cas10d':'TypeI-D','cas8e':'TypeI-E','cas8f':'TypeI-F','cas8u':'TypeI-U'}
        TypeII_subtype_genes={'cas4':'TypeII-B','csn2':'TypeII-A'}
        TypeIV_subtype_genes={'TypeIV':'TypeIV'}
        TypeIII_subtype_genes={'csm6':'TypeIII-A','cmr':'TypeIII-B/TypeIII-D','csx10':'TypeIII-C'}
        TypeV_subtype_genes={'cas12a':'TypeV-A','cas12b':'TypeV-B','cas12c':'TypeV-C','CasY':'TypeV-D','CasX':'TypeV-E'}
        TypeVU_subtype_genes={'csc4':'TypeVU-1','c2c8':'TypeVU-2','c2c10':'TypeVU-3','c2c9':'TypeVU-4','c2c5':'TypeVU-5'}
        TypeVI_subtype_genes={'cas13a':'TypeVI-A','cas13b':'TypeVI-B','cas13c':'TypeVI-C'}
        system_type =list()
        subsystem = list()
        sig_prots = 0
        cas1present = ''
        for x in signature_genes.keys():
            if x in str(cas_prot_string):
                system_type.append(signature_genes[x])
                sig_prots += 1
                #print system_type
        for x in system_type:
            if x == 'TypeI':
                for y in TypeI_subtype_genes.keys():
                    if y in str(cas_prot_string):
                        subsystem.append(TypeI_subtype_genes[y])
            if x == 'TypeIII':
                for y in TypeIII_subtype_genes.keys():
                    if y in str(cas_prot_string):
                        subsystem.append(TypeIII_subtype_genes[y])
            if x == 'TypeIV':
                for y in TypeIV_subtype_genes.keys():
                    if y in str(cas_prot_string):
                        subsystem.append(TypeIV_subtype_genes[y])
            if x == 'TypeVI':
                for y in TypeVI_subtype_genes.keys():
                    if y in str(cas_prot_string):
                        subsystem.append(TypeVI_subtype_genes[y])
            if x == 'TypeV-U':
                for y in TypeVU_subtype_genes.keys():
                    if y in str(cas_prot_string):
                        subsystem.append(TypeVU_subtype_genes[y])
            if x == 'TypeV':
                for y in TypeV_subtype_genes.keys():
                    if y in str(cas_prot_string):
                        subsystem.append(TypeV_subtype_genes[y])
            if x == 'TypeII':
                if 'csn2' not in str(cas_prot_string):
                    if 'cas4' not in str(cas_prot_string):
                        subsystem.append('TypeII-C')
                    elif 'cas4' in str(cas_prot_string):
                        subsystem.append('TypeII-B')
                else:
                    for y in TypeII_subtype_genes.keys():
                        if y in str(cas_prot_string):
                            subsystem.append(TypeII_subtype_genes[y])
        if sig_prots == 0:
            missing_sigprot='missing signature protein'
        else:
            missing_sigprot = ''
        if 'cas1' not in str(cas_prot_string):
            cas1present = 'missing cas1'
        output = '|'.join(sorted(system_type)) + ',' + '|'.join(sorted(subsystem)) + ',' + str(sig_prots) + ',' + str(cas1present) +',' + str(missing_sigprot)
        return output

def missingRSA(master_tables):
    master_tables = master_tables.reset_index(drop=True)
    #mapping = {'': 0}
    #master_tables = master_tables.replace({'multiple systems': mapping, 'Number of CRISPRs': mapping})
    #master_tables = master_tables.fillna(0)
    master_tables[['multiple systems','Number of CRISPRs']] = master_tables[['multiple systems','Number of CRISPRs']].fillna(value=0)
    master_tables = master_tables.replace(to_replace='', value=0)
    for index, row in master_tables.iterrows():
        CRISPRs = row['Number of CRISPRs']
        #Systems = row['System type']
        numberSigProts = row['multiple systems']
        if int(numberSigProts)>0:
            if int(CRISPRs) == 0:
                missing_RSA ='no repeats'
            elif int(CRISPRs) > int(numberSigProts):
                missing_RSA = 'not all loci have cas genes'
            elif int(CRISPRs) < int(numberSigProts):
                missing_RSA = 'not all loci have repeats'
            else:
                missing_RSA = ''
        else:
            missing_RSA = ''
        master_tables.loc[index, 'missing RSAs'] = missing_RSA
    return master_tables

def typeAnalysis(today, final_outdir=os.getcwd(),working_outdir=os.getcwd()):
    master_summary_table = generateMASTERtbl(working_outdir, final_outdir, today)
    master_summary_table['System type'], master_summary_table['system subtype'], master_summary_table['multiple systems'], master_summary_table['cas1 missing'], master_summary_table['missing signature prot'] = master_summary_table['Genes present'].apply(findType).str.split(',', 4).str
    master_summary_table = missingRSA(master_summary_table)
    master_summary_table.to_csv(os.path.join(final_outdir,'Master_CRISPR_summary_table_'+ today +'.csv'))
    #systemcounts = master_summary_table['System type'].value_counts().to_frame()
    systemcounts = pd.DataFrame(columns=['System type','Counts'])
    for name, group in master_summary_table.groupby(by='System type'):
        group_df = pd.DataFrame(data=[[name, len(group)]],columns=['System type', 'Counts'])
        systemcounts = systemcounts.append(group_df)
    #systemcounts = systemcounts.reset_index(drop=False).rename(columns={"index":"System type"})
    print systemcounts
    type_dict ={'TypeI':0,'TypeII':0,'TypeIII':0,'TypeIV':0,'TypeV':0,'TypeV-U':0,'TypeVI':0}
    for index, row in systemcounts.iterrows():
        sys_types = row['System type']
        counts = row['Counts']
        if type(sys_types) is not int:
            typelist = sys_types.split('|')
            #print typelist
            for x in typelist:
                for key in type_dict.keys():
                    if x == key:
                        new_total= int(type_dict[key]) + int(counts)
                        type_dict[key] = new_total
    type_summary_frame = pd.DataFrame(columns=['Type','Count'])
    for key in type_dict.keys():
        key_row = pd.DataFrame(data=[[key, type_dict[key]]],columns=['Type','Count'])
        type_summary_frame = type_summary_frame.append(key_row)
    #type_summary_frame = type_summary_frame.reset_index(drop=True)
    type_summary_frame_sorted = type_summary_frame.sort_values(by='Type')
    type_summary_frame_sorted = type_summary_frame_sorted.reset_index(drop=True)
    #print type_summary_frame_sorted
    type_summary_frame_sorted.to_csv(os.path.join(final_outdir,'CRISPR-Cas_Type_summary.csv'))
    subsystemcounts = pd.DataFrame(columns=['System subtype','Counts'])
    for name, group in master_summary_table.groupby(by='system subtype'):
        group_df = pd.DataFrame(data=[[name, len(group)]],columns=['System subtype', 'Counts'])
        subsystemcounts = subsystemcounts.append(group_df)
    subtype_dict ={'TypeI-A':0,'TypeI-B':0,'TypeI-C':0,'TypeI-D':0,'TypeI-E':0,'TypeI-F':0,'TypeI-U':0,'TypeII-B':0,'TypeII-A':0,'TypeII-C':0,'TypeIII-A':0,'TypeIII-B/TypeIII-D':0,'TypeIII-C':0,'TypeIV':0, 'TypeV-A':0,'TypeV-B':0,'TypeV-C':0,'TypeV-D':0,'TypeV-E':0,'TypeVU-1':0,'TypeVU-2':0,'TypeVU-3':0,'TypeVU-4':0,'TypeVU-5':0,'TypeVI-A':0,'TypeVI-B':0,'TypeVI-C':0} 
    for index, row in subsystemcounts.iterrows():
        counts = row['Counts']
        sys_types = row['System subtype']
        if type(sys_types) is not int:
            typelist = sys_types.split('|')
            for x in typelist:
                for key in subtype_dict.keys():
                    if x == key:
                        new_total= int(subtype_dict[key]) + int(counts)
                        subtype_dict[key] = new_total
                        #print x, counts, subtype_dict[key]
    subtype_summary_frame = pd.DataFrame(columns=['Subtype','Count'])
    for key in subtype_dict.keys():
        key_row = pd.DataFrame(data=[[key, subtype_dict[key]]],columns=['Subtype','Count'])
        subtype_summary_frame = subtype_summary_frame.append(key_row)
    subtype_summary_frame = subtype_summary_frame.reset_index(drop=True)
    subtype_summary_frame_sorted = subtype_summary_frame.sort_values(by='Subtype')
    subtype_summary_frame_sorted = subtype_summary_frame_sorted.reset_index(drop=True)
    subtype_summary_frame_sorted.to_csv(os.path.join(final_outdir,'CRISPR-Cas_Subtype_summary.csv'))
    return master_summary_table

def addStrainInfo(master_summary_table, tax, taxinfofile, today, final_outdir=os.getcwd()):
    strain_info = pd.read_csv(taxinfofile, low_memory=False)
    if tax =='AgB':
        for index, row in master_summary_table.iterrows():
            orgname = row['organism'].split('_')[0]
            master_summary_table.loc[index, 'AIM Number'] = orgname
        subset_strain_info = strain_info[['AIM Number', 'Taxonomic ID Domain', 'Taxonomic ID Kingdom', 'Taxonomic ID Phylum', 'Taxonomic ID Class', 'Taxonomic ID Order', 'Taxonomic ID Family', 'Taxonomic ID Genus']]
        master_with_strain_info = pd.merge(master_summary_table, subset_strain_info,on='AIM Number', how = 'left')
    else:
        subset_strain_info = strain_info[['organism', 'Taxonomic ID Kingdom', 'Taxonomic ID Phylum', 'Taxonomic ID Class', 'Taxonomic ID Order', 'Taxonomic ID Family', 'Taxonomic ID Genus']]
        subset_strain_info = subset_strain_info.drop_duplicates()
        master_with_strain_info = pd.merge(master_summary_table, subset_strain_info,on='organism', how = 'left')
    master_with_strain_info.to_csv(os.path.join(final_outdir, 'Master_CRISPR_summary_table_with_strain_info_'+today+'.csv'))
    return master_with_strain_info

def masterTblWithStrain(taxinfofile,tax, today, finaloutputdir=os.getcwd(),workdir=os.getcwd()):
    master_summary_table = typeAnalysis(today, final_outdir=finaloutputdir,working_outdir=workdir)
    master_with_strain_info = addStrainInfo(master_summary_table,tax,taxinfofile, today, final_outdir=finaloutputdir)
    return master_with_strain_info
