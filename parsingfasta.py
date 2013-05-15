from Bio import SeqIO
import hashlib, os

class seqEntry:
    data = {}
    def __init__(self, seq_id, seq_hash, path="null"):
        self.data["seqID"] = seq_id
        self.data["seqHash"] = seq_hash
        self.data["path"] = path

    def commands(self):
        """generate list of insert statements based on which
        fields the sequence has defined"""
       # ret = "INSERT INTO Sequences(seqID, seqHash) VALUES (%('seqID')s, %('seqHash')s", (self.data["seqID"], self.data["seqHash"])
        ret = "INSERT INTO Sequences(seqID, path) VALUES (%(seqID)s, %(path)s)" % self.data
        return [ret]

def hasher(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()
    
def file_type(filename):
    return "fasta"

def file_to_entries(filename):
    seq_entries = []
    for seq_record in SeqIO.parse(filename, file_type(filename)):
        seq_entries.append(seqEntry(seq_record.id,
                                    hasher(str(seq_record.seq)),
                                    filename))
    return seq_entries

def entries_to_file(entries):
    SeqIO.write(seq_entries, "my_fasta.faa", "fasta")

def extension(input):
    path, ext = os.path.splitext(input)
    return ext[1:]
