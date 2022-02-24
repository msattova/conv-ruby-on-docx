
import re

from bs4 import BeautifulSoup as bs4

from . import consts as con


def make_new_xml(code: str) -> str:

    nc = re.sub(r'\s|\n', '', code)
    iwr = iter(re.findall(con.get_wr, nc))

    # 置き換え対象
    replace_target = list()

    for s in iwr:
        if re.search(r'\|', str(s)):
            replace_target.append(str(next(iwr)))

    ruby_text = list()
    splited_text = list()
    for s in replace_target:
        ruby_text += re.findall(con.get_ruby, s)
        # タグを消去
        elaced = re.sub(con.tag_reg, '', s).strip()
        splited_text.append(re.split(con.split_reg, elaced))

    outs = list()
    out = ''
    wrt = ''
    rbtemplate = con.make_template()
    for i in range(len(ruby_text)):
        out = ''
        out = (''.join(rbtemplate[0]) + ruby_text[i].strip()
               + ''.join(rbtemplate[1]) + splited_text[i][0].strip()
               + ''.join(rbtemplate[2]) + splited_text[i][1].strip()
               + ''.join(rbtemplate[3]))
        outs.append(out)

    iouts = iter(outs)

    soup = bs4(code, 'xml')
    sep_char = '!@sep$@'
    separated = iter(soup.get_text(sep_char).split(sep_char))
    print(soup.get_text(sep_char).split(sep_char))
    ps = [i.lstrip() for i in soup.prettify().splitlines()]

    # ルビ振り置換前処理
    in_wr_flag = False
    start_wr = list()
    end_wr = list()
    in_ruby = list()
    for i, x in enumerate(ps):
        if r"<w:r>" == x.strip():
            in_wr_flag = True
            start_wr.append(i)
            continue
        elif r"</w:r>" == x.strip():
            in_wr_flag = False
            end_wr.append(i)
            if len(end_wr) != len(in_ruby):
                in_ruby.append(False)
            continue

        if in_wr_flag and r"|" == x.strip():
            in_ruby.append(True)
        # タグじゃなければ、その行をseparatedで置換
        # 元から"<tag>"のような文字列が含まれていると正しく処理されない
        if re.match(con.tag_reg, x.strip()) is None:
            print(i, x)
            ps[i] = next(separated)
            print(i, ps[i])
            #print(re.match(con.tag_reg, x.strip()))

    print(len(in_ruby), len(start_wr), len(end_wr))
    # ルビ振り置換
    rubysets = iter(zip(in_ruby, start_wr, end_wr))
    tmp = list()
    for rs in rubysets:
        if not rs[0]:
            continue
        else:
            tmp = list()
            start = int(rs[1])
            _, _, end2 = next(rubysets)
            tmp.append(str(next(iouts)))  # 要素数1のリストを作成するための措置
            #print(tmp)
            ps[start:(end2+1)] = (['']*(end2-start)+tmp)

    for i in ps:
        if i == '':
            continue
        else:
            wrt += i

    return wrt
