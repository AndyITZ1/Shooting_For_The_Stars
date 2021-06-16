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



## Creating the Executable

Along with pygame installed, you need to install the "cx_Freeze" package. This package is what's used to create an executable and the MSI.

- In a terminal (such as the one in PyCharm), run "python setup.py build". This will create an executable located in the new build directory.
- In a terminal (such as the one in PyCharm), run "python setup.py bdist_msi". This will create an MSI in the new dist directory.  Running this MSI will guide you in the installation process for the game.
