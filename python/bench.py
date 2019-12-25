from subprocess import run
from os import makedirs, getcwd
from pathlib import Path
import argparse

parser = argparse.ArgumentParser('Run benchmark')
parser.add_argument('year', nargs='?', type=int)
parser.add_argument('days', nargs=argparse.REMAINDER, type=int)
args = parser.parse_args()
years = [args.year] if args.year is not None else list(range(2015, 2020))
days = args.days if args.days else list(range(1, 26))


rootdir = Path(__file__) / '../aoc'



for y in years:
    benchdir = rootdir / f'{y}/benchmark'
    for d in days:
        makedirs(benchdir, exist_ok=True)
        exppath = benchdir / f'{d:02d}.md'
        cmd = f'hyperfine --export-markdown "{exppath.resolve()}" "python -m aoc.{y}.{d:02d}"'
        print(cmd)
        ps = run(cmd)
        ps.check_returncode()

