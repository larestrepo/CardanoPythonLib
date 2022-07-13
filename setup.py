import setuptools
import pathlib
import sys

HERE = pathlib.Path(__file__).parent

long_description = (HERE / 'README.md').read_text(encoding='utf-8')

_VERSION = '1.0.1'

setup_requires = (
    ["pytest-runner"] if any(x in sys.argv for x in ("pytest", "test", "ptr")) else []
)

setuptools.setup(
    name='cardanopythonlib',
    version=_VERSION,
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
    install_requires=["setuptools"])
