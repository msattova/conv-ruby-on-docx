import os
import platform
import subprocess
from zipfile import ZipFile, ZIP_STORED
import shutil
from pathlib import Path
from dataclasses import dataclass
from modules.txt2docx import make_new_xml


@dataclass
class FileProc:

    template: Path
    inputfile: Path
    output: Path
    ruby_font: str
    em_style: str

    def __post_init__(self):
        self.template = self.template.resolve()
        self.inputfile = self.inputfile.resolve()
        self.output = self.output.resolve()

        self.extract_dir: Path = self.output.parent

    def _extract(self, inputfile: Path,
                 extract_dir: Path) -> tuple[list[str], set[str], Path]:
        with ZipFile(inputfile) as zf:
            files = zf.namelist()
            dirs: set[str] = set()
            for f in files:
                d = os.path.dirname(f)
                dirs.add(d)
            dirs.discard('')
            # print(self.__dirs)
            os.chdir(extract_dir)
            zf.extractall(extract_dir)
            docxml = tuple(extract_dir.glob('word/document*.xml'))[0]
        return (files, dirs, docxml)

    def _from_read_to_write(self, document: Path):
        with document.open(mode='r', encoding='utf-8') as f:
            s = f.read()

        new_code = make_new_xml(self.ruby_font, self.em_style, s)

        with document.open(mode='w', encoding='utf-8') as f:
            f.write(new_code)

    def _make_docx(self, file_list: list[str]):
        with ZipFile(self.output.name, 'w',
                     compression=ZIP_STORED,
                     compresslevel=0) as zf:
            for f in file_list:
                filepath = os.path.join('.', f)
                zf.write(filepath)
                os.remove(filepath)
        if platform.system() == 'Darwin':
            subprocess.run(
                f'zip --delete {self.output.name} "*__MACOSX*" "*.DS_Store"')

    def _delete_tempdir(self, extract_dir: str, dirs: set[str]):
        for dd in dirs:
            if os.path.exists(dd):
                shutil.rmtree(os.path.join(extract_dir, dd))

    def process(self):
        files, dirs, docxml = self._extract(self.inputfile, self.extract_dir)
        self._from_read_to_write(docxml)
        self._make_docx(files)
        self._delete_tempdir(self.extract_dir.as_posix(), dirs)
