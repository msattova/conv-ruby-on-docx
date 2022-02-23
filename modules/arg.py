import argparse

class CmdArg:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
                    description='HTMLファイル形式のTRPGログをmarkdownにするツールです。')
        self.parser.add_argument('filename', type=str, help='変換したいログのファイル名')
        self.parser.add_argument('-l', '--leave',
                    default=False, action='store_true',
                    help='''出力ファイル名を入力ファイル名と同じにする
                    （-oオプションは無視されます）''')
        self.parser.add_argument('-o', '--output',
                    nargs='?', type=str,
                    default='out.md',
                    help='出力ファイル名')
        self.parser.add_argument('--only', type=str,
                    default=None,
                    help='指定したタブのみ変換')
        self.parser.add_argument('--exclude', action='extend', type=str,
                    default=None, nargs='*',
                    help='指定したタブを除外して変換')
        self.parser.add_argument('--notab',
                    default=False, action='store_true',
                    help='タブ名を表示しない')
        self.args = self.parser.parse_args()


