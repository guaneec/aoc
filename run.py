import argparse
import os
from subprocess import run
from pathlib import Path

commands = {
    'python': {
        'dir': './python',
        'src': 'aoc/{y}/{d}.py',
        'run': 'python -m aoc.{y}.{d}',
    },
    'nim': {
        'dir': './nim',
        'src': '{y}/D{d}.nim',
        'build': 'nim c --define:release {y}/D{d}.nim',
        'run': str(Path('./nim/{y}/D{d}.exe').resolve()),
    },
    'kotlin': {
        'dir': './kotlin',
        'src': 'src/main/kotlin/aoc/Y{y}/D{d}.kt',
        'build': 'gradle build',
        'run': 'kotlin -classpath build/classes/kotlin/main/ aoc.Y{y}.D{d}Kt'
    },
    'haskell': {
        'dir': './haskell',
        'src': 'app/{y}/{d}/Main.hs',
        'build': 'stack ghc app/{y}/{d}/Main.hs',
        'run': str(Path('./haskell/app/{y}/{d}/Main.exe').resolve())
    },
    'wolfram': {
        'src': 'wolfram/{y}/{d}.wl',
        'run': f"wolframscript -file {str(Path('./wolfram/{y}/{d}.wl').resolve())}"
    }
}


class YearDayAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        yd = values.split('.')
        if len(yd) == 2:
            y, d = yd
        else:
            y, d = values, ','.join(str(i+1) for i in range(25))
        setattr(namespace, 'years', [int(x) for x in y.split(',')])
        setattr(namespace, 'days', [int(x) for x in d.split(',')])

parser = argparse.ArgumentParser(description='Run AoC stuff')
parser.add_argument('command', choices=('run', 'bench', 'test', 'ls'), help='command')
parser.add_argument('yearday', action=YearDayAction, help=
''' Format: <year(s)>.<day(s)>
ex: 2015.1 | 2016,2017.2,3
''')
parser.add_argument('names', nargs='*', default=list(commands))
parser.add_argument('--save', action='store_true')
args = parser.parse_args()



cwd = os.getcwd()

datadir = (Path(__file__).parent / 'data').resolve()

for y in args.years:
    for d in args.days:
        print(f'>>> {args.command} {y}.{d}')
        for k, v in commands.items():
            if k not in args.names:
                continue
            os.chdir(cwd)
            yd = dict(y=y, d=f'{d:02d}')
            if 'dir' in v:
                os.chdir(v['dir'])
            exists = Path(v['src'].format(**yd)).is_file()
            if args.command == 'ls':
                if exists:
                    print(k)
                continue
            
            if not exists:
                print(f'src not found: {k}')
                continue
                
            if 'build' in v:
                build_cmd = v['build'].format(**yd)
                print(f'Building {k}')
                print('>', build_cmd)
                run(build_cmd, check=True, shell=True)
            run_cmd = v['run'].format(**yd)
            if args.command == 'run':
                print(f'Running {k}')
                print('>', run_cmd)
                if args.save:
                    p = run(run_cmd, shell=True, encoding='utf-8', capture_output=True)
                    if p.stdout:
                        print(p.stdout, end='')
                    if p.stderr:
                        print(p.stderr, end='')
                    p.check_returncode()
                    with open(datadir / f'{y}/{d:02d}.output.txt', 'w') as f:
                        f.write(p.stdout)
                        print(f'Output saved to {f.name}')
                else:
                    p = run(run_cmd, shell=True, check=True)
            elif args.command == 'bench':
                print(f'Benching {k}')
                bench_cmd = f'hyperfine -w 1 -m 2  "{run_cmd}"'
                print('>', bench_cmd)
                run(bench_cmd, check=True, shell=True)
