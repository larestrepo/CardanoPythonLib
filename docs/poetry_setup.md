# Working with poetry as virtual environment and to handle the project setup


### Install poetry

```shell
curl -sSL https://install.python-poetry.org | python3 -

poetry new cardanopythonlib
```
## Add dependencies
```shell
poetry add <dependency>
```

### Building and publishing to PyPI

1. Set the version
```shell
poetry version 0.1.0
poetry build
```
2. Configure PyPi test repository

- Configure the token for poetry to connect with Pypi
```shell
poetry config pypi-token.pypi <token>
```
- Or configure testpypi as follows:
```shell
poetry config repositories.testpypi https://test.pypi.org/legacy/
```

3. Publish the package
- If with token configured:
```shell
    poetry publish
```
- If working with testpypi and username and password
```shell
poetry publish -r testpypi -u <username> -p <password> --dry-run
poetry publish -r testpypi -u <username> -p <password>
# To publish it in actual PyPi
poetry publish -u <username> -p <password>
```

### Update Packages with Poetry
```shell
    poetry show -l
    poetry update
```


Reference:
[pypi and poetry](https://www.digitalocean.com/community/tutorials/how-to-publish-python-packages-to-pypi-using-poetry-on-ubuntu-22-04)
[Update](https://www.yippeecode.com/topics/update-packages-in-python-poetry/)