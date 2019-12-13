import requests
from os import makedirs
from pathlib import Path

with open("session.txt") as f:
    cookies = {"session": f.read().strip()}

datadir = Path(__file__) / ('../data')


makedirs(datadir, exist_ok=True)

print("fetching inputs...")

for i in range(1,26):
    filepath = datadir / f'{i:02d}.input.txt'
    if filepath.is_file():
        continue

    url = f'https://adventofcode.com/2019/day/{i}/input'
    r = requests.get(url, cookies=cookies)
    if r.status_code != 200:
        print(f'failed fetching input for day {i} (status={r.status_code})')
        break
    
    with open(filepath, 'w') as f:
        f.write(r.text)
        print(f'fetched {str(filepath)}')
