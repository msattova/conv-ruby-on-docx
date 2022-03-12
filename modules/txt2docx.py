
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
    """[|, 親文字, 《, ル, ビ, 》]みたいになっているのを[|, 親文字《ルビ》]にする"""
    united = list()
    marks = dict()
    in_wr_flag = False
    start_wr: list[int] = list()
    end_wr: list[int] = list()
    now_close = False
    kr_flag = False
    piped_flag: bool = False
    ruby_flag = False
    striped = [bc.lstrip() for bc in basecode]
    for i, bc in enumerate(striped):
        if con.REG_WR.match(bc) is not None:
            in_wr_flag = False if in_wr_flag else True
            if in_wr_flag:
                start_wr.append(i)
            else:
                if not (piped_flag or ruby_flag or kr_flag or now_close):
                    marks=dict()
                elif kr_flag:
                    marks=dict()
                    united[-1] = {}
                end_wr.append(i)
                united.append(marks)
                marks = dict()
                kr_flag = False
                now_close = False
            continue
        if con.REG_TAG.match(bc) is None:
            match bc:
                case '|':
                    marks = dict()
                    kr_flag = False
                    marks['pipe'] = start_wr[-1]
                case '《':
                    marks['open'] = (bc, i)
                    piped_flag = False
                    ruby_flag = True
                case '》':
                    marks['close'] = (bc, i)
                    ruby_flag = False
                    now_close = True
            if piped_flag and bc != '《':
                marks['oyamoji'] = (bc, i)
            elif ruby_flag and bc != '》':
                marks['ruby'] = (bc, i)
        if con.REG_KANJI_AND_RUBY.match(bc):
            marks = dict()
            marks['kr'] = 1
            kr_flag = True
            piped_flag = False
    ref_tuple = tuple(z for z in zip(united, start_wr, end_wr)
                      if any(z[0])==True)

    #print(ref_tuple)
    ind: int = 0
    for i in ref_tuple:
        if i[0].get('oyamoji') is None:
            continue
        ind = i[0]['oyamoji'][1]
        for j, bc in enumerate(striped[ind:]):
            if bc == '》':
                break
            if con.REG_TAG.match(bc) is not None:
                basecode[j+ind] = ''
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
