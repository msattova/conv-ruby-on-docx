import pytest

import modules.txt2docx as t2d
import modules.consts as con
from test.cases_replace_ruby import (testcode, idealcode,
                                    testcode2, idealcode2,
                                    testcode3, idealcode3,
                                    testcode4, idealcode4,
                                    testcode5, idealcode5)

def test_replace_ruby():
    template = con.make_template()
    return_code = t2d.replace_ruby(testcode, template)
    return_code2 = t2d.replace_ruby(testcode2, template)
    return_code3 = t2d.replace_ruby(testcode3, template)
    return_code4 = t2d.replace_ruby(testcode4, template)
    return_code5 = t2d.replace_ruby(testcode5, template)

    assert return_code == "".join(idealcode)
    assert return_code2 == "".join(idealcode2)
    assert return_code3 == "".join(idealcode3)
    assert return_code4 == "".join(idealcode4)
    assert return_code5 == "".join(idealcode5)


if __name__ == '__main__':
    pytest.main()
