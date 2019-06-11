# https://stackoverflow.com/questions/10361206/how-to-run-an-ipython-magic-from-a-script-or-timing-a-python-script
import os
import subprocess
import sys
import tempfile

import IPython
import IPython.core.magic
import IPython.display as disp

# obtain ipython
try:

    ipython = IPython.get_ipython()

except AttributeError:
    try:
        import IPython.core.ipapi
        ipython = IPython.core.ipapi.get()
    except ModuleNotFoundError:
        import IPython.ipapi
        ipython = IPython.ipapi.get()


@IPython.core.magic.magics_class
class CppMagic(IPython.core.magic.Magics):
    @IPython.core.magic.cell_magic
    def cpp(self, line, cell):
        # https://ipython.readthedocs.io/en/stable/config/custommagics.html#defining-custom-magics

        filename = self.get_filename(line)

        code = cell.strip()

        with open(filename, 'wt', encoding='utf-8') as f:
            f.write(code)

        build_result = build_cpp(filename)

        if build_result.returncode:
            result = self.get_stdout_stderr(build_result)

        else:
            run_result = run(filename)
            run_result.check_returncode()

            result = self.get_stdout_stderr(run_result)

        cleanup(filename)

        return result

    @staticmethod
    def get_stdout_stderr(run_result):
        result_list = []

        if run_result.stdout:
            result_list.append(run_result.stdout.decode())

        if run_result.stderr:
            result_list.append(run_result.stderr.decode())

        result = '=====\n'.join(result_list)

        return result

    @staticmethod
    def get_filename(line):
        if not line:
            line = tempfile.gettempprefix() + '.cpp'

        filename = os.path.abspath(line.strip().split()[0])

        basename, ext = os.path.splitext(filename)

        if not ext:
            ext = '.cpp'
            filename = ''.join((basename, ext))
        elif ext not in ('.cpp', '.c'):
            raise NotImplementedError
        return filename


def write_file(filename, code):
    """
    Write a new file
    To make C/C++ source code file
    """
    ipython.run_cell_magic("writefile", filename, code)


def build_cpp(filename):
    """
    Build cpp file
    filename : ex) test or test.cpp
    """
    # Detect OS type because OSX may need different options
    # https://stackoverflow.com/questions/3466166/how-to-check-if-running-in-cygwin-mac-or-linux/18790824

    basename, ext = os.path.splitext(filename)

    if not ext:
        filename += '.cpp'

    assert os.path.exists(filename)

    # for debug purpose
    if 'CI' in os.environ:
        print(f"sys.platform = {sys.platform}")

    if sys.platform.lower().startswith('linux'):
        # build command for Linux
        r = subprocess.run([
            'g++', '-Wall', '-g', '-std=c++14', filename,
            '-o', os.path.join(os.curdir, basename), # output file name
            f'-Wa,-adhln={basename}.s',
            ],
            check=False,
            capture_output=True,
        )
    else:
        # Otherwise
        r = subprocess.run([
            'g++', '-Wall', '-g', '-std=c++14',
            '-o',  os.path.join(os.curdir, f'{basename}'), filename,
            ],
            check=False,
            capture_output=True,
        )

    return r


def run(cpp_filename):
    """
    Run the execution file from the cpp file
    cpp_filename : ex) test or test.cpp
    """
    basename, ext = os.path.splitext(cpp_filename)
    # https://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output
    # https://stackoverflow.com/questions/35160256/how-do-i-output-lists-as-a-table-in-jupyter-notebook

    # Run executable while capturing output
    result = subprocess.run(
            [os.path.join(os.curdir, basename)],
            stdout=subprocess.PIPE,
            check=True,
    )

    # present output
    return result


def cleanup(cpp_filename):
    """
    Clean up cpp and execution files
    Assume execution file name is basename of the cpp filename
    cpp_filename : ex) test or test.cpp
    """
    basename, ext = os.path.splitext(cpp_filename)
    if not ext:
        cpp_filename += '.cpp'

    # to delete execution file
    if os.path.exists(basename):
        os.remove(basename)
    else:
        print(f"Unable to find {basename}")
        print(os.listdir())

    # to delete source file
    os.remove(cpp_filename)


def run_markdown(cpp_filename):
    """
    Run execution file from the cpp file
    and present the output as markdown
    cpp_filename : ex) test or test.cpp
    """
    basename, ext = os.path.splitext(cpp_filename)
    # https://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output
    # https://stackoverflow.com/questions/35160256/how-do-i-output-lists-as-a-table-in-jupyter-notebook

    # Run executable while capturing output
    result = subprocess.run(
            [os.path.join(os.curdir, basename)],
            stdout=subprocess.PIPE,
            check=True,
    )
    # present output as a markdown
    disp.display(disp.Markdown(result.stdout.decode()))


def get_tempfile_name():
    # https://stackoverflow.com/a/26541521
    tempname = next(tempfile._get_candidate_names())

    return tempname
