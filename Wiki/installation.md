# Easy
Open up a terminal and run ```pipx install gambling-simulator```

If pipx isn't installed run ```pip install pipx``` and rerun the command above.

# Advanced
## Option 1
Go to the repository and open a terminal.
### Windows
Run ```python -m pip install .\requirements.txt```

### Linux
Run ```python -m pip install ./requirements.txt```

## Option 2
## Create python venv
Currently there are problems getting tkinter running in a venv so you have the option to fix it by yourself [here](https://stackoverflow.com/questions/15884075/tkinter-in-a-virtualenv). <br>
To create the venv go to the repository and open a terminal there. Then run ```python -m venv venv```.

## Install dependencies
### Windows
Run ```.\venv\Scripts\python -m pip install -r .\requirements.txt --no-cache```

### Linux
Run ```./venv/bin/python -m pip install -r ./requirements.txt --no-cache```