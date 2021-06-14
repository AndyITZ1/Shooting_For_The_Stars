from setuptools import setup

setup(
    name='shooting_for_the_stars',  # Name of the PyPI package. All lower-case with _ separating words.
    version='0.1',
    packages=['projectss'],  # Name of the modules. Do we need any, since we are developing a game?
    url='https://github.com/Andytr13/Shooting_For_The_Stars',
    license='MIT',
    author='Luan Tran, Daniel Brodbeck, Jose Lopez, Elizaveta Vlasova, Calvin Yang',
    author_email='ltran3@ufl.edu, dbrodbeck@ufl.edu, joselopez7693@ufl.edu, vlasovae@ufl.edu, cyang2@ufl.edu',
    description='A 2D rythym-based vertical platformer video game.',
    install_requires=["pygame"]
)
