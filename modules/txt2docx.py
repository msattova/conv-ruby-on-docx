
import re

from bs4 import BeautifulSoup as bs4

from . import consts as con


def make_new_xml(code: str) -> str:

    nc = re.sub(r'\s|\n', '', code)
    wr = re.findall(con.get_wr, nc)
    iwr = iter(wr)

    # 置き換え対象
    replace_target = list()

    for s in iwr:
        st = str(s)
        if re.search(r'\|', str(s)):
            replace_target.append(str(next(iwr)))

    ruby_text = list()
    splited_text = list()
    for s in replace_target:
        ruby_text += re.findall(con.get_ruby, s)
        # タグを消去
        elaced = re.sub(con.tag_reg, '', s).strip()
        splited_text.append(re.split(con.split_reg, elaced))

    l = len(ruby_text)

    outs = list()
    out = ''
    wrt = ''
    rbtemplate = con.make_template()
    for i in range(l):
        out = ''
        out = (rbtemplate[0].strip() + ruby_text[i].strip()
               + rbtemplate[1].strip() + splited_text[i][0].strip()
               + rbtemplate[2].strip() + rbtemplate[3].strip()
               + splited_text[i][1].strip() + rbtemplate[4].strip()
               )
        outs.append(out)

    iouts = iter(outs)

    soup = bs4(code, 'lxml-xml')
    ps = [i.lstrip() for i in soup.prettify().split('\n')]

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

    rubysets = iter(zip(in_ruby, start_wr, end_wr))
    tmp = list()
    for rs in rubysets:
        if not rs[0]:
            continue
        else:
            tmp = list()
            start = int(rs[1])
            end = int(rs[2])+1
            _, _, end2 = next(rubysets)
            tmp.append(str(next(iouts)))  # 要素数1のリストを作成するための措置
            # print(tmp)
            ps[start:(end2+1)] = (['']*(end2-start)+tmp)

    for i in ps:
        if i == '':
            continue
        else:
            wrt += i

    return wrt
