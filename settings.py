tables = [
    "CREATE TABLE Sequences(seqID TEXT, seqHash TEXT, path TEXT)", 
    "CREATE TABLE Reeds(sampleID INT, seqHash TEXT)", 
    "CREATE TABLE Assembled(Assembler TEXT, sampleID TEXT, seqID TEXT, seqHash TEXT)", 
    "CREATE TABLE Align(aligner TEXT, sourceID TEXT, targetID TEXT, targetHash TEXT)" 
    ]
#These are the extensions for file formats that have been programmed in
extensions = ['fasta','sam']

guest = {'username': 'laadguest',
         'password': 'password'}
