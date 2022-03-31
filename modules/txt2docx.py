
from enum import Enum, auto
from modules.consts import (make_template,
                    REG_TAG, REG_TAG_GET,
                    REG_KANJI_AND_RUBY,
                    REG_KANJI_AND_RUBY_AROUND,
                    REG_PIPE_OYAMOJI_RUBY,
                    REG_PIPE_OYAMOJI_GET_AROUND,
                    REG_BOUTEN_GET,
                    REG_BOUTEN_GET_INSIDE,
                    REG_PIPE,
                    REG_BOUTEN_OP, REG_BOUTEN_CL, REG_BOUTEN_OPCL,
                    REG_OP_SENTENCE, REG_CL_SENTENCE, REG_OPCL_SENTENCE,
                    )


class RubyType(Enum) :
    HASPIPE = auto()
    NONPIPE = auto()
    BOUTEN = auto()

def connect_serial_nontag(code: list[str]) -> list[str]:
    ref_code = tuple(i for i in code if i)
    tagmatch = REG_TAG.match
    for i, c in enumerate(ref_code):
        if len(code) <= (i+1):
            break
        else:
            if not code[i] :
                continue
            elif not (tagmatch(c) or tagmatch(ref_code[i+1])):
                code[i] = f"{code[i]}{code[i+1]}"
                code[i+1] = ""
    return [i for i in code if i != ""]

def filter_void_tag(code: str, opening: str, closing: str) -> str:
    # return re.sub(f"{opening}{closing}", "", code)
    return code.replace(f"{opening}{closing}", "")


def code_to_list(code: str) -> list[str]:
    """XMLをタグごと、テキスト文字列ごとに分割してリストに"""
    return [i for i in
            REG_TAG_GET.sub('\n\\1\n', code).splitlines()
            if i]

def isolate(ruby_type: RubyType, code: list[str], opening: str, closing: str) -> list[str]:
    match ruby_type:
        case RubyType.NONPIPE:
            pattern = REG_KANJI_AND_RUBY_AROUND
        case RubyType.HASPIPE:
            pattern = REG_PIPE_OYAMOJI_GET_AROUND
        case RubyType.BOUTEN:
            pattern = REG_BOUTEN_GET
        case _:
            return []
    psub = pattern.sub
    tagmatch = REG_TAG.match
    ref_code = tuple(i for i in code)
    tmp_code = [i for i in code]
    for i, c in enumerate(ref_code):
        if tagmatch(c):
            continue
        if ruby_type is RubyType.NONPIPE and REG_PIPE_OYAMOJI_GET_AROUND.match(c):
            continue
        elif ruby_type is RubyType.HASPIPE and REG_KANJI_AND_RUBY_AROUND.match(c):
            continue
        tmp_code[i] = psub(rf'{closing}{opening}\1{closing}{opening}', c)
    return code_to_list(filter_void_tag("".join(tmp_code), opening, closing))

def isolate_rubysets(code: list[str], opening: str, closing: str) -> list[str]:
    new_code = isolate(RubyType.HASPIPE, code, opening, closing)
    new_code = isolate(RubyType.NONPIPE, new_code, opening, closing)
    new_code = isolate(RubyType.BOUTEN, new_code, opening, closing)
    return new_code

def convert_basecode(basecode: list[str]) -> list[str]:
    ruby_flag = False
    ref_code = tuple(i for i in basecode)
    tagmatch = REG_TAG.match
    for ind, bc in enumerate(ref_code):
        if (REG_PIPE.search(bc)
                or REG_OP_SENTENCE.search(bc)
                or REG_BOUTEN_OP.search(bc)):
            ruby_flag = True
        if ruby_flag:
            #print(bc)
            if (REG_CL_SENTENCE.search(bc)
                    or REG_OPCL_SENTENCE.search(bc)
                    or REG_BOUTEN_CL.search(bc)
                    or REG_BOUTEN_OPCL.search(bc)):
                ruby_flag = False
            elif tagmatch(bc) :
                if bc == '<w:tab/>':
                    basecode[ind] = '\t'
                else:
                    basecode[ind] = ''
    #print(basecode)
    return connect_serial_nontag([i for i in basecode if i])

def replace_rubies(ruby_type: RubyType, template: tuple[str, str, str, str, str, str], code: str):
    match ruby_type:
        case RubyType.NONPIPE:
            pattern = REG_KANJI_AND_RUBY
        case RubyType.HASPIPE:
            pattern = REG_PIPE_OYAMOJI_RUBY
        case RubyType.BOUTEN:
            pattern = REG_BOUTEN_GET_INSIDE
        case _:
            return ''
    psub = pattern.sub
    tmp_code = code_to_list(code)
    ref_code = tuple(i for i in tmp_code)
    for i, c in enumerate(ref_code):
        if REG_TAG.match(c) or (not c):
            continue
        if ruby_type is RubyType.BOUTEN:
            tmp_code[i] = psub(rf"{template[4]}{template[5]}\1{template[4]}{template[3]}", c)
            continue
        tmp_code[i] = psub(rf"{template[4]}{template[0]}\2{template[1]}\1{template[2]}{template[3]}", c)
    return filter_void_tag("".join(tmp_code), template[3], template[4])

def replace_tabchar(template, code: str) -> str:
    if '\t' not in code:
        return code
    just_before_tags = []
    tagmatch = REG_TAG.match
    karajoin = "".join
    tmp_code = code_to_list(code)
    for i, c in enumerate(tmp_code):
        if tagmatch(c):
            if c == '</w:r>' or c == '</w:t>':
                just_before_tags = []
                continue
            just_before_tags.append(c)
        if '\t' in c:
            tmp_code[i] = c.replace('\t', f'{template[4]}<w:r><w:tab/></w:r>{karajoin(just_before_tags)}')
    return filter_void_tag(karajoin(tmp_code), template[3], template[4])

def replace_ruby(base: list[str], template: tuple) -> list[str]:
    joined = "".join(base)
    haspipe_proc = replace_rubies(RubyType.HASPIPE, template, joined)
    #print(f"result: \t{result}\n")
    nonpipe_proc = replace_rubies(RubyType.NONPIPE, template, haspipe_proc)
    bouten_proc = replace_rubies(RubyType.BOUTEN, template, nonpipe_proc)
    tab_proc = replace_tabchar(template, bouten_proc)
    #print(f"result2: \t{result2}\n")
    keep_proc = tab_proc.replace(r'|《', '《')
    #tab_proc = keep_proc.replace('\t', f'{template[4]}<w:r><w:tab/></w:r>{template[3]}')
    return keep_proc

def make_new_xml(ruby_font: str, em_style: str, code: str) -> str:
    """out.docx内のdocument.xmlに書き込む文字列生成"""
    match em_style:
        case 'dot':
            pass
        case 'comma':
            pass
        case _:
            em_style = 'dot'
    template = make_template(ruby_font, em_style)
    basecode = code_to_list(code)  # xmlを一行づつ分割
    each_lines = convert_basecode(basecode)
    each_lines = isolate_rubysets(each_lines, template[3], template[4])
    wrt = replace_ruby(each_lines, template)

    return wrt
