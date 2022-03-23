

import re

from . import consts as con

def connect_serial_nontag(code: list[str]) -> list[str]:
    tmp_code = tuple(i for i in code)
    for i, c in enumerate(tmp_code):
        if len(code) < (i+1):
            break
        else:
            if c == "" or code[i] == "" :
                continue
            elif not (con.REG_TAG.match(c) or con.REG_TAG.match(tmp_code[i+1])):
                print(f"tmp_len: {len(tmp_code)} code_len: {len(code)} now_i: {i}")
                code[i] = code[i]+code[i+1]
                code[i+1] = ""
    return [i for i in code if i!=""]


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
    return connect_serial_nontag([i for i in basecode if i!= ''])


def split_code(code: str) -> list[str]:
    return [i for i in re.sub(
            r'(<[^<>]*>)', "\n\\1\n", code).splitlines()
            if i != "" ]

def replace_rubies_with_pipe(template: list[str], code: str):
    return con.REG_PIPE_OYAMOJI_RUBY.sub(
        rf"</w:t></w:r>{template[0]}\2{template[1]}\1{template[2]}<w:r><w:t>", code)


def replace_rubies_without_pipe(template: list[str], code: str):
    return con.REG_KANJI_AND_RUBY.sub(
        rf"</w:t></w:r>{template[0]}\2{template[1]}\1{template[2]}<w:r><w:t>", code)

def replace_ruby(base: list[str], ruby_font: str):
    joined = "".join(base)
    f = con.REG_PIPE_OYAMOJI_RUBY.findall(joined)
    print(f"findall: {f}")
    template = con.make_template(ruby_font)
    result = replace_rubies_with_pipe(template, joined)
    result2 = replace_rubies_without_pipe(template, result)
    #result3 = con.REG_KEEP_BLACKET.sub(r"《", result2)

    print(f"result: {result2}")

    return result2

def make_new_xml(ruby_font: str, code: str) -> str:
    """out.docx内のdocument.xmlに書き込む文字列生成"""
    each_lines = split_code(code)  # xmlを一行づつ分割
    each_lines = convert_basecode(each_lines)
    #print(each_lines)
    wrt = replace_ruby(each_lines, ruby_font)

    return wrt
