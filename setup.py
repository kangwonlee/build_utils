from setuptools import setup

setup(
   name='build_util',
   version='0.1',
   description='Build (and run) C/C++ files using iPython / Jupyter magic commands',
   author='KangWon LEE',
   author_email='kangwon@gmail.com',
   packages=['build_util'],
   install_requires=['IPython', 'pytest'],
)
