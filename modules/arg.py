import argparse


class CmdArg:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='カクヨム記法で示されたルビをWordのルビにするツールです')
        self.parser.add_argument('inputfile', type=str, help='変換元docxファイル')
        self.parser.add_argument('-o', '--output',
                                 nargs='?', type=str,
                                 default='out.docx',
                                 help='出力ファイル名')
        self.parser.add_argument('-f', '--font',
                                 nargs='?', type=str,
                                 default='',
                                 help='出力ファイル名')
        self.args = self.parser.parse_args()
