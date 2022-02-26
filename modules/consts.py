
import platform
import regex
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
         r'</w:ruby>', r'</w:r>'),#ルビ関連のタグここまで
        (r'<w:r><w:rPr>',
         r'<w:rFonts w:hint="eastAsia"/>',
         r'</w:rPr><w:t>'),
        # ルビ振り処理対象外の余った文字列をここに
        (r'</w:t>', r'</w:r>')))

def make_rubyset(template:tuple[str], furigana:str, kanji:str):
    #print('furigana: ', furigana)
    #print('kanji: ', kanji)
    return template[0]+furigana+template[1]+kanji+template[2]

def make_text(template:tuple[str], text:str):
    return template[3]+text+template[4]

# 置換後文字列を出力
def make_out(template:tuple[str], base_ruby:tuple) -> list[str]:
    out_list = list()
    for br in base_ruby:
        inner = list()
        ir = iter(br[0])
        for e in br[1]:
            #print('e', e)
            if e == f"#rbt!":
                inner.append(make_rubyset(template, furigana=next(ir), kanji=next(ir)))
            else:
                inner.append(make_text(template, text=e))
        out_list.append(''.join(inner))
        #print(f'inner, {inner}')
    #print(out_list)
    return out_list


# <w:r>タグで囲まれた文字列（<w:r>を含む）を取得するパターン
get_wr = r'<w:r>(?:(?!<w:r>|</w:r>).)*</w:r>' #make_new_xml内で1回しか利用されないのでコンパイルしない
# 《》内の文字列取得用パターン
get_ruby = regex.compile(r'(?<=《).*?(?=》)')
# タグにマッチするパターン
tag_reg = regex.compile(r'<[^<>]*>')
# 漢字《かんじ》にマッチするパターン
get_kanji_and_ruby = regex.compile(r'[\p{Script=Han}\u30F5]+《[^《》]*?》')
# 漢字にだけマッチするパターン
get_kanji = regex.compile(r'[\p{Script=Han}\u30F5]+')

