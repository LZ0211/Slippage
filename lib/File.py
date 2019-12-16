#!/usr/bin/env python
# coding=utf-8
import os,re,xlrd,xlwt,codecs,chardet

class File:
    def __init__(self,filename=None):
        if not filename == None:
            found = re.match(r'^"(.*)"$',filename)
            if found:
                filename = found[1]
            (filepath, tempfilename) = os.path.split(filename)
            (filename, filetype) = os.path.splitext(tempfilename)
            self.filepath = filepath
            self.filename = filename
            self.filetype = filetype.lower()
            self.file = os.path.join(self.filepath,self.filename+self.filetype)
            self.data = []

    def detectCode(self,path):
	    with open(path, 'rb') as file:
		    data = file.read(200000)
		    dicts = chardet.detect(data)
	    return dicts["encoding"]

    def read_data(self):
        if self.filetype == '.txt':
            self.data = self.read_txt_file(self.file)
        elif self.filetype == '.csv':
            self.data = self.read_txt_file(self.file)
        elif self.filetype == '.xls':
            self.data = self.read_xls_file(self.file)
        elif self.filetype == '.xlsx':
            self.data = self.read_xls_file(self.file)
        else:
            raise Exception(self.file + ' is invalid data file!')
        return self.data

    def write_data(self,data):
        if self.filetype == '.txt':
            self.write_txt_file(self.file,data)
        elif self.filetype == '.csv':
            self.write_csv_file(self.file,data)
        elif self.filetype == '.xls':
            self.write_xls_file(self.file,data)
        elif self.filetype == '.xlsx':
            self.write_xls_file(self.file,data)

    def save_as(self,file):
        (filepath, tempfilename) = os.path.split(file)
        (filename, filetype) = os.path.splitext(tempfilename)
        filetype = filetype.lower()
        if filetype == '.txt':
            self.write_txt_file(file,self.data)
        elif filetype == '.csv':
            self.write_csv_file(file,self.data)
        elif filetype == '.xls':
            self.write_xls_file(file,self.data)
        elif filetype == '.xlsx':
            self.write_xls_file(file,self.data)

    def read_txt_file(self,filename):
        encoding = self.detectCode(filename)
        lines = open(filename,encoding=encoding).read().strip().splitlines()
        lines = filter(lambda line: not re.match(r'[^\s\d\.\+\-]',line),lines)
        points = filter(lambda x:len(x)==2,map(lambda line:list(map(lambda x:float(x),filter(lambda x: not x == '',re.split(r'[,\s]+',line.strip())))),lines))
        return list(points)

    def read_xls_file(self,filename):
        wb = xlrd.open_workbook(filename)
        ws = wb.sheet_by_index(0)
        points = []
        for i in range(1,ws.nrows):
            line = []
            for j in range(ws.ncols):
                val = ws.cell_value(i, j)
                line.append(val)
            points.append(line)
        return points

    def write_txt_file(self,filename,data):
        open(filename,'w+').write('\n'.join(map(lambda x:'\t'.join(map(str,x)),data)))

    def write_csv_file(self,filename,data):
        open(filename,'w+').write('\n'.join(map(lambda x:','.join(map(str,x)),data)))

    def write_xls_file(self,filename,data):
        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet('Sheet1', cell_overwrite_ok=True)
        for i in range(len(data)):
            line = data[i]
            for j in range(len(line)):
                ws.write(i,j,line[j])
        wb.save(filename)
