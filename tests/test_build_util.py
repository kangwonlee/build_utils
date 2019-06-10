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

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import IPython.testing.globalipapp


@pytest.fixture
def ipython():

    ip = IPython.testing.globalipapp.get_ipython()

    yield ip

    del ip


def test_ipython(ipython):
    assert isinstance(ipython, IPython.terminal.interactiveshell.TerminalInteractiveShell), type(ipython)
