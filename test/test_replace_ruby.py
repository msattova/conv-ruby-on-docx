import pytest

import modules.txt2docx as t2d
import modules.consts as con
from test.cases_replace_ruby import (testcode, idealcode,
                                    testcode2, idealcode2,
                                    testcode3, idealcode3)

def test_replace_ruby():
    template = con.make_template()
    return_code = t2d.replace_ruby(testcode, template)
    '''
    print(f"ideal:\t {t2d.code_to_list(''.join(idealcode))}\n")
    print(f"ret:\t {t2d.code_to_list(return_code)}\n")
    '''
    return_code2 = t2d.replace_ruby(testcode2, template)
    return_code3 = t2d.replace_ruby(testcode3, template)

    assert return_code == "".join(idealcode)
    assert return_code2 == "".join(idealcode2)
    assert return_code3 == "".join(idealcode3)


if __name__ == '__main__':
    pytest.main()
