import os
import zipfile
import shutil
from . import txt2docx as t2d


class FileProc:

    def __init__(self, template: str,
                 input: str, output: str, extract_dir: str = './'):
        self._template = template
        self._input = input
        self._output = output
        self._extract_dir = extract_dir
        self._files = list()
        self._dirs = set()
        self._document = 'word/document.xml'

    def _extract(self, input: str,
                 extract_dir: str) -> tuple[list[str], set[str]]:
        with zipfile.ZipFile(input) as zf:
            files = zf.namelist()
            dirs = set()
            # print(self.__files)
            for f in files:
                d = os.path.dirname(f)
                dirs.add(d)
            dirs.discard('')
            # print(self.__dirs)
            zf.extractall(extract_dir)
        return (files, dirs)

    def _from_read_to_write(self,
                            extract_dir: str,
                            document: str):
        with open(extract_dir+document,
                  mode='r', encoding='utf-8') as f:
            s = f.read()

        new_code = t2d.make_new_xml(s)

        with open(extract_dir+document,
                  mode='w', encoding='utf-8') as f:
            f.write(new_code)

    def _make_docx(self, output, extract_dir, file_list):
        with zipfile.ZipFile(output, 'w',
                             compression=zipfile.ZIP_STORED,
                             compresslevel=0) as zf:
            for f in file_list:
                # print(f)
                zf.write(extract_dir+f)
                os.remove(extract_dir+f)

    def _delete_tempdir(self, extract_dir, dirs):
        for dd in dirs:
            if os.path.exists(dd):
                shutil.rmtree(extract_dir + dd)

    def process(self, output_place='.'):
        self._files, self._dirs = self._extract(self._input, self._extract_dir)
        self._from_read_to_write(self._extract_dir, self._document)
        self._make_docx(self._output, self._extract_dir, self._files)
        self._delete_tempdir(self._extract_dir, self._dirs)
        new_file = os.path.join(os.getcwd(), self._output)
        shutil.move(new_file, output_place)
