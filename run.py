import argparse
import os
from subprocess import run
from pathlib import Path

commands = {
    'python': {
        'dir': './python',
        'run': 'python -m aoc.{y}.{d:02d}'
    },
    'nim': {
        'dir': './nim',
        'build': 'nim c --define:release {y}/D{d:02d}.nim',
        'run': str(Path('./nim/{y}/D{d:02d}.exe').resolve())
    },
    'kotlin': {
        'dir': './kotlin',
        'build': 'gradle build',
        'run': 'kotlin -classpath build/classes/kotlin/main/ aoc.Y{y}.D{d:02d}Kt'
    },

}


class YearDayAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        y, d = values.split('.')
        setattr(namespace, 'years', [int(x) for x in y.split(',')])
        setattr(namespace, 'days', [int(x) for x in d.split(',')])

parser = argparse.ArgumentParser(description='Run AoC stuff')
parser.add_argument('command', choices=('run', 'bench', 'test'), help='command')
parser.add_argument('yearday', action=YearDayAction, help=
''' Format: <year(s)>.<day(s)>
ex: 2015.1 | 2016,2017.2,3
''')
parser.add_argument('names', nargs='*', default=list(commands))
args = parser.parse_args()



cwd = os.getcwd()

for y in args.years:
    for d in args.days:
        for k, v in commands.items():
            if k not in args.names:
                continue
            os.chdir(cwd)
            if 'dir' in v:
                os.chdir(v['dir'])
            if 'build' in v:
                build_cmd = v['build'].format(y=y, d=d)
                print(f'Building {k}')
                print('>', build_cmd)
                run(build_cmd, check=True, shell=True)
            run_cmd = v['run'].format(y=y, d=d)
            if args.command == 'run':
                print(f'Running {k}')
                print('>', run_cmd)
                run(run_cmd, check=True, shell=True)
            elif args.command == 'bench':
                print(f'Benching {k}')
                bench_cmd = f'hyperfine -w 1 -m 2  "{run_cmd}"'
                print('>', bench_cmd)
                run(bench_cmd, check=True, shell=True)
