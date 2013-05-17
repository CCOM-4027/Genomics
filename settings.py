

tables = [
    "CREATE TABLE Sequences(seqID TEXT, seqHash TEXT, path TEXT)", 
    "CREATE TABLE Reeds(sampleID INT, seqHash TEXT)", 
    "CREATE TABLE Assembled(Assembler TEXT, sampleID TEXT, seqID TEXT, seqHash TEXT)", 
    "CREATE TABLE Align(aligner TEXT, sourceID TEXT, targetID TEXT, targetHash TEXT)" 
    ]

tables2 = {'Sequences':[('seqID','TEXT'),
                        ('seqHash', 'TEXT'),
                        ('path','TEXT')]}
#These are the extensions for file formats that have been programmed in
extensions = {'fasta': ['fasta','fa','fas','fast','fna'],
              'sam': ['sam']}

#This defines the default username and password for the database, used when the
#database is created and when any action is attempted without providing a username
guest = {'username': 'laadguest',
         'password': 'password'}

import re
def regexer(regex):
    pattern = re.compile(regex)
    return lambda string: pattern.findall(string)

headers = {'equals': regexer('(\w+)=(\d+)'),
           'aligned': regexer('(\w+-\w+), (\d+)\.\.(\d+)')}
        
def equals(matches):
    return {key:value for key,value in matches}

def aligned(matches):
    target,start,finish = matches[0]
    return {'aligned_to': target,
            'start':start,
            'finish':finish}

patterns = [['equals', '(\w+)=(\d+)', equals], 
            ['aligned', '(\w+-\w+), (\d+)\.\.(\d+)', aligned]]

#string = "MID7contig04845 HMEL015723-RA, 7..303  length=351   numreads=7"
#print foo.make(string)

