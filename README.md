# Shooting_For_The_Stars

Group Project for CIS4930

## Development Setup

This project should be developed in a clean virtual environment with pygame installed. To set up a new virtual environment that follows these requirements in PyCharm, do the following:

1. File > Settings > Project > Python Interpreter
2. Gear Icon > Add > Virtualenv Environment > New environment
3. IMPORTANT: the location of the virtual environment does NOT need to exist in the project directory. It is discouraged to do so since venvs are not typically added in repos since they add up after numerous pushes. Instead, designate a separate directory to contain your venvs.
4. Make available to all projects > OK
5. After your new venv interpreter is selected, click on the plus icon
6. search pygame > Install Package
7. Apply

Now you can test if your venv is ready by right clicking on main.py and running it. While the project directory might change throughout development, your venv will not be destroyed or changed.



## Source Distribution and Installation

To create a source distribution from the project, go to the directory "Shooting_For_The_Stars" and execute the setup.py script like so: "python setup.py sdist". This will create a new dist directory containing your sdist.

If you want to install this sdist, say on a new computer or in a new venv, you can either

- go to the extracted sdist directory and run the command "python setup.py install".
- Run the command "pip install -e <absolute path to the project directory>"

Once the game is installed, you can run it in a command window by running "shooting_for_the_stars".
