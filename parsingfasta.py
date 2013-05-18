from Bio import SeqIO
import hashlib, os

def insert(entry):
    return ["INSERT INTO Sequences(seqID, path) VALUES (\"%(seqID)s\", \"%(path)s\");" % entry]

def hasher(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

class parser:
    import re
    def regexer(self,regex):
        pattern = self.re.compile(regex)
        return lambda string: pattern.findall(string)

    def __init__(self,pattern=[]):
        self.match, self.fetch = {},{}
        for key,self.match[key],self.fetch[key] in pattern:
            self.match[key] = self.regexer(self.match[key])

    def parse(self,string, entry={}):
        for label in self.match.keys():
            match = self.match[label](string)
            if match:
                entry.update(self.fetch[label](match))
        return entry


def file2entries(file):
    if fileType(file) == 'fasta':
        return parseFasta(file)


def parseFasta(filepath):
    from settings import patterns
    fileparser = parser(patterns)
    entries = []
    for record in SeqIO.parse(filepath,extension(filepath)):
        entries.append(
            fileparser.parse(record.description,
                             {'seqID': record.id,
                              'description': record.description,
                              'seqHash': hasher(str(record.seq)),
                              'path': filepath,
                              'format':extension(filepath)}))
    return entries
        
def entries2records(entries):
    records = []
    files = set([(entry['path'],entry['format']) for entry in entries])
    find = set(entry['seqID'] for entry in entries)
    for file,format in files:
        for record in SeqIO.parse(file,format):
            if record.id in find:
                find.remove(record.id)
                records.append(record)
    return records

def records2file(records, path):
    SeqIO.write(records, path, fileType(path))

def entries2file(entries,file):
    records2file(entries2records(entries),file)

def extension(filename):
    path, ext = os.path.splitext(filename)
    return ext[1:]

from settings import extensions
def fileType(filename):
    ext = extension(filename)
    for key in extensions.keys():
        if ext in extensions[key]:
            return key
    return

            
