"""
    https://pmbaumgartner.github.io/blog/testing-ipython-magics/

    1. Import the global ipython app with from IPython.testing.globalipapp import get_ipython
    2. Create an object with the global ipython app with ip = get_ipython()
    3. Load your magic with ip.magic('load_ext your_magic_name')
    4. Run your magic with ip.run_line_magic('your_magic_function', 'your_magic_arguments')
    5. (Optional) Access results of your magic with ip.user_ns (ipython user namespace).
"""

import os
import sys

import IPython.testing.globalipapp
import pytest


@pytest.fixture(scope="module")
def ipython():

    ip = IPython.testing.globalipapp.get_ipython()

    yield ip

    del ip


def test_ipython(ipython):
    assert isinstance(ipython, IPython.terminal.interactiveshell.TerminalInteractiveShell), type(ipython)


@pytest.fixture(scope="module")
def ipython_with_build_util(ipython):

    ipython.run_cell(
        'import os\n'
        'import sys\n'
        'sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.getcwd()))))\n'
    )

    ipython.magic('load_ext build_util')

    return ipython


def test_ipython_with_build_util_hello_world(ipython_with_build_util):
    # https://pmbaumgartner.github.io/blog/testing-ipython-magics/
    ip = ipython_with_build_util

    line = 'temp'

    msg = 'Hello World!'
    cell = ('#include <iostream>\n'
        'int main(int argn, char* argv[])\n'
        '{\n'
     f'''    std::cout << "{msg}" << '\\n';\n'''
        '    return 0;\n'
        '}\n')

    result_str = ip.run_cell_magic('cpp', line, cell)

    assert result_str.strip() == msg, result_str

    # clean up
    if os.path.exists(line + '.s'):
        os.remove(line + '.s')


def test_ipython_with_build_util_hello_world_error(ipython_with_build_util):
    # https://pmbaumgartner.github.io/blog/testing-ipython-magics/
    ip = ipython_with_build_util

    line = 'temp'

    msg = 'Hello World!'
    cell = ('#include <iostream>\n'
        'int main(int argn, char* argv[])\n'
        '{\n'
     f'''    std::cout << "{msg}' << '\\n';\n'''
        '    return 0;\n'
        '}\n')

    result_str = ip.run_cell_magic('cpp', line, cell)

    assert '''error: missing terminating " character''' in result_str.strip(), result_str

    # clean up
    if os.path.exists(line + '.s'):
        os.remove(line + '.s')


if "__main__" == __name__:
    pytest.main()
