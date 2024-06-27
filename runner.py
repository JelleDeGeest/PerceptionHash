import subprocess

command_1 = [
    'C:/Users/jelle/AppData/Local/Programs/Python/Python311/python.exe',
    './ImageDistorter.py',
    '-m', 'rotation',
    '-i', 'MetaTestset_1'
]

command_2 = [
    'C:/Users/jelle/AppData/Local/Programs/Python/Python311/python.exe',
    './ImageDistorter.py',
    '-m', 'crop_rotation',
    '-i', 'MetaTestset_1'
]

command_3 = [
    'C:/Users/jelle/AppData/Local/Programs/Python/Python311/python.exe',
    './ImageDistorter.py',
    '-m', 'rotation',
    '-i', 'MetaTestset_2'
]

command_4 = [
    'C:/Users/jelle/AppData/Local/Programs/Python/Python311/python.exe',
    './ImageDistorter.py',
    '-m', 'crop_rotation',
    '-i', 'MetaTestset_2'
]


subprocess.run(command_1)
subprocess.run(command_2)
subprocess.run(command_3)
subprocess.run(command_4)
