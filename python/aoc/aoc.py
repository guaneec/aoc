from pathlib import Path
import sys
import subprocess

rootdir = Path(__file__) / '../../../'
def getinput(year, day):
    p = rootdir / f'data/{year}/{day:02d}.input.txt'
    if not p.is_file():
        cp = subprocess.run(f"python {rootdir / 'data.py'}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(cp.stdout.decode('utf-8'))
        cp.check_returncode()
    with open(p) as f:
        return f.read()
