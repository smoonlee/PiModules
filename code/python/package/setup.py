"""pimodules: PiModules(R) Product support Python package

A package which contains code to support PiModules products of various kinds.
"""

classifiers = """\
Development Status :: 5 - Testing/Beta
Intended Audience :: PiModules Product Developers
License :: OSI Approved :: GNU General Public License v3 (GPLv3)
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Topic :: PiModules(R)
Topic :: PiModules(R) Products Python Package
Operating System :: POSIX :: Linux
"""

from setuptools import setup

doclines = __doc__.split("\n")

setup(
    name='pimodules',
    version='0.1dev',
    description=doclines[0],
    long_description="\n".join(doclines[2:]),
    license='GPL3',
    author='Mike Ray',
    author_email='mike.ray@btinternet.com',
    url='http://pimodules.com',
    platforms=['POSIX'],
    classifiers=classifiers.split('\n'),
    packages=['pimodules'],
    python_requires='>=3.6',
)
