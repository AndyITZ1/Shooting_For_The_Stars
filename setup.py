from setuptools import setup

setup(
    name='shooting_for_the_stars',  # Name of the PyPI package. All lower-case with _ separating words.
    version='0.0.1',
    description='A 2D rhythm-based vertical platformer video game.',
    license='MIT',
    author='Luan Tran, Daniel Brodbeck, Jose Lopez, Elizaveta Vlasova, Calvin Yang',
    author_email='ltran3@ufl.edu, dbrodbeck@ufl.edu, joselopez7693@ufl.edu, vlasovae@ufl.edu, cyang2@ufl.edu',
    url='https://github.com/Andytr13/Shooting_For_The_Stars',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Topic :: Software Development :: Libraries :: pygame",
        "Topic :: Games/Entertainment"
    ],
    packages=['projectSS', ],  # Name of the modules. Do we need any, since we are developing a game?
    install_requires=[
        "pygame >= 2.0.1"
    ],

    entry_points=
    {"console_scripts":     # ?
        [
            "shooting_for_the_stars = projectSS:main"
        ]
    }
)
