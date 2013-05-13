from Bio import SeqIO
import hashlib, os

class SeqEntry:
    def __init__(self, seq_id, seq_hash, seq_location):
        self.id = seq_id
        self.hash = seq_hash
        self.location = seq_location

def hasher(string):
    m = hashlib.md5()
    m.update(string)
    return m.digest()
    
def file_type(filename):
    return "fasta"

def file_to_entries(filename):
    seq_entries = []
    for seq_record in SeqIO.parse(filename, file_type(filename)):
        seq_entries.append(SeqEntry(seq_record.id,
                                    hasher(str(seq_record.seq)),
                                    filename))
    return seq_entries

def entries_to_file(entries):
    SeqIO.write(seq_entries, "my_fasta.faa", "fasta")

def extension(input):
    path, ext = os.path.splitext(input)
    return ext
