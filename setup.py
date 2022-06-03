import setuptools

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

with open('README.md') as _f:
    _README_MD = _f.read()

_VERSION = '0.1'

setuptools.setup(name='cardanopythonlib',
                    version=_VERSION,
                    description='Cardano Python lib to interact with the blockchain',
                    long_description=_README_MD,
                    packages=['cardanopythonlib'],
                    url='https://github.com/larestrepo/CardanoPythonLib',
                    download_url='https://github.com/larestrepo/CardanoPythonLib/tarball/{}'.format(_VERSION),
                    author='Luis Restrepo',
                    # packages=find_packages(include=['cardanopythonlib*']), 
                    test_suite="testing",
                    setup_requires=["pytest-runner"],
                    tests_require=["pytest", "pytest-cov"],
                    include_package_data=True,
                    install_requires=install_requires)