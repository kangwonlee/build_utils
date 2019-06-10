from setuptools import setup

setup(

   name='build_util',
   version='0.1',
   description='Build (and run) C/C++ files using iPython / Jupyter magic commands',
   author='KangWon LEE',
   author_email='kangwon@gmail.com',
   packages=['build_util'],
   install_requires=['IPython', 'pytest'],
   test_suite="build_util.tests.test_all" 
   # https://setuptools.readthedocs.io/en/latest/setuptools.html#test-build-package-and-run-a-unittest-suite
)
