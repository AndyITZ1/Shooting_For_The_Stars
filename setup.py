from setuptools import setup
from setuptools.command import install, sdist


class SrcDistro(sdist.sdist):
    def run(self):
        sdist.sdist.run(self)


class Installer(install.install):
    def run(self):
        install.install.run(self)


if __name__ == "__main__":
    setup(
        cmdclass={"install": Installer, "sdist": SrcDistro},
    )

# import cx_Freeze
#
# executables = [cx_Freeze.Executable("projectSS/main.py")]
#
# cx_Freeze.setup(
#     name='Shooting For The Stars',
#     options={'build_exe': {'packages': ['pygame'],
#                            "include_files": ['projectSS/assets']}},
#     description='A 2D rhythm-based vertical platformer video game',
#     executables=executables
# )
