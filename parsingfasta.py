from Bio import SeqIO
import hashlib, os

def insert(sequence):
    return ["INSERT INTO Sequences(seqID, path) VALUES (\"%(seqID)s\", \"%(path)s\");" % sequence]

def hasher(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

from settings import headers
def file_to_entries(filename):
    entries = []
    for record in SeqIO.parse(filename, extension(filename)):
        entry = {'seqID': record.id,
                 'description': record.description,
                 'seqHash': hasher(str(record.seq)),
                 'path': filename}
        match = headers['equals'](record.description)
        if match:
            for label, value in match:
                entry[label] = value
        match = headers
        entries.append(entry)
    return entries

def entries_to_file(entries):
    SeqIO.write(seq_entries, "my_fasta.faa", "fasta")

def extension(input):
    path, ext = os.path.splitext(input)
    return ext[1:]

from settings import extensions
def file_type(filename):
    ext = extension(filename)
    for extension in extensions.keys():
        if ext in extensions[key]:
            return key
        
class parser:
    import re
    def regexer(self,regex):
        pattern = re.compile(regex)
        return lambda string: pattern.findall(string)

    def __init__(self,pattern=[]):
        self.match, self.parse = {},{}
        for key,self.match[key],self.parse[key] in pattern:
            self.match[key] = regexer(self.match[key])

    def make(self,string, entry={}):
        for label in self.match.keys():
            match = self.match[label](string)
            if match:
                entry.update(self.parse[label](match))
        return entry
