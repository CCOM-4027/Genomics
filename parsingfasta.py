from Bio import SeqIO

import os
def extension(filename):
    path, ext = os.path.splitext(filename)
    return ext[1:]

from settings import extensions
def fileType(filename):
    ext = extension(filename)
    for key in extensions:
        if ext in extensions[key]:
            return key
    return

from hashlib import md5             
def hasher(string):
    m = md5()
    m.update(string)
    return m.hexdigest()

class parser:
    import re
    def regexer(self,regex):
        """
        regexer:regex->lamda:string->matches
        takes a regular expression and outputs a function that
        takes a string and produces a list of tuples of captured values
        """
        pattern = self.re.compile(regex)
        return lambda string: pattern.findall(string)

    def __init__(self,pattern=[]):
        self.match, self.fetch = {},{}
        for key,self.match[key],self.fetch[key] in pattern:
            self.match[key] = self.regexer(self.match[key])

    def parse(self,string, entry={}):
        """
        tries to match all regexes against the string
        if successful runs the associated handler
        """
        for label in self.match.keys():
            match = self.match[label](string)
            if match:
                entry.update(self.fetch[label](match))
        return entry

def file2entries(file,options):
    return eval('%s2entries'%fileType(file))(file,options)
def sam2entries(file,options):
    print 'sam'
def fasta2entries(filepath, options):
    description=options['description']
    from settings import patterns
    fileparser = parser(patterns)
    entries = []
    for record in SeqIO.parse(filepath,fileType(filepath)):
        entries.append(
            fileparser.parse(record.description+" "+description,
                             {'seqID': record.id,
                              'description': record.description,
                              'seqHash': hasher(str(record.seq)),
                              'path': filepath,
                              'format':extension(filepath)}))
    return entries

def json2entries(file, options):
    import ast
    with open(file,'r') as file:
        return ast.literal_eval(file.read())
def csv2entries(file, options):
    return csvInput(file,options)
def tsv2entries(file, options):
    return csvInput(file,options,'excel-tab')

def csvInput(file,options,dialect='excel'):
    header=options['header']
    from csv import DictReader
    with open(file,'r') as f:
        if not header:
            reader = DictReader(f,dialect=dialect)
        else:
            reader = DictReader(f,dialect=dialect,fieldnames=header.split(','))
        reader.fieldnames = map(options['alias'],reader.fieldnames)
        entries =[line for line in reader]
        map(lambda(dict):
                dict.update({"file":file,
                             "format":fileType(file)}),
            entries)
        return entries
        


############
###OUTPUT###
############
def entries2file(entries,file,verbose = False):
    eval('entries2%s'%fileType(file))(entries,file,verbose)

def entries2fasta(entries,file,verbose=False):
    if verbose:
        entryno,files = len(entries),len(set([entry['path'] for entry in entries]))
        print "Fetching %s sequences from % source file(s)" % (entryno,files)
    records = entries2records(entries)
    if verbose:
        print "Writing %s entries to %s" % (entryno,file)
    SeqIO.write(records,file,fileType(file))

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

def entries2json(entries,file,verbose=False):
    import json
    with open(file,'w') as file:
        jsonfile.write(json.dumps(entries))

def entries2csv(entries,file,verbose=False):
    csvOutput(entries,file)

def entries2tsv(entries,file,verbose=False):
    csvOutput(entries,file,'excel-tab')

def csvOutput(entries,file, dialect='excel'):
    from csv import DictWriter
    with open(file,'w') as file:
        keys = []
        for entry in entries:
            keys.extend(key for key in entry)
        keys = list(set(keys))
        w=DictWriter(file,keys,dialect=dialect)
        w.writeheader()
        #({key:key for key in keys})
        for entry in entries:
            w.writerow(entry)





            
