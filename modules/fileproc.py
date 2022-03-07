import os
import glob
import zipfile
import shutil
from pathlib import Path
from dataclasses import dataclass
from . import txt2docx as t2d


@dataclass
class FileProc:

    template: Path
    inputfile: Path
    output: Path
    ruby_font: str

    def __post_init__(self):
        self.template = self.template.resolve()
        self.inputfile = self.inputfile.resolve()
        self.output = self.output.resolve()

        self.extract_dir = self.output.parent

    def _extract(self, inputfile: str,
                 extract_dir: str) -> tuple[list[str], set[str], Path]:
        with zipfile.ZipFile(inputfile) as zf:
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
            docxml = tuple(Path(extract_dir).glob('word/document*.xml'))[0]
        return (files, dirs, docxml)

    def _from_read_to_write(self, document: str):
        with open(document, mode='r', encoding='utf-8') as f:
            s = f.read()

        new_code = t2d.make_new_xml(self.ruby_font, s)

        with open(document, mode='w', encoding='utf-8') as f:
            f.write(new_code)

    def _make_docx(self, output: str, file_list: list[str]):
        with zipfile.ZipFile(output, 'w',
                             compression=zipfile.ZIP_STORED,
                             compresslevel=0) as zf:
            for f in file_list:
                filepath = os.path.join('.', f)
                zf.write(filepath)
                os.remove(filepath)

    def _delete_tempdir(self, extract_dir: str, dirs: set[str]):
        for dd in dirs:
            if os.path.exists(dd):
                shutil.rmtree(os.path.join(extract_dir, dd))

    def process(self):
        self.files, self.dirs, self.docxml = self._extract(
                self.inputfile.as_posix(),
                self.extract_dir.as_posix())
        self._from_read_to_write(self.docxml.as_posix())
        self._make_docx(self.output.as_posix(), self.files)
        self._delete_tempdir(self.extract_dir.as_posix(), self.dirs)
