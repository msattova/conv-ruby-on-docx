
import platform
import regex
from typing import Final


def make_template(font="", emtype="dot") -> tuple:
    if font == '':
        pf = platform.system()
        match pf:
            case 'Windows':
                font = 'ＭＳ 明朝'
            case 'Darwin':
                font = 'ヒラギノ明朝 ProN '
            case 'Linux':  # Linux環境の場合はOSごとに標準でインストールされてるフォントが違うので要改善
                font = 'Noto Serif CJK JP'
            case _ :
                font = 'Noto Serif CJK JP'
    return tuple(''.join(s) for s in (
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
         rf'<w:rFonts w:ascii="{font}" w:eastAsia="{font}" w:hAnsi="{font}" w:hint="eastAsia"/>',
         r'<w:sz w:val="10"/>',
         r'</w:rPr>',
         r'<w:t>'), # 0 close
        # ここにルビ文字列（例：ふりがな）
        (r'</w:t>',
         r'</w:r>',
         r'</w:rt>',
         r'<w:rubyBase>',
         r'<w:r w:rsidR="00E95970">',
         r'<w:rPr>',
         r'<w:rFonts w:hint="eastAsia"/>',
         r'</w:rPr>',
         r'<w:t>'), # 1 close
        # ここにルビを振る文字列（例：振仮名）
        (r'</w:t>', r'</w:r>', r'</w:rubyBase>',
         r'</w:ruby>', r'</w:r>'),  # ルビ関連のタグここまで # 2 close
        (r'<w:r><w:rPr>',
         r'<w:rFonts w:hint="eastAsia"/>',
         r'</w:rPr><w:t>'), # 3 close
        # ルビ振り処理対象外の余った文字列をここに
        (r'</w:t>', r'</w:r>'), # 4 close
        # 傍点表示用
        (r'<w:r><w:rPr>',
         r'<w:rFonts w:hint="eastAsia"/>',
         rf'<w:em w:val="{emtype}"/>',
         r'</w:rPr><w:t>') ))  # 5 close

# <w:r>タグで囲まれた文字列（<w:r>を含む）を取得するパターン
# make_new_xml内で1回しか利用されないのでコンパイルしない
REG_SURROUND_WR: Final[str] = r'<w:r(?:\s[^<>]+)?>(?:(?!<w:r>|</w:r>).)*</w:r>'
REG_SURROUND_WR_WITH_ATTR: Final[str] = r'<w:r\s[^<>]+>(?:(?!<w:r>|</w:r>).)*</w:r>'
# 《》内の文字列取得用パターン
REG_RUBY = regex.compile(r'(?<=《).*?(?=》)')
# マッチさせたいタグ名を格納するタプル
TAGS: Final[tuple] = ('w:r', 'w:t', '.+')
# タグで囲まれた文字列にマッチするパターン
REG_TAG_OPCL = { tag: regex.compile(r'<{tag}>(?:(?!<{tag}>|</{tag}>).)*</{tag}>') for tag in TAGS}
# タグ単体（開始or終了）にマッチするパターン
REG_TAG = regex.compile(r'<[^<>]*>')
# w:rタグの開始or終了にマッチ
REG_WR = regex.compile(r'</?w:r(\s[^<>]+)?>')
# 漢字《かんじ》にマッチするパターン
REG_KANJI_AND_RUBY = regex.compile(r'([\p{Script=Han}\u30F5]+)《([^《》]+)》')
REG_KANJI_AND_RUBY_AROUND = regex.compile(
    r'([\p{Script=Han}\u30F5]+《[^《》]*?》)')
# 漢字にだけマッチするパターン
REG_KANJI = regex.compile(r'[\p{Script=Han}\u30F5]+')
# パイプ（|）つき親文字にマッチするパターン（例：|親文字《ルビ》）
REG_PIPE_OYAMOJI = regex.compile(r'(?<=\|)([^|]+)(?=《)')
REG_PIPE_OYAMOJI_RUBY = regex.compile(r'\|([^|]+)《([^《》]+)》')
REG_PIPE_OYAMOJI_GET_AROUND = regex.compile(r'(\|[^|《》]+《[^《》]+》)')
# |《にマッチするパターン（《をそのまま出力したい場合）（正規表現でなくて良い）
REG_KEEP_BLACKET = regex.compile(r'\|《')
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
