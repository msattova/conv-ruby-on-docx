
import re
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
    ruby_kanji = list()
    ruby_text = list()
    nonruby_text = list()
    for s in replace_target:
        tmp_list = list()
        ruby_kanji.append(con.get_kanji_and_ruby.findall(s))
        # タグを消去
        elaced = con.tag_reg.sub('', s).strip()
        tmp_list = [ i for i in con.get_kanji_and_ruby.sub('~#rbt!~', elaced).split('~') if i != '']
        nonruby_text.append(tmp_list)
    for rklist in ruby_kanji:
        rtxt = list()
        for part in rklist:
            rtxt += con.get_ruby.findall(part)
            rtxt += con.get_kanji.findall(part)
        ruby_text.append(rtxt)
    outs = list()
    wrt = ''
    rbtemplate = con.make_template()
    base_and_ruby = tuple(zip(ruby_text, nonruby_text))
    outs = con.make_out(rbtemplate, base_and_ruby )
    iouts = iter(outs)

    soup = bs4(code, 'xml')
    sep_char = '!@sep$@'
    separated = iter(soup.get_text(sep_char).split(sep_char))
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
            if len(end_wr) != len(in_ruby): #w:rタグが終わるまでin_rubyに要素がappendされてなければ
                in_ruby.append(RubyType.NOTHING)
            continue
        if not in_wr_flag:
            continue
        # タグじゃなければ、その行をseparatedで置換
        # 元から"<tag>"のような文字列が含まれていると正しく処理されない
        if con.tag_reg.match(x.strip()) is None:
            ps[i] = next(separated)
        if r"|" == x.strip():
            in_ruby.append(RubyType.YOUPIPE)
        elif in_wr_flag and con.get_kanji_and_ruby.search(x.strip()):
            in_ruby.append(RubyType.NONPIPE)

    # ルビ振り置換
    rubysets = iter(zip(in_ruby, start_wr, end_wr))
    tmp = list()
    for rs in rubysets:
        if rs[0] is RubyType.NOTHING:
            continue
        else:
            tmp = list()
            start = rs[1]
            t = str(next(iouts))
            if rs[0] is RubyType.YOUPIPE:
                _, _, end = next(rubysets)#`|`（パイプ）の次の文字列がルビ振り対象文字列なので
            elif rs[0] is RubyType.NONPIPE:
                end = rs[2]
            tmp.append(t)  # 要素数1のリストを作成するための措置
            ps[start:(end+1)] = (['']*(end-start)+tmp)

    for i in ps:
        if i == '':
            continue
        else:
            wrt += i

    return wrt
