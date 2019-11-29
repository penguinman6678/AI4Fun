
# AI4Fun
to put things together for instructions/summaries/examples

## Prerequisites
#### systems
1. OS: Mac
2. Programming: Python 3.6+
   - how to install virtualenv
```sh
$>python3 -m pip install virtualenv
```
   - install python using virtualenv
      - to create a local version of python env, you can create an virtual env for a python
```sh
$>virtualenv -p python3 my_venv_test
$> source my_venv_test/bin/activate
# Note that python3 is the executable python version you want to use as a default 
# for the environment you are creating, "my_venv_test"
# For example, you can specify -- "/usr/local/.../Python.framework/Versions/3.7/bin/python3" instead of python3
 ``` 
   - install modules such as numpy, etc
```sh
(my_venv_test)$>pip3 install numpy
(my_venv_test)$>deactivate
```
   - when you are going to use the venv python
```sh
$>alias vpython3='/Users/buddy/my_venv_test/bin/python3'
## or you can add the above alias line into your bash_profile and source
```
   - How to add above alias to your system
```sh
$> emacs ~/.bash_profile
# copy and paste the above alias line
# save and quit
$> source ~/.bash_profile
$>vpython3
Python 3.7.2 (default, Feb 12 2019, 08:16:38)
[Clang 10.0.0 (clang-1000.11.45.5)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

3. Decide which IDE (e.g. programming editor such as emacs, pycharm, etc)
   - [PyCharm Community version](https://www.jetbrains.com/pycharm/)
4. Start to write/draw ideas on papers (before start to write blocks of codes, always write/draw your ideas on papers to visualize/constrcut steps)

## First programming excercise
#### Boardgame
##### Tic-Tac-Toe (3 by 3 size of a board)
1. [Tic-Tac-Toe](boardGames/README.md)
