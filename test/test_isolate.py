import pytest

import modules.txt2docx as t2d
import modules.consts as con
from test.cases_isolate import (testcode, idealcode,
                                testcode2, idealcode2)

def test_isolate():
    template = con.make_template()
    returncode = t2d.isolate(con.REG_KANJI_AND_RUBY_AROUND, testcode2, template[3], template[4])
    assert ''.join(returncode) == ''.join(idealcode2)


def test_isolate_rubyset():
    template = con.make_template()
    return_code = t2d.isolate_rubysets(testcode, template[3], template[4])
    assert "".join(return_code) == "".join(idealcode)


def test_code_to_list():
    return_code = t2d.code_to_list("".join(testcode))
    assert return_code == [i for i in testcode if i != '']

if __name__ == '__main__':
    pytest.main()
