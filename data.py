import requests
from os import makedirs
from pathlib import Path

with open(Path(__file__) / "../session.txt") as f:
    cookies = {"session": f.read().strip()}

datadir = Path(__file__) / ('../data')



print("fetching inputs...")

for y in [2017, 2018, 2019]:
    diryear = datadir / str(y)
    makedirs(diryear, exist_ok=True)
    for i in range(1,26):
        filepath = diryear / f'{i:02d}.input.txt'
        if filepath.is_file():
            continue

        url = f'https://adventofcode.com/{y}/day/{i}/input'
        r = requests.get(url, cookies=cookies)
        if r.status_code != 200:
            print(f'failed fetching input for day {i} (status={r.status_code})')
            break
        
        with open(filepath, 'w') as f:
            f.write(r.text)
            print(f'fetched {str(filepath)}')
