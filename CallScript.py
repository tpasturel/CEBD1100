import os, subprocess
files = filter(os.path.isfile, os.listdir( os.curdir ))
for file in files:
    if file.endswith(".data"):
        subprocess.call("python3 CEBD1100_Homework5_ThibaultPasturel.py -i" + str(file), shell=True)