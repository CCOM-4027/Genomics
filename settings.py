default = {
    'database':'genomedb',
    'username':'laadguest',
    'password':'password'
    }
databases = {
    'genomedb' : {
        'Sequences' : [
            ['seqID','TEXT'],
            ['seqHash', 'TEXT'],
            ['seq','LONGTEXT'],
            ['file','TEXT'],
            ['format','TEXT'],
            ['sampleID', 'TEXT']],
        'Reeds':[
            ('seqHash', 'TEXT')],
        'Aligned':
            [('aligner', 'TEXT'),
             ('seqID','TEXT'),
             ('seqHash', 'TEXT'),
             ('aligned_to', 'TEXT'),
             ('score','DOUBLE(15,15)'),
             ('start','INT'),
             ('end','INT')]},
    'ximena' : {
        'Sequences' : [
            ['seq','LONGTEXT'],
            ['seqID', 'TEXT']],
        'Alignments' : [
            ['seqID', 'TEXT'],
            ['score', 'DOUBLE(10,10)'],
            ['pop1','TEXT'],
            ['pop2','TEXT']]
        }
    }
tables = {
    'Sequences':
        [['seqID','TEXT'],
         ['seqHash', 'TEXT'],
         ['seq','LONGTEXT'],
         ['file','TEXT'],
         ['format','TEXT'],
         ['sampleID', 'TEXT']],
    'Reeds':
        [('seqHash', 'TEXT')],
    'Aligned':
        [('aligner', 'TEXT'),
         ('seqID','TEXT'),
         ('seqHash', 'TEXT'),
         ('aligned_to', 'TEXT'),
         ('score','DOUBLE(15,15)'),
         ('start','INT'),
         ('end','INT')]
    }
#users
#This section defines users that are to be created automatically when the
#database is initialized
#This defines the default username and password for the database, used when the
#database is created and when any action is attempted without providing a username
guest = {'username': 'laadguest',
        'password': 'password'}
    
#Extensions
#this is a mapping of a file format to it's possible extensions
extensions = {
    'fasta': ['fasta','fa','fas','fast','fna'],
    #'sam': ['sam'],
    'csv': ['csv'],
    'tsv': ['tsv'],
    'json': ['json']
    }

#Patterns  
#This section deals with patterns for extracting information from description strings

#This first part defines functions that take a list of tuples
#these are generated when a regular expression is matched
#any non-specified part of a regular expression is captured if there is a match
#these definitions specify under what key these matches will be stored
#in a dictionary
def equals(matches):
    return {key:value for key,value in matches}

def aligned(matches):
    target,start,finish = matches[0]
    return {'aligned_to': target,
            'start':int(start),
            'end':int(finish)}
def species(matches):
    number = matches[0]
    return {'species':number}
#'patterns' list which will be called when a parser is needed
#it consists of a label, a regular expression and the name of
#one of the functions defined above
patterns = [['equals', '(\w+)=(\w+)', equals], 
            ['aligned', '(\w+-\w+), (\d+)\.\.(\d+)', aligned],
            ['species', 'MID(\d+)contig', species]]

#string = "MID7contig04845 HMEL015723-RA, 7..303  length=351   numreads=7"
#print foo.make(string)
aliases = {
    'ximena':
        {'Fst':'score',
         'Locus ID':'seqID',
         '2':'seqID',
         '9':'seq',
         'Pop 1 ID':'pop1',
         'Pop 2 ID':'pop2'}
    }
queries = {
    'allseqs' :
        "select * from Sequences",
    'ximena' :
        "select seqID,seq from (select seq, seqID from Sequences where file = \"batch_1.catalog.tags.tsv\") as seqs where seqs.seqID in (select seqID from Aligned where score >= .5);",
    'ximena2' :
        "select seqID from (select seqID from Aligned where score >=.5) as seqs where seqs.seqID in (select seqID from Sequences);"
    }
headers = {
    'catalog':
        "0,1,2,3,4,5,6,7,8,9,10,11,12"
    }
              
