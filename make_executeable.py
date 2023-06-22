from cx_Freeze import setup, Executable

# Specify the main script and any additional dependencies
options = {
    'build_exe': {
        'packages': ['PySimpleGUI', 'pandas', 'torch', 'numpy',  'sklearn', 'subprocess','ctypes','wmi','psutil'],
        'excludes': [],
        'include_files': ['model.pt']
    }
}

# Create an executable
executables = [
    Executable('program_exe.py', base=None)  # Replace 'your_script.py' with your main script name
]

setup(
    name='my_1st_app',
    version='1.0',
    description='Description of your app',
    options=options,
    executables=executables
)
