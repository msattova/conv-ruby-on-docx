
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

#
# 猫《ねこ》の猿《さる》蟹《かに》ごっこには微塵も、興味《きょうみ》が湧《わ》かない
# ruby_kanji [[猫, ねこ], [猿, さる], [蟹, かに], [興味, きょうみ], [湧、 わ]]
# basetext [<rbt_0>, の, <rbt_1>, <rbt_2>, ごっこには微塵も, <rbt_3>, が, <rbt_4>, かない]
# 1. get_ruby_and_kanjiでもとの文字列からルビ対象箇所を<rbt_n>で置換して区切り文字を挿入。それ以外の場所はそのまま
# 2. 区切り文字でbasetextをsplit。
# 3. <rbt_n>のnはruby_kanjiの対応する位置の情報を保持
# そんなことしなくてもn番目の<rbt>ならruby_kanji[n]に対応、とすれば良い
# b&r ([yomi, kanji], [text1, rbt, text2], [False, True, False])
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
get_wr = r'<w:r>(?:(?!<w:r>|</w:r>).)*</w:r>'
# 《》内の文字列取得用パターン
get_ruby = r'(?<=《).*?(?=》)'
# 《》の前後で文字列分割
split_reg = r'《[^《》]*?》'
# タグにマッチするパターン
tag_reg = r'<[^<>]*>'
# 漢字《かんじ》にマッチするパターン
get_kanji_and_ruby = regex.compile(r'[\p{Script=Han}\u30F5]+《[^《》]*?》')
# 漢字にだけマッチするパターン
get_kanji = regex.compile(r'[\p{Script=Han}\u30F5]+')

