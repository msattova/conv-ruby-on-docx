import pytest

import modules.txt2docx as t2d
import modules.consts as con
from test.cases_isolate import (testcode, idealcode,
                                testcode2, idealcode2,
                                testcode3, idealcode3,
                                testcode4, idealcode4,
                                testcode5, idealcode5)

def test_isolate():
    template = con.make_template()
    returncode = t2d.isolate(t2d.RubyType.NONPIPE, testcode2, template[3], template[4])
    assert ''.join(returncode) == ''.join(idealcode2)


def test_isolate_rubyset():
    template = con.make_template()
    return_code = t2d.isolate_rubysets(testcode, template[3], template[4])
    return_code2 = t2d.isolate_rubysets(testcode2, template[3], template[4])
    return_code3 = t2d.isolate_rubysets(testcode3, template[3], template[4])
    return_code4 = t2d.isolate_rubysets(testcode4, template[3], template[4])
    return_code5 = t2d.isolate_rubysets(testcode5, template[3], template[4])
    assert "".join(return_code) == "".join(idealcode)
    assert "".join(return_code2) == "".join(idealcode2)
    assert "".join(return_code3) == "".join(idealcode3)
    assert "".join(return_code4) == "".join(idealcode4)
    assert "".join(return_code5) == "".join(idealcode5)

def test_code_to_list():
    return_code = t2d.code_to_list("".join(testcode))
    assert return_code == [i for i in testcode if i != '']

if __name__ == '__main__':
    pytest.main()
