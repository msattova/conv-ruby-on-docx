
from dataclasses import replace
import re
from enum import Enum,auto
from . import consts as con

class RubyType(Enum) :
    HASPIPE = auto()
    NONPIPE = auto()
    BOUTEN = auto()

def connect_serial_nontag(code: list[str]) -> list[str]:
    tmp_code = tuple(i for i in code)
    for i, c in enumerate(tmp_code):
        if len(code) < (i+1):
            break
        else:
            if c == "" or code[i] == "" :
                continue
            elif not (con.REG_TAG.match(c) or con.REG_TAG.match(tmp_code[i+1])):
                code[i] = code[i]+code[i+1]
                code[i+1] = ""
    return [i for i in code if i!=""]

def filter_void_tag(code: str, opening: str, closing: str) -> str:
    return re.sub(f"{opening}{closing}", "", code)

def code_to_list(code: str) -> list[str]:
    return [i for i in
            re.sub(r'(<[^<>]+>)', '\n\\1\n', code).splitlines()
        if i != '']

def isolate(ruby_type: RubyType, code: list[str], opening: str, closing: str) -> list[str]:
    match ruby_type:
        case RubyType.NONPIPE:
            pattern = con.REG_KANJI_AND_RUBY_AROUND
        case RubyType.HASPIPE:
            pattern = con.REG_PIPE_OYAMOJI_GET_AROUND
        case RubyType.BOUTEN:
            pattern = con.REG_BOUTEN_GET
        case _:
            return []
    ref_code = tuple(i for i in code)
    tmp_code = [i for i in code]
    for i, c in enumerate(ref_code):
        if con.REG_TAG.match(c) or c == '':
            continue
        if ruby_type == RubyType.NONPIPE and con.REG_PIPE_OYAMOJI_GET_AROUND.match(c):
            continue
        elif ruby_type == RubyType.HASPIPE and con.REG_KANJI_AND_RUBY_AROUND.match(c):
            continue
        tmp_code[i] = pattern.sub(
            rf'{closing}{opening}\1{closing}{opening}', c)
        if ruby_type == RubyType.BOUTEN:
            print(tmp_code[i])
    return code_to_list(filter_void_tag("".join(tmp_code), opening, closing))

def isolate_rubysets(code: list[str], opening: str, closing: str) -> list[str]:
    new_code = isolate(RubyType.HASPIPE, code, opening, closing)
    new_code = isolate(RubyType.NONPIPE, new_code, opening, closing)
    new_code = isolate(RubyType.BOUTEN, new_code, opening, closing)
    return new_code

def convert_basecode(basecode: list[str]) -> list[str]:
    ruby_flag = False
    ref_code = tuple(i for i in basecode)
    for ind, bc in enumerate(i for i in ref_code):
        if ((con.REG_PIPE.search(bc)
                or con.REG_OP_SENTENCE.search(bc)
                or con.REG_BOUTEN_OP.search(bc)) is not None):
            ruby_flag = True
        if ruby_flag:
            print(bc)
            if ((con.REG_CL_SENTENCE.search(bc)
                    or con.REG_OPCL_SENTENCE.search(bc)
                    or con.REG_BOUTEN_CL.search(bc)
                    or con.REG_BOUTEN_OPCL.search(bc)) is not None):
                ruby_flag = False
            elif con.REG_TAG.match(bc) is not None:
                basecode[ind] = ''
    print(basecode)
    return connect_serial_nontag([i for i in basecode if i!= ''])

def replace_rubies(ruby_type: RubyType, template: tuple[str, str, str, str, str], code: str):
    match ruby_type:
        case RubyType.NONPIPE:
            pattern = con.REG_KANJI_AND_RUBY
        case RubyType.HASPIPE:
            pattern = con.REG_PIPE_OYAMOJI_RUBY
        case RubyType.BOUTEN:
            pattern = con.REG_BOUTEN_GET_INSIDE
        case _:
            return []
    tmp_code = code_to_list(code)
    ref_code = tuple(i for i in tmp_code)
    for i, c in enumerate(ref_code):
        if con.REG_TAG.match(c) or c == '':
            continue
        if ruby_type == RubyType.BOUTEN:
            tmp_code[i] = pattern.sub(
                rf"{template[4]}{template[5]}\1{template[4]}{template[3]}", c)
            continue
        tmp_code[i] = pattern.sub(
            rf"{template[4]}{template[0]}\2{template[1]}\1{template[2]}{template[3]}", c)
    return filter_void_tag("".join(tmp_code), template[3], template[4])

def replace_ruby(base: list[str], template: tuple) -> list[str]:
    joined = "".join(base)
    haspipe_proc = replace_rubies(RubyType.HASPIPE, template, joined)
    #print(f"result: \t{result}\n")
    nonpipe_proc = replace_rubies(RubyType.NONPIPE, template, haspipe_proc)
    bouten_proc = replace_rubies(RubyType.BOUTEN, template, nonpipe_proc)
    #print(f"result2: \t{result2}\n")
    keep_proc = con.REG_KEEP_BLACKET.sub(r"《", bouten_proc)
    return keep_proc

def make_new_xml(ruby_font: str, code: str) -> str:
    """out.docx内のdocument.xmlに書き込む文字列生成"""
    template = con.make_template(ruby_font)
    basecode = code_to_list(code)  # xmlを一行づつ分割
    each_lines = convert_basecode(basecode)
    each_lines = isolate_rubysets(each_lines, template[3], template[4])
    wrt = replace_ruby(each_lines, template)

    return wrt
