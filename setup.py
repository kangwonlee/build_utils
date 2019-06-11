from setuptools import setup, find_packages

setup(

   name='build_util',
   version='0.1',
   description='Build (and run) C/C++ files using iPython / Jupyter magic commands',
   author='KangWon LEE',
   author_email='kangwon@gmail.com',
   packages=find_packages(),
   install_requires=['IPython', 'pytest'],
   setup_requires=["pytest-runner",],
   tests_require=['pytest', 'IPython'],
   test_suite="tests",
   # https://setuptools.readthedocs.io/en/latest/setuptools.html#test-build-package-and-run-a-unittest-suite
)
