
from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple
import platform
import regex


class EmType(Enum):
    DOT = 'dot'
    COMMA = 'comma'


class TemplateType(NamedTuple):
    ruby_open:    str
    ruby_end:     str
    oyamoji_open: str
    oyamoji_end:  str
    general_open: str
    general_end:  str
    bouten_open:  str


@dataclass
class Template:
    font:   str
    emtype: str

    def __post_init__(self):
        if not self.font:
            self.font = self.division_font()
        if self.emtype not in set(i.value for i in EmType):
            self.emtype = EmType.DOT.value
        self.template = self.make_template()

    @staticmethod
    def division_font() -> str:
        pf = platform.system()
        match pf:
            case 'Windows':
                return 'ＭＳ 明朝'
            case 'Darwin':
                return 'ヒラギノ明朝 ProN '
            case 'Linux':
                # Linux環境の場合はOSごとに標準でインストールされてるフォントが違うので要改善
                return 'Noto Serif CJK JP'
            case _:
                return 'Noto Serif CJK JP'

    def make_template(self) -> TemplateType:
        tmp = tuple(''.join(s) for s in (
            (r'<w:r>', r'<w:ruby>', r'<w:rubyPr>',
             r'<w:rubyAlign w:val="distributeSpace"/>',
             r'<w:hps w:val="10"/>',
             r'<w:hpsRaise w:val="18"/>',
             r'<w:hpsBaseText w:val="21"/>',
             r'<w:lid w:val="ja-JP"/>',
             r'</w:rubyPr>',
             r'<w:rt>',
             r'<w:r w:rsidR="00E95970" w:rsidRPr="00E95970">',
             r'<w:rPr>',
             rf'<w:rFonts w:ascii="{self.font}" w:eastAsia="{self.font}" w:hAnsi="{self.font}" w:hint="eastAsia"/>',
             r'<w:sz w:val="10"/>',
             r'</w:rPr>',
             r'<w:t>'),  # 0 close
            # ここにルビ文字列（例：ふりがな）
            (r'</w:t>',
             r'</w:r>',
             r'</w:rt>'),  # 1 close
            (r'<w:rubyBase>',
             r'<w:r w:rsidR="00E95970">',
             r'<w:rPr>',
             r'<w:rFonts w:hint="eastAsia"/>',
             r'</w:rPr>',
             r'<w:t>'),  # 2 close
            # ここにルビを振る文字列（例：振仮名）
            (r'</w:t>', r'</w:r>', r'</w:rubyBase>',
             r'</w:ruby>', r'</w:r>'),  # ルビ関連のタグここまで # 3 close
            (r'<w:r><w:rPr>',
             r'<w:rFonts w:hint="eastAsia"/>',
             r'</w:rPr><w:t>'),  # 4 close
            # ルビ振り処理対象外の余った文字列をここに
            (r'</w:t>', r'</w:r>'),  # 5 close
            # 傍点表示用
            (r'<w:r><w:rPr>',
             r'<w:rFonts w:hint="eastAsia"/>',
             rf'<w:em w:val="{self.emtype}"/>',
             r'</w:rPr><w:t>')))  # 6 close
        return TemplateType(
            ruby_open=tmp[0],
            ruby_end=tmp[1],
            oyamoji_open=tmp[2],
            oyamoji_end=tmp[3],
            general_open=tmp[4],
            general_end=tmp[5],
            bouten_open=tmp[6])


# タグ単体（開始or終了）にマッチするパターン
REG_TAG = regex.compile(r'<[^<>]*>')
REG_TAG_GET = regex.compile(r'(<[^<>]+>)')
# 漢字《かんじ》にマッチするパターン
REG_KANJI_AND_RUBY = regex.compile(r'([\p{Script=Han}\u30F5]+)《([^《》]+)》')
REG_KANJI_AND_RUBY_AROUND = regex.compile(
    r'([\p{Script=Han}\u30F5]+《[^《》]*?》)')
# パイプ（|）つき親文字にマッチするパターン（例：|親文字《ルビ》）
REG_PIPE_OYAMOJI_RUBY = regex.compile(r'\|([^|]+)《([^《》]+)》')
REG_PIPE_OYAMOJI_GET_AROUND = regex.compile(r'(\|[^|《》]+《[^《》]+》)')
# パイプ（|）にマッチするパターン
REG_PIPE = regex.compile(r'\|')
# OP：'文字列《'にマッチ。  /  CL：'》文字列'にマッチ
REG_OP_SENTENCE = regex.compile(r'[^《》]*《')
REG_CL_SENTENCE = regex.compile(r'》[^《》]*')
REG_OPCL_SENTENCE = regex.compile(r'[^《》]*《[^《》]*》[^《》]*')
# 傍点の記法《《》》
REG_BOUTEN_OPCL = regex.compile(r'.*《《(?:(?!《《|》》).)+》》.*')
REG_BOUTEN_OP = regex.compile(r'.*《《.*')
REG_BOUTEN_CL = regex.compile(r'.*》》.*')
REG_BOUTEN_GET = regex.compile(r'(《《(?:(?!《《|》》).)+》》)')
REG_BOUTEN_GET_INSIDE = regex.compile(r'《《((?:(?!《《|》》).)+)》》')
