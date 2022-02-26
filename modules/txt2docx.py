
import re
from enum import Enum, auto
from typing import Iterable, Iterator
from bs4 import BeautifulSoup as bs4

from . import consts as con


class RubyType(Enum):
    NOTHING = auto()  # ルビも傍点も振らない
    HASPIPE = auto()  # パイプ有りルビ
    NONPIPE = auto()  # パイプなしルビ
    BOUTEN = auto()   # 傍点


def make_replstr_list(in_wr_strs: Iterator) -> list:
    """置き換え対象文字列リストの生成"""
    replace_target = list()
    for s in in_wr_strs:
        if con.REG_PIPE.search(s):
            replace_target.append(next(in_wr_strs))
        elif con.REG_KANJI_AND_RUBY.search(s):
            replace_target.append(s)
    ruby_kanji = list()
    ruby_text = list()
    nonruby_text = list()
    INTO_SYMBOL = con.SPLIT_SYMBOL + con.REPL_SYMBOL + con.SPLIT_SYMBOL
    for s in replace_target:
        ruby_kanji.append(con.REG_KANJI_AND_RUBY.findall(s))
        # タグを消去
        elaced = con.REG_TAG.sub('', s).strip()
        tmp_list = [i for i in
                    con.REG_KANJI_AND_RUBY.sub(
                        INTO_SYMBOL, elaced).split(con.SPLIT_SYMBOL)
                    if i != '']
        nonruby_text.append(tmp_list)
    for rklist in ruby_kanji:
        rtxt = list()
        for part in rklist:
            rtxt += con.REG_RUBY.findall(part)
            rtxt += con.REG_KANJI.findall(part)
        ruby_text.append(rtxt)
    rbtemplate = con.make_template()
    base_and_ruby = tuple(zip(ruby_text, nonruby_text))
    return con.make_out(rbtemplate, base_and_ruby)


def make_reflist(ps, separated):
    """ ルビ振り処理に参照するオブジェクトを生成"""
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
            # w:rタグが終わるまでin_rubyに要素がappendされてなければRubyType.NOTHINGを追加
            if len(end_wr) != len(in_ruby):
                in_ruby.append(RubyType.NOTHING)
            continue
        if not in_wr_flag:
            continue
        # タグじゃなければ、その行をseparatedで置換
        # 元から"<tag>"のような文字列が含まれていると正しく処理されない
        if con.REG_TAG.match(x.strip()) is None:
            ps[i] = next(separated)
        if r"|" == x.strip():
            in_ruby.append(RubyType.HASPIPE)
        elif in_wr_flag and con.REG_KANJI_AND_RUBY.search(x.strip()):
            in_ruby.append(RubyType.NONPIPE)
    return zip(in_ruby, start_wr, end_wr)


def repl_ruby(rubysets: Iterable, iouts, ps):
    """ルビ振り置換"""
    for rs in rubysets:
        if rs[0] is RubyType.NOTHING:
            continue
        else:
            tmp = list()
            start = rs[1]
            t = str(next(iouts))
            tmp.append(t)  # 要素数1のリストを作成するための措置
            if rs[0] is RubyType.HASPIPE:
                # `|`（パイプ）の次の文字列がルビ振り対象文字列なのでnext()を使う
                _, _, end = next(rubysets)
            elif rs[0] is RubyType.NONPIPE:
                end = rs[2]
            ps[start:(end+1)] = (['']*(end-start)+tmp)
    return ps


def make_new_xml(code: str) -> str:
    """out.docx内のdocument.xmlに書き込む文字列生成"""
    nc = re.sub(r'\s|\n', '', code)
    in_wr_str = iter(re.findall(con.REG_WR, nc))

    soup = bs4(code, 'xml')
    separated = iter(soup.get_text(con.SEPARATE_SYMBOL)
                         .split(con.SEPARATE_SYMBOL))  # 元のテキストデータをリストにして保持
    ps = [i.lstrip() for i in soup.prettify().splitlines()]

    iouts = iter(make_replstr_list(in_wr_str))
    rubysets = make_reflist(ps, separated)
    ps = repl_ruby(rubysets, iouts, ps)
    wrt = ''.join(ps)

    return wrt
