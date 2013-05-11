from Bio import SeqIO
import hashlib

class SeqEntry:
    def __init__(self, seq_id, seq_hash, seq_location):
        self.id = seq_id
        self.hash = seq_hash
        self.location = seq_location

def hasher(string):
    m = hashlib.md5()
    m.update(string)
    return m.digest()
    
def file_type(file):
    return "fasta"

def file_to_entry(filename):
    seq_entries = []
    for seq_record in SeqIO.parse(filename, file_type()):
        seq_entries.append(SeqEntry(seq_record.id,
                                    hasher(str(seq_record.seq)),
                                    filename))

    SeqIO.write(seq_entries, "my_fasta.faa", "fasta")
