import pytest

import modules.txt2docx as t2d
import modules.consts as con
from test.cases_isolate import (testcode, idealcode,
                                testcode2, idealcode2,
                                testcode3, idealcode3,
                                testcode4, idealcode4,
                                testcode5, idealcode5,
                                testcode6, idealcode6,
                                testcode7, idealcode7,
                                testcode8, idealcode8)

template = con.Template(font='', emtype='').template

def test_isolate():
    returncode = t2d.isolate(t2d.RubyType.NONPIPE, testcode2, template.general_open, template.general_end)
    assert ''.join(returncode) == ''.join(idealcode2)


def test_isolate_rubysets():
    return_code  = t2d.isolate_rubysets(testcode,  template.general_open, template.general_end)
    return_code2 = t2d.isolate_rubysets(testcode2, template.general_open, template.general_end)
    return_code3 = t2d.isolate_rubysets(testcode3, template.general_open, template.general_end)
    return_code4 = t2d.isolate_rubysets(testcode4, template.general_open, template.general_end)
    return_code5 = t2d.isolate_rubysets(testcode5, template.general_open, template.general_end)
    return_code6 = t2d.isolate_rubysets(testcode6, template.general_open, template.general_end)
    return_code7 = t2d.isolate_rubysets(testcode7, template.general_open, template.general_end)
    return_code8 = t2d.isolate_rubysets(testcode8, template.general_open, template.general_end)

    assert "".join(return_code)  == "".join(idealcode)
    assert "".join(return_code2) == "".join(idealcode2)
    assert "".join(return_code3) == "".join(idealcode3)
    assert "".join(return_code4) == "".join(idealcode4)
    assert "".join(return_code5) == "".join(idealcode5)
    assert "".join(return_code6) == "".join(idealcode6)
    assert "".join(return_code7) == "".join(idealcode7)
    assert "".join(return_code8) == "".join(idealcode8)

def test_bouten():
    template = con.Template(font='', emtype='').template
    return_code8 = t2d.isolate(
        t2d.RubyType.BOUTEN, testcode8, template.general_open, template.general_end)
    assert "".join(return_code8) == "".join(idealcode8)


def test_code_to_list():
    return_code = t2d.code_to_list("".join(testcode))
    assert return_code == [i for i in testcode if i != '']

if __name__ == '__main__':
    pytest.main()
