
from email.mime import base
import re
import regex
from enum import Enum, auto
from bs4 import BeautifulSoup as bs4

from . import consts as con

class RubyType(Enum):
    NOTHING = auto() #ルビも傍点も振らない
    YOUPIPE = auto() #パイプ有りルビ(zh:有パイプ)
    NONPIPE = auto() #パイプなしルビ
    BOUTEN  = auto() #傍点

def make_new_xml(code: str) -> str:

    nc = re.sub(r'\s|\n', '', code)
    iwr = iter(re.findall(con.get_wr, nc))

    # 置き換え対象
    replace_target = list()

    for s in iwr:
        if re.search(r'\|', str(s)):
            replace_target.append(str(next(iwr)))
        elif con.get_kanji_and_ruby.search(str(s)):
            replace_target.append(str(s))
    #print(replace_target)
    ruby_kanji = list()
    ruby_text = list()
    nonruby_text = list()
    has_amari = list()#ルビ処理に関係ない文字列が含まれるかどうか
    # b&r ([yomi, kanji], [text1, rbt, text2], [False, True, False])
    #
    for s in replace_target:
        tmp_list = list()
        #print('get_k&r', con.get_kanji_and_ruby.findall(s))
        ruby_kanji.append(con.get_kanji_and_ruby.findall(s))
        # タグを消去
        elaced = re.sub(con.tag_reg, '', s).strip()
        #print('elaced', elaced)
        tmp_list = [ i for i in con.get_kanji_and_ruby.sub(f'~#rbt!~', elaced).split('~') if i != '']
        #if len(tmp_list) == 1:
        #print('split', tmp_list)
        nonruby_text.append(tmp_list)
    #print('nonruby', nonruby_text)
    #print(ruby_kanji, len(nonruby_text))
    for rklist in ruby_kanji:
        rtxt = list()
        for part in rklist:
            rtxt += re.findall(con.get_ruby, part)
            #print('ruby', rtxt)
            rtxt += con.get_kanji.findall(part)
        ruby_text.append(rtxt)
    #print('ruby_text', ruby_text)
    outs = list()
    wrt = ''
    rbtemplate = con.make_template()
    base_and_ruby = tuple(zip(ruby_text, nonruby_text))
    #print('b&r', base_and_ruby)
    outs = con.make_out(rbtemplate, base_and_ruby )
    iouts = iter(outs)

    soup = bs4(code, 'xml')
    sep_char = '!@sep$@'
    separated = iter(soup.get_text(sep_char).split(sep_char))
    #print(soup.get_text(sep_char).split(sep_char))
    ps = [i.lstrip() for i in soup.prettify().splitlines()]

    # ルビ振り置換前処理
    in_wr_flag = False
    start_wr = list()
    end_wr = list()
    in_ruby: list[RubyType] = list()
    for i, x in enumerate(ps):
        if r"<w:r>" == x.strip():
            in_wr_flag = True
            start_wr.append(i)
            continue
        elif r"</w:r>" == x.strip():
            in_wr_flag = False
            end_wr.append(i)
            if len(end_wr) != len(in_ruby):
                in_ruby.append(RubyType.NOTHING)
            continue
        if not in_wr_flag:
            continue
        # タグじゃなければ、その行をseparatedで置換
        # 元から"<tag>"のような文字列が含まれていると正しく処理されない
        if re.match(con.tag_reg, x.strip()) is None:
            #print(i, x)
            ps[i] = next(separated)
        if r"|" == x.strip():
            #print(x)
            in_ruby.append(RubyType.YOUPIPE)
        elif in_wr_flag and con.get_kanji_and_ruby.search(x.strip()):
            in_ruby.append(RubyType.NONPIPE)

    #print(len(in_ruby), len(start_wr), len(end_wr))
    # ルビ振り置換
    rubysets = iter(zip(in_ruby, start_wr, end_wr))
    #print(list(rubysets))
    tmp = list()
    for rs in rubysets:
        #print('rs', rs)
        if rs[0] == RubyType.NOTHING:
            continue
        elif rs[0] == RubyType.YOUPIPE:
            tmp = list()
            start = rs[1]
            _, _, end2 = next(rubysets)
            tmp.append(str(next(iouts)))  # 要素数1のリストを作成するための措置
            #print(tmp)
            ps[start:(end2+1)] = (['']*(end2-start)+tmp)
        elif rs[0] == RubyType.NONPIPE:
            tmp = list()
            start = rs[1]
            end = rs[2]
            t = str(next(iouts))
            tmp.append(t)  # 要素数1のリストを作成するための措置
            print(tmp)
            ps[start:(end+1)] = (['']*(end-start)+tmp)

    for i in ps:
        if i == '':
            continue
        else:
            wrt += i

    return wrt
