import cx_Freeze

executables = [cx_Freeze.Executable("projectSS/main.py")]

cx_Freeze.setup(
    name='Shooting For The Stars',
    options={'build_exe': {'packages': ['pygame'],
                           "include_files": ['projectSS/assets']}},
    description='A 2D rhythm-based vertical platformer video game',
    executables=executables
)
