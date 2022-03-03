import os
import glob
import zipfile
import shutil
from dataclasses import dataclass
from . import txt2docx as t2d

@dataclass
class FileProc:

    template: str
    input: str
    output: str
    ruby_font: str

    def __post_init__(self):
        self.extract_dir = os.path.dirname(self.output)
        if self.extract_dir == '':
            self.extract_dir = '.'

    def _extract(self, input: str,
                 extract_dir: str) -> tuple[list[str], set[str], str]:
        with zipfile.ZipFile(input) as zf:
            files = zf.namelist()
            dirs = set()
            docxml: str
            # print(self.__files)
            for f in files:
                d = os.path.dirname(f)
                dirs.add(d)
            dirs.discard('')
            # print(self.__dirs)
            os.chdir(extract_dir)
            zf.extractall(extract_dir)
            docxml = os.path.join(extract_dir, glob.glob('word/document*.xml')[0])
        return (files, dirs, docxml)

    def _from_read_to_write(self, document: str):
        with open(document, mode='r', encoding='utf-8') as f:
            s = f.read()

        new_code = t2d.make_new_xml(self.ruby_font, s)

        with open(document, mode='w', encoding='utf-8') as f:
            f.write(new_code)

    def _make_docx(self, output, file_list):
        with zipfile.ZipFile(output, 'w',
                             compression=zipfile.ZIP_STORED,
                             compresslevel=0) as zf:
            for f in file_list:
                filepath = os.path.join('.', f)
                zf.write(filepath)
                os.remove(filepath)

    def _delete_tempdir(self, extract_dir, dirs):
        for dd in dirs:
            if os.path.exists(dd):
                shutil.rmtree(os.path.join(extract_dir,dd))

    def process(self):
        self.files, self.dirs, self.docxml = self._extract(self.input, self.extract_dir)
        self._from_read_to_write(self.docxml)
        self._make_docx(self.output, self.files)
        self._delete_tempdir(self.extract_dir, self.dirs)
