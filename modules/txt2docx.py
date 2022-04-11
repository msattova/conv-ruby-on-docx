
from tqdm import tqdm
from enum import Enum, auto
from modules.consts import (Template,
                            TemplateType,
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


class RubyType(Enum):
    HASPIPE = auto()
    NONPIPE = auto()
    BOUTEN = auto()


def connect_serial_nontag(code: list[str]) -> list[str]:
    ref_code = tuple(i for i in code if i)
    tagmatch = REG_TAG.match
    bar = tqdm(total=len(ref_code), desc="connect tag", leave=False)
    for i, c in enumerate(ref_code):
        if len(code) <= (i+1):
            bar.update(1)
            break
        if not code[i]:
            bar.update(1)
            continue
        elif not (tagmatch(c) or tagmatch(ref_code[i+1])):
            code[i] = f"{code[i]}{code[i+1]}"
            code[i+1] = ""
        bar.update(1)
    return [i for i in code if i]


def filter_void_tag(code: str, opening: str, closing: str) -> str:
    return code.replace(f"{opening}{closing}", "")


def code_to_list(code: str) -> list[str]:
    """XMLをタグごと、テキスト文字列ごとに分割してリストに"""
    return [i for i in
            REG_TAG_GET.sub('\n\\1\n', code).splitlines()
            if i]


def isolate(ruby_type: RubyType, code: list[str], opening: str, closing: str) -> list[str]:
    desc_message: str
    match ruby_type:
        case RubyType.NONPIPE:
            pattern = REG_KANJI_AND_RUBY_AROUND
            desc_message = "ruby without pipe"
        case RubyType.HASPIPE:
            pattern = REG_PIPE_OYAMOJI_GET_AROUND
            desc_message = "ruby with pipe"
        case RubyType.BOUTEN:
            pattern = REG_BOUTEN_GET
            desc_message = "bouten"
        case _:
            return []
    psub = pattern.sub
    tagmatch = REG_TAG.match
    oyamatch = REG_PIPE_OYAMOJI_GET_AROUND.match
    kanjimatch = REG_KANJI_AND_RUBY_AROUND.match
    ref_code = tuple(i for i in code)
    tmp_code = [i for i in code]
    bar = tqdm(total=len(ref_code), desc=desc_message, leave=False)
    for i, c in enumerate(ref_code):
        if tagmatch(c):
            bar.update(1)
            continue
        if ruby_type is RubyType.NONPIPE and oyamatch(c):
            bar.update(1)
            continue
        elif ruby_type is RubyType.HASPIPE and kanjimatch(c):
            bar.update(1)
            continue
        tmp_code[i] = psub(rf'{closing}{opening}\1{closing}{opening}', c)
        bar.update(1)
    return code_to_list(filter_void_tag("".join(tmp_code), opening, closing))


def isolate_rubysets(code: list[str], opening: str, closing: str) -> list[str]:
    new_code = code
    for type in tqdm(RubyType, desc="isolate", leave=False):
        new_code = isolate(type, code, opening, closing)
    return new_code


def convert_basecode(basecode: list[str]) -> list[str]:
    ruby_flag = False
    ref_code = tuple(i for i in basecode)
    tagmatch = REG_TAG.match
    bar = tqdm(total=len(ref_code), desc="convert code", leave=False)
    for ind, bc in enumerate(ref_code):
        if (REG_PIPE.search(bc)
                or REG_OP_SENTENCE.search(bc)
                or REG_BOUTEN_OP.search(bc)):
            ruby_flag = True
        if ruby_flag:
            if (REG_CL_SENTENCE.search(bc)
                    or REG_OPCL_SENTENCE.search(bc)
                    or REG_BOUTEN_CL.search(bc)
                    or REG_BOUTEN_OPCL.search(bc)):
                ruby_flag = False
            elif tagmatch(bc):
                basecode[ind] = '\t' if (bc == '<w:tab/>') else ''
        bar.update(1)
    return connect_serial_nontag([i for i in basecode if i])


def replace_rubies(
        ruby_type: RubyType,
        template: TemplateType,
        code: str) -> str:
    desc_message: str
    match ruby_type:
        case RubyType.NONPIPE:
            desc_message = "ruby without pipe"
            pattern = REG_KANJI_AND_RUBY
        case RubyType.HASPIPE:
            desc_message = "ruby with pipe"
            pattern = REG_PIPE_OYAMOJI_RUBY
        case RubyType.BOUTEN:
            desc_message = "bouten"
            pattern = REG_BOUTEN_GET_INSIDE
        case _:
            return ''
    psub = pattern.sub
    tmp_code = code_to_list(code)
    ref_code = tuple(i for i in tmp_code)
    bar = tqdm(total=len(ref_code), desc=desc_message, leave=False)
    for i, c in enumerate(ref_code):
        if REG_TAG.match(c) or (not c):
            bar.update(1)
            continue
        if ruby_type is RubyType.BOUTEN:
            tmp_code[i] = psub(
                rf"{template.general_end}{template.bouten_open}\1{template.general_end}{template.general_open}",
                c)
            bar.update(1)
            continue
        tmp_code[i] = psub(
            rf"{template.general_end}{template.ruby_open}\2{template.ruby_end}{template.oyamoji_open}\1{template.oyamoji_end}{template.general_open}",
            c)
        bar.update(1)
    return filter_void_tag("".join(tmp_code), template.general_open, template.general_end)


def replace_tabchar(template: TemplateType, code: str) -> str:
    if '\t' not in code:
        return code
    just_before_tags: list[str] = []
    tagmatch = REG_TAG.match
    karajoin = "".join
    tmp_code = code_to_list(code)
    bar = tqdm(total=len(tmp_code), desc="replace tab", leave=False)
    for i, c in enumerate(tmp_code):
        if tagmatch(c):
            if c == '</w:r>' or c == '</w:t>':
                just_before_tags = []
                bar.update(1)
                continue
            just_before_tags.append(c)
        if '\t' in c:
            tmp_code[i] = c.replace(
                '\t',
                f'{template.general_end}<w:r><w:tab/></w:r>{karajoin(just_before_tags)}')
        bar.update(1)
    return filter_void_tag(karajoin(tmp_code), template.general_open, template.general_end)


def replace_ruby(
        base: list[str],
        template: TemplateType) -> str:
    ret_str = "".join(base)
    for type in tqdm(RubyType, desc="replace", leave=False):
        ret_str = replace_rubies(type, template, ret_str)
    ret_str = replace_tabchar(template, ret_str)
    return ret_str.replace(r'|《', '《')


def make_new_xml(ruby_font: str, emtype: str, code: str) -> str:
    """out.docx内のdocument.xmlに書き込む文字列生成"""
    template = Template(font=ruby_font, emtype=emtype).template
    basecode = code_to_list(code)  # xmlを一行づつ分割
    each_lines = convert_basecode(basecode)
    each_lines = isolate_rubysets(
        each_lines, template.general_open, template.general_end)
    wrt = replace_ruby(each_lines, template)

    return wrt
