import setuptools
import pathlib

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

HERE = pathlib.Path(__file__).parent

long_description = (HERE / 'README.md').read_text(encoding='utf-8')

_VERSION = '0.1'

setuptools.setup(
    name='cardanopythonlib',
    version=_VERSION,
    description='Cardano Python lib to interact with the blockchain',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/larestrepo/CardanoPythonLib',
    download_url='https://github.com/larestrepo/CardanoPythonLib/tarball/{}'.format(_VERSION),
    license='Apache-2.0',
    python_requires='>=3.7, <4',
    tests_require=[
        "pytest",
        "mock",
        "requests-mock",
    ],

    # Author details
    author='Moxie',
    packages=setuptools.find_packages(include=['cardanopythonlib*']),
    test_suite="testing",
    setup_requires=["pytest-runner"],
    include_package_data=True,
    install_requires=install_requires)
