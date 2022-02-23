import os
import zipfile
import shutil
from . import txt2docx as t2d


class FileProc:

    def __init__(self, template: str,
                 input: str, output: str, tmp_dir: str = './'):
        self.__template = template
        self.__input = input
        self.__output = output
        self.__tmp_dir = tmp_dir
        self.__files = list()
        self.__dirs = set()
        self.__document = 'word/document.xml'

    def __extract(self):
        with zipfile.ZipFile(self.__template) as zf:
            self.__files = zf.namelist()
            #print(self.__files)
            for f in self.__files:
                d = os.path.dirname(f)
                self.__dirs.add(d)
            self.__dirs.discard('')
            #print(self.__dirs)
            zf.extractall(self.__tmp_dir)

    def __from_read_to_write(self):
        with open(self.__tmp_dir+self.__document,
                  mode='r', encoding='utf-8') as f:
            s = f.read()

        r = t2d.make_new_xml(s)

        with open(self.__tmp_dir+self.__document,
                  mode='w', encoding='utf-8') as f:
            f.write(r)

    def __make_docx(self):
        with zipfile.ZipFile(self.__output, 'w',
                             compression=zipfile.ZIP_STORED,
                             compresslevel=0) as zf:
            for f in self.__files:
                #print(f)
                zf.write(self.__tmp_dir+f)
                #os.remove(self.__tmp_dir+f)

    def __delete_tempdir(self):
        for dd in self.__dirs:
            if os.path.exists(dd):
                shutil.rmtree(self.__tmp_dir + dd)

    def process(self):
        self.__extract()
        self.__from_read_to_write()
        self.__make_docx()
        self.__delete_tempdir()
