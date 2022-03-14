
from email.mime import base
import re
from enum import Enum, auto
from typing import Iterable, Iterator
from bs4 import BeautifulSoup as bs4

from . import consts as con


class RubyType(Enum):
    NOTHING = auto()  # ルビも傍点も振らない
    HASPIPE = auto()  # パイプ有りルビ
    NONPIPE = auto()  # パイプなしルビ
    RUBY    = HASPIPE | NONPIPE #ルビを振る
    BOUTEN  = auto()  # 傍点

def convert_basecode(basecode: list[str]) -> list[str]:
    ruby_flag = False
    for ind, bc in enumerate(i for i in basecode):
        if (con.REG_PIPE.match(bc) or con.REG_OP_SENTENCE.match(bc)) is not None:
            ruby_flag = True
            print(f'open: {bc}')
        if ruby_flag:
            if (con.REG_CL_SENTENCE.match(bc) or con.REG_OPCL_SENTENCE.match(bc)) is not None:
                ruby_flag = False
            elif con.REG_TAG.match(bc) is not None:
                basecode[ind] = ''
    return [i for i in basecode if i!= ""]

def make_replstr_list(ruby_font: str, in_wr_strs: Iterator) -> list:
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
        elaced = con.REG_TAG.sub('', s).strip()  # タグを消去
        tmp= [i for i in
                con.REG_KANJI_AND_RUBY.sub(
                    INTO_SYMBOL, elaced).split(con.SPLIT_SYMBOL)
                if i != '']
        nonruby_text.append(tmp)
    for rk in ruby_kanji:
        tmp = list()
        for part in rk:
            tmp += con.REG_RUBY.findall(part)
            tmp += con.REG_KANJI.findall(part)
        ruby_text.append(tmp)
    rbtemplate = con.make_template(ruby_font)
    #print('rtxt:\t', ruby_text)
    #print('nrtx:\t', nonruby_text)
    base_and_ruby = zip(ruby_text, nonruby_text)
    return con.make_out(rbtemplate, base_and_ruby)


def make_reflist(each_lines:list[str],
                holded_text:Iterator) -> tuple[Iterable, list[str]]:
    """ ルビ振り処理に参照するオブジェクトを生成"""
    in_wr_flag = False
    start_wr: list[int]      = list()
    end_wr:   list[int]      = list()
    in_ruby:  list[RubyType] = list()
    ref_text: list[str]      = list()
    #print(each_lines)
    for i, x in enumerate(each_lines):
        striped = x.strip()
        if con.REG_WR.match(striped) is not None:
            in_wr_flag = False if in_wr_flag else True
            if in_wr_flag:
                start_wr.append(i)
            else:
                end_wr.append(i)
                if len(end_wr) != len(in_ruby):
                    in_ruby.append(RubyType.NOTHING)
            continue
        if not in_wr_flag or con.REG_TAG.match(striped) is not None:
            continue
        # タグじゃなければ、その行をholded_textで置換
        # 元から"<tag>"のような文字列が含まれていると正しく処理されない
        tmp = next(holded_text)
        each_lines[i] = tmp
        #print('tmp:', tmp)
        #print('striped: ', striped)
        if r"|" == striped:
            in_ruby.append(RubyType.HASPIPE)
        elif con.REG_KANJI_AND_RUBY.search(striped):
            in_ruby.append(RubyType.NONPIPE)
        ref_text.append(striped)
    rbset = zip(in_ruby, start_wr, end_wr)
    #print(tuple(rbset))
    return (rbset, each_lines)


def repl_ruby(rubysets: Iterable,
                repl_strs: Iterator,
                each_lines: list[str]) -> list[str]:
    """ルビ振り置換"""
    replaced_lines = each_lines
    #i = 0
    for rs in rubysets:
        if rs[0] is RubyType.NOTHING:
            continue
        else:
            tmp = list()
            start = rs[1]
            t = next(repl_strs)
            tmp.append(t)  # 要素数1のリストを作成するための措置
            if rs[0] is RubyType.HASPIPE:
                conf = next(rubysets)
                _, _, end = conf
            elif rs[0] is RubyType.NONPIPE:
                end = rs[2]
            replaced_lines[start:(end+1)] = (['']*(end-start)+tmp)

    return replaced_lines


def make_new_xml(ruby_font: str, code: str) -> str:
    """out.docx内のdocument.xmlに書き込む文字列生成"""
    nc = re.sub(r'\s|\n', '', code)
    in_wr_str = iter(re.findall(con.REG_SURROUND_WR, nc))
    #print(re.findall(con.REG_SURROUND_WR, nc))
    soup = bs4(code, 'xml')
    holded_text = iter(soup.get_text(con.SEPARATE_SYMBOL)
                         .split(con.SEPARATE_SYMBOL))  # 元のテキストデータを分割して保持
    each_lines = [i.lstrip() for i in soup.prettify().splitlines()] # xmlを一行づつ分割
    #print("".join(each_lines))
    each_lines = convert_basecode(each_lines)
    #print("".join(each_lines))
    repl_strs = iter(make_replstr_list(ruby_font, in_wr_str))
    rubysets, each_lines = make_reflist(each_lines, holded_text)
    #print(tuple(rubysets))
    replaced_lines = repl_ruby(rubysets, repl_strs, each_lines)
    wrt = ''.join(replaced_lines)

    return wrt
