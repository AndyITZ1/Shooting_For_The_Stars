import cx_Freeze
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"    # Tells the build script to hide the console.

executables = [cx_Freeze.Executable("projectSS/main.py", targetName="Shooting For The Stars", base=base)]

cx_Freeze.setup(
    name='Shooting_For_The_Stars',
    options={'build_exe': {'packages': ['pygame'],
                           "include_files": ['projectSS/assets']}},
    description='A 2D rhythm-based vertical platformer video game',
    executables=executables
)
