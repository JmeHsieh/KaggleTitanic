# Kaggle Titanic
A script version of ipython notebook from [agconti's kaggle-titanic repo](https://github.com/agconti/kaggle-titanic) <br />
[Kaggle Competition Homepage](https://www.kaggle.com/c/titanic) <br />
<br />

## Environment
Mac OS X El Capitan<br />
Framework build Python 3.5.1 (via pyenv)<br />
<br />

## Installation

#### Python
```
$ brew update && brew install pyenv
```
```
$ env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.5
```

#### Virtualenv
```
$ cd KaggleTitanic
$ virtualenv venv
$ source ./venv/bin/activate
```

#### Link framework build python
```
$ mv frameworkpython ./venv/bin/
$ pip install -r requirements.txt
```

#### Run
```
$ frameworkpython main.py
```
<br />

## License
[MIT](https://opensource.org/licenses/mit-license.php)