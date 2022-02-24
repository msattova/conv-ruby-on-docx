
import platform
from typing import Iterable, Iterator

def make_template()->tuple:
    pf = platform.system()
    if pf == 'Windows':
        font = 'ＭＳ 明朝'
    elif pf == 'Darwin':
        font = 'ヒラギノ明朝 ProN '
    elif pf == 'Linux': #Linux環境の場合はOSごとに標準でインストールされてるフォントが違うので要改善
        font = 'Noto Serif CJK JP'
    else: #その他の結果が出た場合
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
         r'<w:t>'),
        # ここにルビ文字列（例：ふりがな）
        (r'</w:t>',
         r'</w:r>',
         r'</w:rt>',
         r'<w:rubyBase>',
         r'<w:r w:rsidR="00E95970">',
         r'<w:rPr>',
         r'<w:rFonts w:hint="eastAsia"/>',
         r'</w:rPr>',
         r'<w:t>'),
        # ここにルビを振る文字列（例：振仮名）
        (r'</w:t>', r'</w:r>', r'</w:rubyBase>',
         r'</w:ruby>', r'</w:r>', r'<w:r><w:rPr>',
         r'<w:rFonts w:hint="eastAsia"/>',
         r'</w:rPr><w:t>'),
        # ルビ振り処理対象外の余った文字列をここに
        (r'</w:t>', r'</w:r>')))


def make_out(template:tuple[str], furigana: str, kanji: str, amari: str) -> str:
    return ''.join((template[0], furigana,
                        template[1], kanji,
                        template[2], amari,
                        template[3]))

# <w:r>タグで囲まれた文字列（<w:r>を含む）を取得するパターン
get_wr = r'<w:r>(?:(?!<w:r>|</w:r>).)*</w:r>'
# 《》内の文字列取得用パターン
get_ruby = r'(?<=《).*?(?=》)'
# 《》の前後で文字列分割
split_reg = r'《.*?》'
# タグにマッチするパターン
tag_reg = r'<[^<>]*>'
