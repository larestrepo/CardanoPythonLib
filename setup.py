import setuptools
import pathlib
import sys
import codecs
import os.path

HERE = pathlib.Path(__file__).parent

long_description = (HERE / 'README.md').read_text(encoding='utf-8')


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setup_requires = (
    ["pytest-runner"] if any(x in sys.argv for x in ("pytest", "test", "ptr")) else []
)

setuptools.setup(
    name='cardanopythonlib',
    version=get_version("cardanopythonlib/__init__.py"),
    description='Cardano Python lib to interact with the blockchain',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/larestrepo/CardanoPythonLib',
    license='Apache-2.0',
    python_requires='>=3.5',
    tests_require=[
        "pytest"
    ],

    # Author details
    author='Moxie',
    author_email='luis.restrepo@ayllu.io',
    packages=setuptools.find_packages(),
    platforms=["any"],
    test_suite="tests",
    setup_requires=setup_requires,
    include_package_data=True,
    install_requires=['setuptools','Cerberus==1.3.4'])
